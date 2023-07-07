#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>



int main(int argc, char** argv) {


    MPI_Init(&argc, &argv);
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    int its = 100;
    int N = size;


    // os dados locais um array
    //printf("rank %d\tarray: ",rank);
    int local_data[its];
    for (int j = 0; j < its; j++) {
        local_data[j] = its*rank + j; // Dados a serem enviados por cada processo
        //printf("%d ",local_data[j]);
    }
    //printf("\n");


    // parte de alocação de memoria
    int *global_data;
    if (rank == 0 ){
       global_data = (int*)malloc(its*size*sizeof(int)); // apenas o 1o processo ganha um pedaçao
    }
    else{
       global_data = (int*)malloc(2*2*sizeof(int)); // resto ganha pocalias apenas
    }
    
    MPI_Barrier(MPI_COMM_WORLD); // sincronia antes de juntar todos os dados

    // pega todos os dados
    MPI_Gather(local_data, its, MPI_INT,
            global_data, its, MPI_INT,
            0, MPI_COMM_WORLD);
  
    // sincronia por garantia
    MPI_Barrier(MPI_COMM_WORLD);
    


    // printa os valores 
    if (rank == 0 ){
        for (int i = 0; i < N; i++){
            for (int j = 0; j < its; j++){
                printf("%6d ",global_data[i*its + j]);
        }
        printf("\n");        
        }
    }


    MPI_Finalize();
    //free(global_data);
    return 0;
}