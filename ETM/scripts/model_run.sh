#!/bin/bash
#SBATCH -J data_process
#SBATCH -o data_process%j.out
#SBATCH -p bigmem
#SBATCH --qos general
#SBATCH -N 1
#SBATCH --mail-type=begin
#SBATCH --mail-user=constant.marks@unt.edu


printf "data processing\n"

module load pytorch
pip install sklearn --user

python data_reddit.py

unset XDG_RUNTIME_DIR
jupyter notebook --no-browser --ip=0.0.0.0
