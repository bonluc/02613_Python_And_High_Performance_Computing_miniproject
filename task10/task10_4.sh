#!/bin/bash
#BSUB -J task10_4                              # Job name
#BSUB -o out_and_err/task10_4_%J.out
#BSUB -e out_and_err/task10_4_%J.err
#BSUB -q c02613
#BSUB -n 4
#BSUB -gpu "num=1:mode=exclusive_process"         # Request 1 GPU with exclusive access
#BSUB -R "rusage[mem=1G]"                         # Request GB of memory per core
#BSUB -R "span[hosts=1]"        
#BSUB -W 00:10                                    # Time limit
                                     # Time limit

cd ~/02613/MiniProject
mkdir -p out_and_err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

for N in $(seq 10 2 20); do
    { time python task10.py $N ; } 2>> task10_timing_results.txt
    echo "N=$N" >> task10_timing_results.txt
done
