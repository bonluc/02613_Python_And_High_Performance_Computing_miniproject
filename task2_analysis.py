import re
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def parse_timing_file(path):
    N_values = []
    times = []
    
    with open(path, "r") as f:
        lines = f.readlines()
    
    current_real = None
    for line in lines:
        # Extract real time, e.g. "real    1m32.4s"
        match = re.match(r"real\s+(\d+)m([\d.]+)s", line)
        if match:
            minutes = int(match.group(1))
            seconds = float(match.group(2))
            current_real = minutes * 60 + seconds
        
        # Extract N, e.g. "N=10"
        match = re.match(r"N=(\d+)", line)
        if match and current_real is not None:
            N_values.append(int(match.group(1)))
            times.append(current_real)
            current_real = None
    
    return np.array(N_values), np.array(times)

N, times = parse_timing_file("timing_results.txt")

slope, intercept, r, p, se = stats.linregress(N, times)
print(f"Time per floor plan: {slope:.2f} s")
print(f"R²: {r**2:.4f}")

plt.plot(N, times, 'o', label='Measured')
plt.plot(N, slope * N + intercept, '--', label=f'Linear fit ({slope:.2f}s/plan)')
plt.xlabel("Number of floor plans")
plt.ylabel("Time (s)")
plt.legend()
plt.title("Scaling with number of floor plans")
plt.savefig("figures/task2_scaling.png")