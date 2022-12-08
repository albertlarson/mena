#!/bin/bash
#SBATCH --partition=cpu
#SBATCH --time=24:00:00
#SBATCH --gpus=0
#SBATCH --cpus-per-task=1
#SBATCH --job-name=v20_daily_to_monthly
#SBATCH --mem=16000
#SBATCH -o job-%j.out  # %j = job ID

module load python
module load miniconda
source activate sm

python -u v20_daily_to_monthly.py  > v20_daily_to_monthly.out 