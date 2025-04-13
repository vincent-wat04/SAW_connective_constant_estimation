import random
import math
import matplotlib.pyplot as plt

def initialize_polymer(L):
    """
    Initialize a polymer of length L as a straight line.
    Returns:
        polymer: List of tuples representing positions.
    """
    return [(i, 0) for i in range(L + 1)]

def is_SAW(polymer):
    """
    Check if the polymer configuration is a self-avoiding walk (SAW).
    Returns:
        True if valid SAW, False otherwise.
    """
    return len(set(polymer)) == len(polymer)

def pivot_move(polymer):
    """
    Perform a pivot move on the polymer:
      1. Randomly choose a pivot index (not the first monomer).
      2. Randomly choose a rotation angle (90°, 180°, or 270°).
      3. Rotate the tail (monomers from the pivot onward) about the pivot.
    
    Returns:
        new_polymer: The new polymer configuration after the pivot move.
    """
    L = len(polymer) - 1
    pivot_index = random.randint(1, L)
    pivot_point = polymer[pivot_index]

    # Choose a random rotation angle (in radians)
    angle = random.choice([math.pi/2, math.pi, 3*math.pi/2])
    cos_theta = round(math.cos(angle))
    sin_theta = round(math.sin(angle))

    new_polymer = polymer[:pivot_index]  # Unchanged head of the chain
    for point in polymer[pivot_index:]:
        # Translate point relative to pivot
        dx = point[0] - pivot_point[0]
        dy = point[1] - pivot_point[1]
        # Apply rotation
        new_dx = cos_theta * dx - sin_theta * dy
        new_dy = sin_theta * dx + cos_theta * dy
        # Translate back
        new_polymer.append((pivot_point[0] + new_dx, pivot_point[1] + new_dy))
    
    return new_polymer

def metropolis_SAW(L, steps, equilibration=1000):
    """
    Run a canonical Monte Carlo simulation using the Metropolis algorithm with pivot moves.
    
    Parameters:
        L: polymer chain length (number of bonds)
        steps: total number of Monte Carlo steps.
        equilibration: number of steps to discard for equilibration.
        
    Returns:
        configurations: list of sampled SAW configurations after equilibration.
        acceptance_ratio: overall acceptance ratio.
    """
    polymer = initialize_polymer(L)
    accepted = 0
    configurations = []
    
    for step in range(steps):
        proposed = pivot_move(polymer)
        # Acceptance step: if proposed configuration is a valid SAW, accept it.
        if is_SAW(proposed):
            polymer = proposed
            accepted += 1
        # Record configurations after equilibration
        if step >= equilibration and step % 100 == 0:
            configurations.append(polymer.copy())
    
    acceptance_ratio = accepted / steps
    return configurations, acceptance_ratio