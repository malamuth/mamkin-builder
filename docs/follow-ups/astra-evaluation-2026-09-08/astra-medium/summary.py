def summarize(items):
    """Return unique normalized names in first-seen order and occurrence counts."""
    counts = {}
    for item in items:
        name = item.strip().casefold()
        if name:
            counts[name] = counts.get(name, 0) + 1
    return {"names": list(counts), "counts": counts}
