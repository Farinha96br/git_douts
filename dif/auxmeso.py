# aruivo auxiliar para criação de headers e outras coisas para submissao ao mesocentre


def header():
    A = '# !Submittion!: sbatch ./bash_amu_mesocenter_submit.sh \n \
    #SBATCH -J Farinha               # job name \n \
    #SBATCH -p skylake               # partition to submit \n \
    #SBATCH -N 1                     # Number of nodes to use \n \
    #SBATCH -n 20                    # Number of cores per node \n \
    #SBATCH -t 0-00:30:00            # walltime (JJ-HH:MM:SS) - maximum of 7 days \n \
    #SBATCH -A b141                  # Project name to count CPU hours (b141) \n \
    #SBATCH -o %x.out                # Output file name \n \
    #SBATCH -e %x.err                # Error file name  \n \
    #SBATCH --mail-type=BEGIN,END    # Which stages shall SLURM send a message \n \
    #SBATCH --mail-user=farinh96br@gmail.com \n \
    module purge                          # unload modules \n \
    module load userspace/all             # load module space (all, custom, tr17.10) \n \
    module load gcc/11.2.0                # C/C++ compiler \n \
    module load openmpi/gcc112/psm2/4.0.5 # OpenMP library \n'
    return A


def comp_str():
    a = 'module purge                          # unload modules \n \
    module load userspace/all             # load module space (all, custom, tr17.10) \n \
    module load gcc/11.2.0                # C/C++ compiler \n \
    module load openmpi/gcc112/psm2/4.0.5 # OpenMP library ' 
    return a


def directory_stuff():
    a = 'WRKDIR=/scratch/$SLURM_JOB_USER/$SLURM_JOB_ID/ \n \
    echo "Working dir: $WRKDIR" \n \
    echo "Submission dir: $SLURM_SUBMIT_DIR" \n \
    echo "Job user: $SLURM_JOB_USER" \n \
    echo "Job ID: $SLURM_JOB_ID" \n \
    mkdir -p $WRKDIR \n \
    cd $WRKDIR'
    return a

def runpart():
    a = 'pwd \n \
    echo "CPUs on node: $SLURM_CPUS_ON_NODE" \n \
    bash bash_simulation.sh $SLURM_CPUS_ON_NODE \n \
    # Copy results \n \
    mkdir -p $SLURM_SUBMIT_DIR/ \n \
    cp -r $WRKDIR $SLURM_SUBMIT_DIR/ \n'
