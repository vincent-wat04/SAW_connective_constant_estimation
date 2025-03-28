import random
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def initialize_saw():
    return [(0, 0)]

def is_SAW(saw):
    return len(set(saw)) == len(saw)

def get_neighbors(pos):
    x, y = pos
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

def grow_saw(saw, delta_n=1):
    """尝试延长Δn步，返回新链或None"""
    new_saw = saw.copy()
    for _ in range(delta_n):
        end = new_saw[-1]
        neighbors = get_neighbors(end)
        random.shuffle(neighbors)
        for new_pos in neighbors:
            if new_pos not in new_saw:
                new_saw.append(new_pos)
                break
        else:
            return None  # 无法继续延长
    return new_saw

def shrink_saw(saw, delta_n=1):
    if len(saw) > delta_n:
        return saw[:-delta_n]
    return saw

def metropolis_hasting_SAW(steps, z, omega=1.0, max_delta_n=5):
    """
    Modified B-S-M algorithm with dynamic Δn adjustment.
    Parameters:
        z: 逸度 (控制平均链长)
        omega: 温度参数 (e^(ε/kT), 默认1.0对应SAW)
    """
    saw = initialize_saw()
    hist = {}  # 链长直方图
    
    for _ in range(steps):
        current_n = len(saw)
        
        # 动态调整Δn（简化实现）
        delta_n = random.randint(1, max_delta_n) if current_n > 50 else 1
        
        if random.random() < 0.5:
            # 尝试延长Δn步
            new_saw = grow_saw(saw, delta_n)
            if new_saw:
                new_n = len(new_saw)
                # 接受概率：公式(11)中的权重比
                accept_prob = min(1, (z**delta_n) * (omega**(new_n - current_n)) )
            else:
                new_saw = None
        else:
            # 尝试缩短Δn步
            new_saw = shrink_saw(saw, delta_n)
            new_n = len(new_saw)
            # 接受概率：权重比的倒数
            accept_prob = min(1, (z**(-delta_n)) * (omega**(new_n - current_n)) )
        
        # Metropolis准则
        if new_saw and (random.random() < accept_prob):
            saw = new_saw
        
        # 记录直方图
        n = len(saw)
        hist[n] = hist.get(n, 0) + 1
    
    return hist

# 拟合函数（高温度相分区函数形式）
def fit_func(n, mu_z, gamma):
    return (mu_z**n) * (n**(gamma-1))

def estimate_mu_z(hist):
    """通过非线性回归估计μ*z和γ"""
    n_values = np.array(sorted(hist.keys()))
    counts = np.array([hist[n] for n in n_values])
    counts = counts / np.sum(counts)  # 归一化
    
    # 初始猜测：μ*z ≈ 1, γ ≈ 1.16 (3D) 或 1.34 (2D)
    popt, pcov = curve_fit(fit_func, n_values, counts, p0=[1.0, 1.3])
    mu_z, gamma = popt
    return mu_z, gamma

# 参数设置
steps = 1000000
z = 0.3773  # 对应论文表1中ω=1.0的z值（2D）
omega = 1.0  # SAW对应无能量权重

# 运行模拟
hist = metropolis_hasting_SAW(steps, z, omega)

# 估计μ*z和γ
mu_z, gamma = estimate_mu_z(hist)
print(f"Estimated μ*z = {mu_z:.5f}, γ = {gamma:.3f}")

# 已知z时计算μ
mu_estimated = mu_z / z
print(f"Estimated μ = {mu_estimated:.5f} (真实值≈2.638)")

# 绘制直方图与拟合曲线
n_values = np.array(sorted(hist.keys()))
plt.bar(n_values, [hist[n]/steps for n in n_values], alpha=0.7, label='Simulation')
plt.plot(n_values, fit_func(n_values, mu_z, gamma), 'r-', label='Fit')
plt.xlabel("SAW length (n)")
plt.ylabel("Probability")
plt.title("SAW Length Distribution with Fit")
plt.legend()
plt.show()