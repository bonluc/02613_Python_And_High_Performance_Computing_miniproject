from os.path import join
import sys

import numpy as np
import multiprocessing as mp
import matplotlib.pyplot as plt
from time import perf_counter as time
from numba import cuda



def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask

@cuda.jit
def jacobi_CUDA_kernel(u,u_out,int_mask):
    j,i=cuda.grid(2)


    if i< int_mask.shape[0] and j < int_mask.shape[1]:
        if int_mask[i,j]==1:
            u_out[i+1,j+1]=0.25*(u[i+1,j]+u[i+1,j+2]+u[i,j+1]+u[i+2,j+1])
        else:
            u_out[i+1,j+1]=u[i+1,j+1]





def jacobi_CUDA_helper(u, interior_mask, max_iter, TPB):
    u = np.copy(u)
    d_u = cuda.to_device(u)
    d_u_out=cuda.to_device(u)

    blockspergrid_x = (interior_mask.shape[0]+TPB[0]-1) // TPB[0]
    blockspergrid_y = (interior_mask.shape[1]+TPB[1]-1) // TPB[1]
    blockspergrid = (blockspergrid_x, blockspergrid_y)

    d_int_mask=cuda.to_device(interior_mask)


    for i in range(max_iter):
        # Compute average of left, right, up and down neighbors, see eq. (1)
        jacobi_CUDA_kernel[blockspergrid,TPB](d_u,d_u_out,d_int_mask)
        d_u,d_u_out = d_u_out, d_u

    cuda.synchronize()

    return d_u_out.copy_to_host()

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
    threadsperblock=(32,32)

    blockspergrid_x = (all_interior_mask[0].shape[0]+threadsperblock[0]-1) // threadsperblock[0]
    blockspergrid_y = (all_interior_mask[0].shape[1]+threadsperblock[1]-1) // threadsperblock[1]
    blockspergrid = (blockspergrid_x, blockspergrid_y)
    d_u0_comp = cuda.to_device(all_u0[0])
    d_u0_out_comp= cuda.to_device(all_u0[0])
    d_int_mask_comp = cuda.to_device(all_interior_mask[0])
    jacobi_CUDA_kernel[blockspergrid,threadsperblock](d_u0_comp,d_u0_out_comp,d_int_mask_comp)

    all_u=np.empty_like(all_u0)
    for i, (u0, interior_mask) in enumerate(zip(all_u0,all_interior_mask)):
        all_u[i]=jacobi_CUDA_helper(u0,interior_mask,MAX_ITER, threadsperblock)

    # Print summary statistics in CSV format
    """stat_keys = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
    print('building_id, ' + ', '.join(stat_keys))  # CSV header
    for bid, u, interior_mask in zip(building_ids, all_u, all_interior_mask):
        stats = summary_stats(u, interior_mask)
        print(f"{bid},", ", ".join(str(stats[k]) for k in stat_keys))"""