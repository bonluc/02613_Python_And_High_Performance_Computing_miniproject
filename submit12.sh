#!/bin/bash
#BSUB -q c02613
#BSUB -J Task12
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=7GB]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -W 00:30
#BSUB -o Task12_%J.out
#BSUB -e Task12_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

time python task12.py 4571