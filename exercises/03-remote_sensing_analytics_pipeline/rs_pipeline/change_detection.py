"""Basic land-cover change detection."""

def change_map(before, after):
    if before.shape != after.shape:
        raise ValueError("Input class maps must have the same shape.")
    return (before != after).astype("uint8")

def transition_matrix(before, after):
    if before.shape != after.shape:
        raise ValueError("Input class maps must have the same shape.")
    transitions = {}
    for b, a in zip(before.ravel(), after.ravel()):
        if b == 0 or a == 0:
            continue
        key = f"{int(b)}->{int(a)}"
        transitions[key] = transitions.get(key, 0) + 1
    return transitions
