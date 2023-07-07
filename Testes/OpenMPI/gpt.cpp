#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int send_data = rank; // Dados a serem enviados por cada processo
    int* recv_data = NULL;    // Dados a serem recebidos pelo processo raiz

    if (rank == 0) {
        recv_data = (int*)malloc(size * sizeof(int)); // Alocar memória para receber dados
    }

    MPI_Gather(&send_data, 1, MPI_INT, recv_data, 1, MPI_INT, 0, MPI_COMM_WORLD);

    if (rank == 0) {
        printf("Processo raiz (rank %d) recebeu os seguintes dados:\n", rank);
        for (int i = 0; i < size; i++) {
            printf("%d ", recv_data[i]);
        }
        printf("\n");
        free(recv_data); // Liberar memória alocada para receber dados
    }

    MPI_Finalize();

    return 0;
}