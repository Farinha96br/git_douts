#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <boost/numeric/odeint.hpp>

using namespace std;





int main(int argc, char** argv) {
   MPI_Init(&argc, &argv);
   //double var = atof(argv[6]);

   int rank, size;
   
   MPI_Comm_rank(MPI_COMM_WORLD, &rank);
   MPI_Comm_size(MPI_COMM_WORLD, &size);

   int its = 10;
   // Inicialização e distribuiçao de cond. iniciais
   double *x0s;
   double *y0s;
   double *global_x; // array final do resultado
   double *global_y; // array final do resultado


   // alocação de memoria do master (rank 0)
   if (rank == 0 ){
      x0s = (double*)malloc(size*sizeof(double)); // apenas o 1o processo ganha um pedaçao
      y0s = (double*)malloc(size*sizeof(double)); // apenas o 1o processo ganha um pedaçao
      global_x = (double*)malloc(its*size*sizeof(double)); // apenas o 1o processo ganha um pedaçao
      global_y = (double*)malloc(its*size*sizeof(double)); // apenas o 1o processo ganha um pedaçao

      x0s[0] = 0.1;
      x0s[1] = 0.2;
      y0s[0] = 0.3;
      y0s[1] = 0.4;
   }
   // alocação nos subprocessos
   else{
      x0s = (double*)malloc(1*sizeof(double)); // resto ganha pocalias apenas
      y0s = (double*)malloc(1*sizeof(double)); // resto ganha pocalias apenas
      global_x = (double*)malloc(2*1*sizeof(double)); // resto ganha pocalias apenas
      global_y = (double*)malloc(2*1*sizeof(double)); // resto ganha pocalias apenas
   }

   



   // distribui as cond. iniciais
   double x0;
   double y0;
   MPI_Barrier(MPI_COMM_WORLD); // garante q tudo foi alocado e lido certinho    
   MPI_Scatter(x0s, 1, MPI_DOUBLE, &x0, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
   MPI_Scatter(y0s, 1, MPI_DOUBLE, &y0, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
   
	//printf(" rank %d %lf: \n",rank,x0) ;
   // memoria para x(t) e y(t)
   double *xts = (double*)malloc(its*size*sizeof(double));
   double *yts = (double*)malloc(its*size*sizeof(double));

	int c = 0;
   while (t < tf){    
      if ((t > c*strobe - step/2) && (t < c*strobe + step/2)){
   		//printf(" rank:%d x[0]: %lf: \n",rank,x[0]) ;
         xts[c] = x[0];
			yts[c] = x[1];
			c++;
      }
      stepper.do_step(mysyst, x, t, step);  
      t += step;
    }



   MPI_Barrier(MPI_COMM_WORLD); // sincronia antes de juntar todos os dados

   //pega todos os dados
   MPI_Gather(xts, its, MPI_DOUBLE,
            global_x, its, MPI_DOUBLE,
            0, MPI_COMM_WORLD);

   MPI_Barrier(MPI_COMM_WORLD); // sincronia antes de juntar todos os dados

   MPI_Finalize();
   //free(global_data);
   return 0;
}