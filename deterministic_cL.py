def count_SAW(L, pos=(0, 0), visited=None):
    """
    Recursively count the number of self-avoiding walks (SAWs) of length L.
    
    Parameters:
        L (int): remaining steps.
        pos (tuple): current position (default is the origin).
        visited (set): set of visited positions.
        
    Returns:
        int: number of SAWs from this state.
    """
    if visited is None:
        visited = {pos}
    if L == 0:
        return 1
    total = 0
    # Four possible directions: right, left, up, down.
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        newpos = (pos[0] + dx, pos[1] + dy)
        if newpos not in visited:
            total += count_SAW(L - 1, newpos, visited | {newpos})
    return total

# Compute c_L for L = 1 to 20.
deterministic_counts = {}
for L in range(1, 21):
    deterministic_counts[L] = count_SAW(L)
    print(f"Deterministic: L = {L}, c_L = {deterministic_counts[L]}")