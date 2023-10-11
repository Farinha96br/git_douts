#!/bin/sh 

#SBATCH -J aaaa
#SBATCH -p skylake
#SBATCH -A b336
#SBATCH -N 1
#SBATCH -n 32
#SBATCH -t 00:00:00 
#SBATCH --mail-type=END 
#SBATCH --mail-user=farinha96br@gmail.com

# purge environment modules
module purge
# set userspace and load modules
module load userspace/all
module load mpich/gcc72/psm2/3.2.1
module load boost/gcc72/openmpi/1.65.1
module load python3/3.8.6

mpic++ integrator_mpi.cpp -lm -lgsl
