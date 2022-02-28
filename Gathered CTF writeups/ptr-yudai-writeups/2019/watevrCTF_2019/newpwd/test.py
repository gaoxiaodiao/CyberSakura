import pickle

pattern = pickle.load(open("char.db", "rb"))
for key in pattern:
    print(key, len(pattern[key]))
