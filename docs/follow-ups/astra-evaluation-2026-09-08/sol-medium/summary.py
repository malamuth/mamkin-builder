def summarize(items):
    """Return unique normalized names in first-seen order and occurrence counts."""
    names = []
    counts = {}

    for item in items:
        name = item.strip().casefold()
        if not name:
            continue
        if name not in counts:
            names.append(name)
            counts[name] = 0
        counts[name] += 1

    return {"names": names, "counts": counts}
