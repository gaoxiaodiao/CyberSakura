import angr
import claripy

p = angr.Project("./obfuscaxor")

flag = claripy.BVS("flag", 8 * 0x10)

st = p.factory.entry_state(
    args = ["./obfuscaxor"],
    add_options = angr.options.unicorn,
    stdin = flag
)
sm = p.factory.simulation_manager(st)
sm.explore(find=0x400000 + 0x2137, avoid=0x400000 + 0x219e)
found = sm.found[-1]

keys = found.solver.eval(flag)
print(keys)

# AAAABBBBCCCCDDDD
# 0x55555575c010: 0xaeffec9f      0xadfcef9c      0xacfdee9d      0xabfae99a
# 0x55555575c010: 0xadffec9f      0xadfcef9c      0xacfdee9d      0xabfae99a
# 0x55555575c010: 0xadfcef9c      0xaeffec9f      0xacfdee9d      0xabfae99a
