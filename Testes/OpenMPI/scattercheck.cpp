#include <stdio.h>
#include <stdlib.h>

//#include <mpi.h>

int main(int argc, char** argv){

    int *a;
    // USAR CALLOC PRA FAZER O BLOCAO DE UMA VEZ
    a = (int*)calloc(1,sizeof(int));
    printf("%d\n",a[15]);
    

    //int process_Rank, size_Of_Comm;
    //int distro_Array[4] = {39, 72, 129, 42};
    //int scattered_Data;
//
    //MPI_Init(&argc, &argv);
    //MPI_Comm_size(MPI_COMM_WORLD, &size_Of_Comm);
    //MPI_Comm_rank(MPI_COMM_WORLD, &process_Rank);
//
    //MPI_Scatter(&distro_Array, 1, MPI_INT, &scattered_Data, 1, MPI_INT, 0, MPI_COMM_WORLD);
//
    //printf("Process %d has received: %d \n",process_Rank , scattered_Data);
    //MPI_Finalize();
return 0;
}



