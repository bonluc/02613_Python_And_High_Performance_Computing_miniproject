#!/bin/bash
#BSUB -J task4                              # Job name
#BSUB -o out_and_err/task4%J.out
#BSUB -e out_and_err/task4%J.err
#BSUB -q hpc
#BSUB -n 1
#BSUB -R "rusage[mem=1G]"                          # Request GB of memory per core
#BSUB -R "span[hosts=1]"        
#BSUB -R "select[model==XeonGold6226R]"
#BSUB -W 01:00                                       # Time limit

cd ~/02613_high_performance_computing/autolab/mini_project2
mkdir -p out_and_err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

kernprof -l -v task4.py 1

