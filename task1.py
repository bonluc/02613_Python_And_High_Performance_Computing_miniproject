import numpy as np
import matplotlib.pyplot as plt
from os.path import join


LOAD_DIR = r'/dtu/projects/02613_2025/data/modified_swiss_dwellings/'    
N_PLANS  = 3

def load_data(load_dir, bid):
    domain   = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior = np.load(join(load_dir, f"{bid}_interior.npy"))
    return domain, interior


def visualize(building_ids, load_dir):
    n = len(building_ids)
    fig, axes = plt.subplots(n, 3, figsize=(14, 4.5 * n),
                             gridspec_kw={"wspace": 0.1, "hspace": 0.4})
    if n == 1:
        axes = [axes]

    fig.suptitle("Modified Swiss Dwellings — Floor Plan Visualization",
                 fontsize=14, fontweight="bold", y=1.01)

    for row, bid in enumerate(building_ids):
        domain, interior = load_data(load_dir, bid)
        ax1, ax2, ax3 = axes[row]

        # Interior mask walls (True) vs. room (False)
        ax1.imshow(interior, cmap="binary_r", interpolation="nearest")
        ax1.set_title(f"[{bid}]\nWalls vs. Room", fontsize=10, fontweight="bold")
        ax1.axis("off")

        # Boundary temperatures 
        # Mask out zero pixels so only boundary temps are visible
        masked_domain = np.ma.masked_where(domain == 0, domain)
        ax2.imshow(interior, cmap="binary_r", interpolation="nearest", alpha=0.2)
        im = ax2.imshow(masked_domain, cmap="RdYlBu_r", interpolation="nearest",
                        vmin=0, vmax=30)
        ax2.set_title("Boundary Temperatures", fontsize=10, fontweight="bold")
        ax2.axis("off")
        plt.colorbar(im, ax=ax2, fraction=0.046, pad=0.04, label="°C")

        #Combined overview
        # Build an RGB image showing walls, room air, hot and cold boundaries
        display = np.zeros((*domain.shape, 3))
        display[~interior]    = [0.2, 0.2, 0.2]   # walls = dark gray
        display[interior]     = [0.85, 0.92, 1.0]  # room air = light blue
        display[domain == 25] = [1.0, 0.3, 0.1]    # hot wall = red
        display[domain == 5]  = [0.1, 0.4, 1.0]    # cold wall = blue

        ax3.imshow(display, interpolation="nearest")
        ax3.set_title("Overview\n(red=hot wall, blue=cold wall, light=room air)",
                      fontsize=10, fontweight="bold")
        ax3.axis("off")

    plt.tight_layout()
    out = "task1_floorplan_visualization.png"
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    print(f"Saved -> {out}")
    #plt.show()


if __name__ == "__main__":
    with open(join(LOAD_DIR, "building_ids.txt"), "r") as f:
        building_ids = f.read().splitlines()[:N_PLANS]

    print(f"Visualizing {len(building_ids)} floor plans: {building_ids}")
    visualize(building_ids, LOAD_DIR)