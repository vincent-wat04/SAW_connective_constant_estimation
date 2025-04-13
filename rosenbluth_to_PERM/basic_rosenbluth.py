import random
import matplotlib.pyplot as plt

def generate_SAW_Rosenbluth(L):
    """
    Generate a self-avoiding walk (SAW) of length L using the Rosenbluth algorithm.
    
    Returns:
        path (list): The generated SAW as a list of positions.
        weight (int): The Rosenbluth weight associated with this path.
    """
    pos = (0, 0)
    path = [pos]
    weight = 1
    visited = {pos}
    for _ in range(L):
        # Find all valid (unvisited) neighbors.
        valid_neighbors = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            newpos = (pos[0] + dx, pos[1] + dy)
            if newpos not in visited:
                valid_neighbors.append(newpos)
        m = len(valid_neighbors)
        if m == 0:
            # Walk is trapped; return current path with weight zero.
            return path, weight * 0
        weight *= m  # Update weight (Equation (7))
        pos = random.choice(valid_neighbors)
        visited.add(pos)
        path.append(pos)
    return path, weight

def monte_carlo_II(L, trials=100000):
    total_weight = 0
    success_count = 0
    for _ in range(trials):
        path, weight = generate_SAW_Rosenbluth(L)
        total_weight += weight
        if weight > 0:
            success_count += 1
    # The average weight is an unbiased estimator for c_L (Equation (11)).
    return total_weight / trials, success_count / trials

# Example: Estimate c_L and the success ratio for L = 20 using the Rosenbluth algorithm.
L = 20
estimated_cL, success_ratio = monte_carlo_II(L, trials=100000)
mu = estimated_cL**(1/L)
print(f"Monte Carlo II (Rosenbluth): L = {L}, estimated c_L ≈ {estimated_cL:.2f}, eatimated mu ≈ {mu:.6f}, success ratio ≈ {success_ratio:.6f}")

# Draw a plot of the estimated mu and success ratio as a function of L.
L_values = list(range(1, 31))
mu_values = []
success_ratios = []
for L in L_values:
    # Perform Monte Carlo simulation for each L with 100,000 trials.
    estimated_cL, success_ratio = monte_carlo_II(L, trials=100000)
    mu = estimated_cL**(1/L)
    mu_values.append(mu)
    success_ratios.append(success_ratio)

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('L')
ax1.set_ylabel('Success ratio', color=color)
ax1.plot(L_values, success_ratios, color=color, marker='o')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('mu', color=color)
ax2.plot(L_values, mu_values, color=color, marker='x')
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plt.title("Monte Carlo II (Rosenbluth): Estimated cL and mu")
plt.show()
