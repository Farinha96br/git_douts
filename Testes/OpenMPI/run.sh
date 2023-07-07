#!/bin/sh
#SBATCH -J Job_skylake
#SBATCH -p skylake
#SBATCH -N 2
#SBATCH -n 32
#SBATCH -A b001
#SBATCH -t 2-12
#SBATCH -o .%j.out
#SBATCH -e .%j.err
#SBATCH --mail-type=BEGIN,END
#SBATCH --mail-user=your@mail.address

# chargement des modules
module purge
module load userspace/all
module load openmpi/2.1.2/2018
# moving to the working directory

mpirun mpi3.cpp
