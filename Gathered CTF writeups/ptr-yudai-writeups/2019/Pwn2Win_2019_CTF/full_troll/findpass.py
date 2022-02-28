import angr

p = angr.Project("./full_troll", load_options={"auto_load_libs": False})
state = p.factory.entry_state()
simgr = p.factory.simulation_manager(state)
simgr.explore(find=0x400D3F, avoid=(0x400A79, 0x400D38))
try:
    found = simgr.found[0]
    print(found.posix.dumps(0))
except IndexError:
    print("Not Found")
