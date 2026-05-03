from os.path import join
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numba import cuda



def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask

@cuda.jit
def jacobi_CUDA_kernel(u,u_out,int_mask):
    j,i,b=cuda.grid(3)

    if b< int_mask.shape[0] and  i< int_mask.shape[1] and j < int_mask.shape[2]:
        if int_mask[b,i,j]==1:
            u_out[b,i+1,j+1]=0.25*(u[b,i+1,j]+u[b,i+1,j+2]+u[b,i,j+1]+u[b,i+2,j+1])


def jacobi_CUDA_helper(u, interior_mask, max_iter,TPB):
    batch_size=500
    N_bid = u.shape[0]
    all_u = np.empty_like(u)
    for start in range(0,N_bid,batch_size):
        end = min(start+batch_size,N_bid)
        d_u=cuda.to_device(u[start:end])
        d_u_out=cuda.to_device(u[start:end])
        B,H,W = interior_mask[start:end].shape

        d_int_mask=cuda.to_device(interior_mask[start:end])
        BPG = ((W + TPB[0] - 1) // TPB[0], (H + TPB[1] - 1) // TPB[1], B)

        for i in range(max_iter):
            jacobi_CUDA_kernel[BPG,TPB](d_u,d_u_out,d_int_mask)
            d_u,d_u_out = d_u_out, d_u
        
        cuda.synchronize()
        all_u[start:end] = d_u.copy_to_host()

    return all_u

def summary_stats(u, interior_mask):
    u_interior = u[1:-1, 1:-1][interior_mask]
    mean_temp = u_interior.mean()
    std_temp = u_interior.std()
    pct_above_18 = np.sum(u_interior > 18) / u_interior.size * 100
    pct_below_15 = np.sum(u_interior < 15) / u_interior.size * 100
    return {
        'mean_temp': mean_temp,
        'std_temp': std_temp,
        'pct_above_18': pct_above_18,
        'pct_below_15': pct_below_15,
    }


if __name__ == '__main__':
    
    # Load data
    LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
    with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
        building_ids = f.read().splitlines()

    if len(sys.argv) < 2:
        N = 1
    else:
        N = int(sys.argv[1])
    building_ids = building_ids[:N]


    # Load floor plans
    all_u0 = np.empty((N, 514, 514))
    all_interior_mask = np.empty((N, 512, 512), dtype='bool')
    for i, bid in enumerate(building_ids):
        u0, interior_mask = load_data(LOAD_DIR, bid)
        all_u0[i] = u0
        all_interior_mask[i] = interior_mask

    MAX_ITER = 20_000
    threadsperblock=(32,32,1)
    
    all_u=jacobi_CUDA_helper(all_u0,all_interior_mask,MAX_ITER,threadsperblock)

    rows = []
    for bid, u, interior_mask in zip(building_ids, all_u, all_interior_mask):
        stats = summary_stats(u, interior_mask)
        row = {
            'building_id': bid,
            'mean_temp': stats['mean_temp'],
            'std_temp': stats['std_temp'],
            'pct_above_18': stats['pct_above_18'],
            'pct_below_15': stats['pct_below_15'],
        }
        rows.append(row)
    df = pd.DataFrame(rows)

    #df.to_csv('results.csv', index=False)

    print(f'Total Buildings: {len(df)}')
    #average of the mean temperatures across buildings
    print(f'Average Mean Temperature: {df["mean_temp"].mean():.2f} °C')
    #standard deviation of mean temperatures across buildings
    print(f'Standard Deviation of Mean Temperatures: {df["mean_temp"].std():.2f} °C')
    #average of the temperature standard deviation
    print(f'Average of the Temperature Standard Deviation: {df["std_temp"].mean():.2f} °C')
    # count how many building have at least 50 % of interior above 18 °C
    count_above_18 = (df['pct_above_18'] >= 50).sum()
    print(f'Number of Buildings with at least 50% interior above 18 °C: {count_above_18}')
    # count how many building have at least 50 % of interior below 15 °C
    count_below_15 = (df['pct_below_15'] >= 50).sum()
    print(f'Number of Buildings with at least 50% interior below 15 °C: {count_below_15}')
    # plotting the distribution of mean temperatures across buildings
    plt.hist(df['mean_temp'], bins=20)
    plt.xlabel('Mean Temperature (°C)')
    plt.ylabel('Number of Buildings')
    plt.title('Distribution of Mean Temperatures Across Buildings')
    plt.savefig('task12_mean_temperature_distribution.png')
    plt.close()
