def summarize(items):
    """Return unique normalized names in first-seen order and occurrence counts."""
    names = sorted(set(items))
    return {"names": names, "counts": {name: items.count(name) for name in names}}
