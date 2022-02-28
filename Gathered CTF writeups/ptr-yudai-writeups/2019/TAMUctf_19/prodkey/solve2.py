import angr
import claripy

p = angr.Project("./prodkey")

flag = claripy.BVS("flag", 8 * 0x1D)

st = p.factory.entry_state(
    args = ["./prodkey"],
    add_options = angr.options.unicorn,
    stdin = flag
)
sm = p.factory.simulation_manager(st)
sm.explore(find=0x400e4e, avoid=0x400ead)
found = sm.found[-1]

def is_symbol(state, byte):
    is_num = state.solver.And(byte >= b"0", byte <= b"9")
    is_alpha_lower = state.solver.And(byte >= b"a", byte <= b"z")
    is_alpha_upper = state.solver.And(byte >= b"A", byte <= b"Z")
    is_bar = byte == b"-"
    return state.solver.Or(is_num, is_alpha_lower, is_alpha_upper, is_bar)

for i in range(0x1D):
    found.add_constraints(is_symbol(found, flag.chop(8)[i]))

keys = found.solver.eval(flag)
print(keys)
