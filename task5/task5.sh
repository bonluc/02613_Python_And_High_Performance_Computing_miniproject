#!/bin/bash
#BSUB -J task5
#BSUB -o out_and_err/task5_%J.out
#BSUB -e out_and_err/task5_%J.err
#BSUB -q hpc
#BSUB -n 20
#BSUB -R "rusage[mem=2G]"
#BSUB -R "span[hosts=1]"
#BSUB -W 01:00

# Ensure we are in the correct directory
cd /zhome/47/9/223816/home/02613_Python_And_High_Performance_Computing_miniproject

# Load conda environment
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

# Run the parallel script
python -u task5.py 20
