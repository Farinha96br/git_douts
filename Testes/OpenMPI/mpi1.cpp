// Programa exemplo para paralelização usando MPI
// compilaçao com mpic++ -lm mpi.cpp
// execucão simples mpirun -np "n" ./a.out
// n é o numero de vezes q vai rodar (nao pode ser maior q o numero de threads)


#include <stdio.h>  // biblioteca padrão
#include <math.h>   // matematica
#include <mpi.h>


using namespace std;

int main(int argc, char** argv){
    printf("Program running \n");

    int process_Rank, size_Of_Cluster; // Variaveis pro indice do programa e do tamanho do cluster 

    MPI_Init(&argc, &argv); // Inicializa o MPI, nsei direi pq ele recebe esses role de argv e argc kkkk

    
    //MPI_Comm_size(MPI_COMM_WORLD, &size_Of_Cluster); // coloca o valor do tamanho do cluster (numero de nucleos)
    size_Of_Cluster = atoi(argv[1]);
    
    MPI_Comm_rank(MPI_COMM_WORLD, &process_Rank);    // rank do processo ou subprocesso

    
    for(int i = 0; i < size_Of_Cluster; i++){
        if(i == process_Rank){
            printf("Hello World from process %d of %d\n", process_Rank, size_Of_Cluster);
        }
        MPI_Barrier(MPI_COMM_WORLD); // Introduz uma barreira que faz com que todos os programas esperem chegar até aqui pra seguir juntos
    }


    MPI_Finalize(); // fecha o ambiente do MPI
    return 0;    
}

