#!/bin/bash

#BSUB -J python
#BSUB -q hpc
#BSUB -W 25
#BSUB -R "rusage[mem=512MB]"
#BSUB -n 20
#BSUB -R "span[hosts=1]"
#BSUB -o python_%J.out
#BSUB -e python_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026


python task6.py 50

