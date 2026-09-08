def writer_key(name):
    return name.strip().casefold()

def reader_key(name):
    return name.lower()

def save(store, name, value):
    store[writer_key(name)] = value

def read(store, name):
    return store.get(reader_key(name))
