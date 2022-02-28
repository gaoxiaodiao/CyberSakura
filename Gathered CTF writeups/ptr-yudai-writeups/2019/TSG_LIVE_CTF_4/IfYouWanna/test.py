import angr

p = angr.Project("./IfYouWanna", load_options={"auto_load_libs": False})
state = p.factory.entry_state()
simgr = p.factory.simulation_manager(state)
simgr.explore(find=0x40096c, avoid=0x400956)
try:
    found = simgr.found[0]
    print(found.posix.dumps(0))
except IndexError:
    print("Not Found")
