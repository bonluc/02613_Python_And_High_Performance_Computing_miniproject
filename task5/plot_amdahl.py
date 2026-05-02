import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

def amdahl_law(n, p):
    """
    Amdahl's Law function for curve fitting.
    n: Number of processors/cores
    p: Parallel fraction of the code
    """
    return 1 / ((1 - p) + (p / n))

def main():
    csv_file = 'task5/amdahl_data.csv'
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found. Please run the simulation first.")
        return

    # 1. Load the data
    print(f"Reading data from {csv_file}...")
    df = pd.read_csv(csv_file)
    
    # Handle different possible column names
    num_cores_col = 'num_workers' if 'num_workers' in df.columns else 'Number of Cores'
    duration_col = 'duration' if 'duration' in df.columns else 'Duration in s'
    
    num_cores = df[num_cores_col].values
    durations = df[duration_col].values

    # 2. Calculate Speed-up
    # Speed-up = Time(1 core) / Time(N cores)
    t_serial = durations[0]
    speed_up = t_serial / durations

    # 3. Fit the curve to find the parallel fraction 'p'
    print("Fitting Amdahl's Law curve...")
    try:
        p_opt, _ = curve_fit(amdahl_law, num_cores, speed_up, p0=[0.9], bounds=(0, 1))
        p = p_opt[0]
        print(f"Estimated parallel fraction (p): {p:.4f}")
    except Exception as e:
        print(f"Warning: Could not fit curve: {e}")
        p = None

    # 4. Create the Plot
    plt.figure(figsize=(10, 6))
    plt.plot(num_cores, speed_up, 'o', label='Measured Speed-up', color='#1f77b4', markersize=8)
    plt.plot(num_cores, num_cores, '--', label='Ideal Scaling (Linear)', color='gray', alpha=0.5)

    if p is not None:
        # Plot the fitted Amdahl curve
        n_smooth = np.linspace(1, max(num_cores), 100)
        plt.plot(n_smooth, amdahl_law(n_smooth, p), '-', 
                 label=f"Amdahl's Law Fit (p={p:.3f})", color='#d62728', linewidth=2)
        
        # Theoretical maximum speed-up
        max_speedup = 1 / (1 - p)
        plt.axhline(y=max_speedup, color='#2ca02c', linestyle=':', 
                    label=f"Theoretical Max Speed-up ({max_speedup:.2f}x)")

    plt.title("Amdahl's Law Analysis: Scaling Performance", fontsize=14)
    plt.xlabel("Number of Cores", fontsize=12)
    plt.ylabel("Speed-up", fontsize=12)
    
    # Force integer ticks on the x-axis
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.6)

    # Save the figure
    output_plot = 'figures/amdahl_plot.png'
    os.makedirs('figures', exist_ok=True)
    plt.savefig(output_plot, dpi=300, bbox_inches='tight')
    print(f"Plot saved as {output_plot}")
    plt.close()

if __name__ == '__main__':
    main()
