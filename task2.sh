#!/bin/bash
#BSUB -J task2                               # Job name
#BSUB -o out_and_err/task2%J.out
#BSUB -e out_and_err/task2%J.err
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

for N in $(seq 10 2 20); do
    { time python simulate.py $N ; } 2>> timing_results.txt
    echo "N=$N" >> task2_timing_results.txt
done
