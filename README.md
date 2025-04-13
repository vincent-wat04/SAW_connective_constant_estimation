# Self-Avoiding Walk (SAW) Sampling Algorithms and Connective Constant Estimation Toolkit (Under Active Development)

## Project Background
This repository implements advanced Monte Carlo methods for studying self-avoiding walks (SAWs), a fundamental model in polymer physics and statistical mechanics. The algorithms enable precise estimation of critical exponents (γ) and connective constants (μ) through:
- Naive Monte Carlo
- Rosenbluth Method (Importance Sampling)
- PERM (Pruned-Enriched Rosenbluth Method), both CPU and GPU-accelerated versions
- Pivot algorithms (Markov Chain Monte Carlo)
  - Canonical sampling techniques (Metropolis algorithm)
  - Grand canonical sampling techniques (Metropolis Hasting algorithm)

Key innovations include adaptive memory management, optimized collision detection, and parallelized sampling on GPU.

---

## Directory Structure

- `deterministic_cl.py`  
  Closed-form enumerations (used for validation)

### /naive_mc
- `naive_monte_carlo.py`  
  Basic SAW generator with O(μⁿ) attrition. Used as benchmark.
- `naive_mc_res_failure-at-30.png`  
  Visualization of exponential attrition (fails beyond L≈30)

### /pivot_algo
- `Pivot_algorithm.ipynb`  
  Jupyter notebook implementing 3 types of pivot algorithms efficient for connective constant estimation:  
  - Sampling using atmosphere as statistics
  - Telescoping method
  - Recursive method 
- `metropolis_algo.py`  
  Core Metropolis acceptance logic  

### /rosenbluth_to_PERM
- `basic_rosenbluth.py`  
  Original Rosenbluth method (1955) with weight accumulation  
- `Rosenbluth_to_PERM_CPU.ipynb`  
  CPU implementation featuring:  
  - Dynamic pruning/enrichment thresholds  
  - Recursive SAW-tree structures  
- `Rosenbluth_to_PERM_GPU.ipynb`  
  CUDA-accelerated version with:  
  - Adaptive local/global memory switching
  - Batch sampling
  - Grid-optimized collision detection (3x speedup)

---

## Key Features
- **Cross-platform** CPU/GPU implementations  
- **Modular design** for algorithm comparisons  
- **Visualization-ready** output formats  

---

## Usage
```bash
# GPU-PERM (requires CUDA)
python rosenbluth_to_PERM/Rosenbluth_to_perm_GPU.ipynb

# CPU benchmarks
python pivot_algo/metropolis_algo.py --length 100 --samples 1e6
```
