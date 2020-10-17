#!/bin/bash
#SBATCH -J jupyter_gpu_1
#SBATCH -o jupyter_job_%j.out
#SBATCH -p gpu
#SBATCH -N 1
#SBATCH --gres=gpu:1
#SBATCH --mail-type=begin
#SBATCH --mail-user=constant.marks@unt.edu


printf "model run\n"
module load pytorch
pip install sklearn --user

module python main.py --mode train --dataset reddit --data_path data/reddit --num_topics 50 --train_embeddings 1 --epochs 10


