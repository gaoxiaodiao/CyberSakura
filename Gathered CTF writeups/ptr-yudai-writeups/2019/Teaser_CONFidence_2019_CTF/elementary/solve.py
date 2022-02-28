import angr
import claripy

p = angr.Project("./elementary")

flag = claripy.BVS("flag", 200*8)

st = p.factory.entry_state(
    args = ["./elementary"],
    add_options = angr.options.unicorn,
    stdin = flag
)
for byte in flag.chop(8):
    st.add_constraints(byte >= '\x20') # ' '
    st.add_constraints(byte <= '\x7e') # '~'
sm = p.factory.simulation_manager(st)
sm.explore(find=0x400000 + 0x773, avoid=0x400000 + 0x786)
found = sm.found[-1]

keys = found.solver.eval(flag)
print(keys)
