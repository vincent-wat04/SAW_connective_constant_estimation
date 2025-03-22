import random

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

# Example: Estimate the proportion of SAWs among random walks for L = 20.
# SAW ratio = cL / 4^L, so cL = 4^L * SAW ratio
L = 20
ratio_I = NaiveMonteCarlo.monte_carlo_I(L, trials=100000)
cL = 4**L * ratio_I
print(f"Monte Carlo I: L = {L}, SAW ratio ≈ {ratio_I:.6f}, estimated c_L ≈ {cL:.2f}")
