#!/bin/bash
#BSUB -J task10_2_                              # Job name
#BSUB -o out_and_err/task10_2_%J.out
#BSUB -e out_and_err/task10_2_%J.err
#BSUB -q c02613
#BSUB -n 4
#BSUB -gpu "num=1:mode=exclusive_process"         # Request 1 GPU with exclusive access
#BSUB -R "rusage[mem=1G]"                         # Request GB of memory per core
#BSUB -R "span[hosts=1]"        
#BSUB -W 00:03                                    # Time limit

cd ~/02613/MiniProject
mkdir -p out_and_err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

time python task9.py 20 

time python task10.py 20 
