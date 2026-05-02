#!/bin/bash
#BSUB -q c02613
#BSUB -J task8
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=1GB]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -W 00:15

#BSUB -o task8_%J.out
#BSUB -e task8_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

for N in $(seq 10 2 20); do
    { time python task8.py $N ; } 2>> task8_timing_results.txt
    echo "N=$N" >> task8_timing_results.txt
done
