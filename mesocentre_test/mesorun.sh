#!/bin/sh
#SBATCH -J Test1
#SBATCH -p skylake
#SBATCH -n 1
#SBATCH -A b126
#SBATCH -t 0:00:10
#SBATCH -o ./%j.%x.out
#SBATCH --mail-type=BEGIN,END
#SBATCH --mail-user=farinha96br@gmail.com

# load module python 3.6.3


#module purge
#module load userspace/all

g++ test2.cpp -lm 
srun ./a.out 5 
srun ./a.out 10 
srun ./a.out 15 
srun ./a.out 20 
