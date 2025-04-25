import random
import numpy as np
import matplotlib.pyplot as plt

def initialize_saw():
    """
    Initialize a saw of length L as a straight line.
    Returns:
        saw: List of tuples representing positions.
    """
    return [(0, 0)]

def is_SAW(saw):
    """
    Check if the polymer configuration is a self-avoiding walk (SAW).
    Returns:
        True if valid SAW, False otherwise.
    """
    return len(set(saw)) == len(saw)

def get_neighbors(pos):
    """get 4 neighbors"""
    x, y = pos
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

def grow_saw(saw):
    end = saw[-1]
    neighbors = get_neighbors(end)
    random.shuffle(neighbors)
    for new_pos in neighbors:
        if new_pos not in saw:
            return saw.append(new_pos)
    return None

def shrink_saw(saw):
    if len(saw) > 1:
        return saw[:-1]
    return saw

def metropolis_hasting_SAW(steps, mu):
    """
    Run a Metropolis Hasting simulation using the Metropolis algorithm with pivot moves.
    suppose the start of walk is fixed at origin point, and the movable end is denoted as I
      1. Randomly choose one of 4 neighboring vertices of I, i.e. I'.
      2. propose a symmetric update of the edge in between, which flips an empty edge to be occupied, and vice versa
    
    Returns:
        configurations: list of sampled SAW configurations after equilibration.
        acceptance_ratio: overall acceptance ratio
    """
    saw = initialize_saw()
    lengths = []
    
    for _ in range(steps):
        if random.random() < 0.5:
            # try growing saw
            new_saw = grow_saw(saw)
            if new_saw:
                accept_prob = min(1, 3 / mu)
                if random.random() < accept_prob:
                    saw = new_saw
        else:
            # try shrinking saw
            new_saw = shrink_saw(saw)
            accept_prob = min(1, mu / 3)    
            if random.random() < accept_prob:
                saw = new_saw

        lengths.append(len(saw))
    
    return lengths

# Run Grand Canonical sampling
steps = 100000
mu = 2.638  # priori μ
lengths = metropolis_hasting_SAW(steps, mu)

average_length = np.mean(lengths)
print(f"average SAW length: {average_length:.2f}")

# plot SAW length distribution
plt.hist(lengths, bins=50, density=True, alpha=0.7, color="blue")
plt.xlabel("SAW length")
plt.ylabel("frequency")
plt.title("SAW length distribution (Grand Canonical Sampling)")
plt.grid()
plt.show()
