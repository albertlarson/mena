#!/bin/bash
#SBATCH --partition=cpu-preempt
#SBATCH --time=24:00:00
#SBATCH --gpus=0
#SBATCH --cpus-per-task=1
#SBATCH --job-name=gldas_download
#SBATCH --mem=32000
#SBATCH -o job-%j.out  # %j = job ID

module load python
module load miniconda
source activate sm

python -u gldas_dl.py  > gldas_dl.out 
