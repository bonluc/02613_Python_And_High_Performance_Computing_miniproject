from os.path import join
import numpy as np
import matplotlib.pyplot as plt

def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask

def jacobi(u, interior_mask, max_iter, atol=1e-4):
    u = np.copy(u)
    for i in range(max_iter):
        u_new = 0.25 * (u[1:-1, :-2] + u[1:-1, 2:] + u[:-2, 1:-1] + u[2:, 1:-1])
        u_new_interior = u_new[interior_mask]
        delta = np.abs(u[1:-1, 1:-1][interior_mask] - u_new_interior).max()
        u[1:-1, 1:-1][interior_mask] = u_new_interior
        if delta < atol:
            break
    return u

LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'

with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
    building_ids = f.read().splitlines()[:3]

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for ax, bid in zip(axes, building_ids):
    u0, interior_mask = load_data(LOAD_DIR, bid)
    u = jacobi(u0, interior_mask, max_iter=20_000)

    # Mask out walls so only interior air is shown
    result = np.where(interior_mask, u[1:-1, 1:-1], np.nan)

    im = ax.imshow(result, cmap='RdYlBu_r', interpolation='nearest', vmin=5, vmax=25)
    ax.set_title(f"Building {bid}")
    ax.axis('off')
    plt.colorbar(im, ax=ax, label='°C')

plt.suptitle("Heat distribution after Jacobi convergence", fontweight='bold')
plt.tight_layout()
plt.savefig("figures/task3_heat_results.png", dpi=150, bbox_inches='tight')