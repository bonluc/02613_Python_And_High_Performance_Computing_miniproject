#!/bin/bash
#BSUB -J task12                             # Job name
#BSUB -o out_and_err/task12%J.out
#BSUB -e out_and_err/task12%J.err
#BSUB -q gpuv100
#BSUB -n 4
#BSUB -gpu "num=1:mode=exclusive_process"         # Request 1 GPU with exclusive access
#BSUB -R "rusage[mem=1G]"                         # Request GB of memory per core
#BSUB -R "span[hosts=1]"        
#BSUB -W 04:00                                    # Time limit
                                    

cd ~/02613_high_performance_computing/autolab/mini_project2
mkdir -p out_and_err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

python task12.py 4571
