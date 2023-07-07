// Programa exemplo para paralelização usando MPI, como fazer os processos se comunicarem
// compilaçao com mpic++ -lm mpi.cpp
// execucão simples mpirun -np "n" ./a.out
// n é o numero de vezes q vai rodar (nao pode ser maior q o numero de threads)

// Detalhes sobre como as funçoes de enviar e receber foram utilizadas:
/*

MPI_Send(
    &message_Item,      //Address of the message we are sending.
    1,                  //Number of elements handled by that address.
    MPI_INT,            //MPI_TYPE of the message we are sending.
    1,                  //Rank of receiving process
    1,                  //Message Tag
    MPI_COMM_WORLD      //MPI Communicator
);

MPI_Recv(
    &message_Item,      //Address of the message we are receiving.
    1,                  //Number of elements handled by that address.
    MPI_INT,            //MPI_TYPE of the message we are sending.
    0,                  //Rank of sending process
    1,                  //Message Tag
    MPI_COMM_WORLD      //MPI Communicator
    MPI_STATUS_IGNORE   //MPI Status Object
);
*/


#include <stdio.h>  // biblioteca padrão
#include <math.h>   // matematica
#include <mpi.h>


using namespace std;

int main(int argc, char** argv){
    printf("Program running \n");

    int process_Rank, size_Of_Cluster; // Variaveis pro indice do programa e do tamanho do cluster 
    int message_Item; // valor a ser transferido 

    MPI_Init(&argc, &argv); // Inicializa o MPI, nsei direi pq ele recebe esses role de argv e argc kkkk

    MPI_Comm_size(MPI_COMM_WORLD, &size_Of_Cluster); // coloca o valor do tamanho do cluster (numero de nucleos)
    MPI_Comm_rank(MPI_COMM_WORLD, &process_Rank);    // rank do processo ou subprocesso

    
    if(process_Rank == 0){
        message_Item = 42;
        MPI_Send(&message_Item, 1, MPI_INT, 1, 1, MPI_COMM_WORLD);
        printf("Sending message containing: %d\n", message_Item);
    }
    else if(process_Rank == 1){
        MPI_Recv(&message_Item, 1, MPI_INT, 0, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        printf("Received message containing: %d\n", message_Item);
    }


    MPI_Finalize(); // fecha o ambiente do MPI
    return 0;    
}

