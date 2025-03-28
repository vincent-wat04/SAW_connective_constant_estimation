import random
import matplotlib.pyplot as plt

class NaiveMonteCarlo:

    def random_walk(self, L):
        """Generate a standard random walk of length L (without SAW restriction)."""
        pos = (0, 0)
        path = [pos]
        for _ in range(L):
            dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            pos = (pos[0] + dx, pos[1] + dy)
            path.append(pos)
        return path

    def is_SAW(self, path):
        """Check whether the given path is self-avoiding."""
        return len(set(path)) == len(path)

    def monte_carlo_I(self, L, trials=100000):
        valid = 0
        for _ in range(trials):
            path = self.random_walk(L)
            if self.is_SAW(path):
                valid += 1
        return valid / trials

# Example: Estimate the proportion of SAWs and connective constahnt mu among random walks for L = 20.
# SAW ratio = cL / 4^L, so cL = 4^L * SAW ratio
L = 20
naive_mc = NaiveMonteCarlo()
SAW_ratio = naive_mc.monte_carlo_I(L)
cL = 4**L * SAW_ratio
mu = cL**(1/L)
print(f"Naive Monte Carlo: L = {L}, estimated c_L ≈ {cL:.2f}, eatimated mu ≈ {mu:.6f}, SAW ratio ≈ {SAW_ratio:.6f}")

# draw a plot of the estimated SAW ratio and mu as a function of L
L_values = list(range(1, 31))
SAW_ratios = [NaiveMonteCarlo().monte_carlo_I(L) for L in L_values]
cL_values = [4**L * SAW_ratio for L, SAW_ratio in zip(L_values, SAW_ratios)]
mu_values = [cL**(1/L) for cL, L in zip(cL_values, L_values)]

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('L')
ax1.set_ylabel('SAW ratio', color=color)
ax1.plot(L_values, SAW_ratios, color=color, marker='o')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('mu', color=color)
ax2.plot(L_values, mu_values, color=color, marker='x')
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plt.title("Naive Monte Carlo: Estimated cL and mu")
plt.show()




