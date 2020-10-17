#!/bin/bash
#SBATCH -J ETM
#SBATCH -o ETM_%j.out
#SBATCH -p gpu
#SBATCH -N 1
#SBATCH --gres=gpu:1
#SBATCH --mail-type=begin
#SBATCH --mail-user=constant.marks@unt.edu


printf "model run\n"

module load pytorch
pip install sklearn --user

python main.py --mode train --dataset reddit --data_path data/reddit --num_topics 50 --emb_path embeddings.txt --train_embeddings 0 --epochs 100


