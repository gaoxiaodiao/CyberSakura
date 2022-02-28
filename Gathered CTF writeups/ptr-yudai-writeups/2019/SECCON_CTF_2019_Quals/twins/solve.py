import angr
import claripy
from logging import getLogger, WARN

getLogger("angr").setLevel(WARN + 1)

p = angr.Project("./Brother1",
                 load_options={"auto_load_libs": False})
state = p.factory.entry_state()
simgr = p.factory.simulation_manager(state)

p.hook_symbol("__libc_start_main", angr.SIM_PROCEDURES["glibc"]["__libc_start_main"]())
p.hook_symbol("printf", angr.procedures.libc.printf.printf())
p.hook_symbol("strlen", angr.procedures.libc.strlen.strlen())
p.hook_symbol("__isoc99_sscanf", angr.procedures.libc.scanf.scanf())
p.hook_symbol("sprintf", angr.procedures.libc.sprintf.sprintf())
p.hook_symbol("memcmp", angr.procedures.libc.memcmp.memcmp())
p.hook_symbol("memset", angr.procedures.libc.memset.memset())
p.hook_symbol("calloc", angr.procedures.libc.calloc.calloc())
p.hook_symbol("stat", angr.procedures.linux_kernel.stat.stat())
p.hook_symbol("read", angr.procedures.posix.read.read())
p.hook_symbol("write", angr.procedures.posix.write.write())

@p.hook(0x4011ef, length=0)
def hook_arc4(state):
    data = state.memory.load(state.regs.rdi, state.regs.rsi)
    print(state.solver.eval(data, cast_to=bytes))
    return
class hook_chkenv(angr.SimProcedure):
    def run(self, arg1):
        return claripy.BVV(1, 32)
p.hook_symbol("chkenv", hook_chkenv())

simgr.explore(find=0x40185e, avoid=0x4018bd)
