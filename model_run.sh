#!/bin/bash
#SBATCH -J jupyter_gpu_1
#SBATCH -o jupyter_job_%j.out
#SBATCH -p gpu
#SBATCH -N 1
#SBATCH --gres=gpu:1
#SBATCH --mail-type=begin
#SBATCH --mail-user=constant.marks@unt.edu


printf "Jupyter Details\n"

module load tensorflow/2.1.0-gpu

unset XDG_RUNTIME_DIR
jupyter notebook --no-browser --ip=0.0.0.0
