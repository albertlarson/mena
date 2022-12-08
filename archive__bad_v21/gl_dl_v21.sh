#!/bin/bash
#SBATCH --partition=gpu
#SBATCH --time=24:00:00
#SBATCH --gpus=1
#SBATCH --cpus-per-task=1
#SBATCH --job-name=gldas_download
#SBATCH --mem=16000
#SBATCH -o job-%j.out  # %j = job ID

module load python
module load miniconda
source activate sm

python -u gl_dl_v22.py  > gl_dl_v22__day2.out 
