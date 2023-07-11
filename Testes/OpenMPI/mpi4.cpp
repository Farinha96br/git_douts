#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <boost/numeric/odeint.hpp>

using namespace boost::numeric::odeint;
using namespace std;

typedef boost::array< double , 2 > state_type; 

// Inicializa as variaveis do sisema, amplitudes, frequencias etc...
array<double,2> A;
array<double,2> w;
array<double,2> kx;
array<double,2> ky;
array<double,2> phasex;
double v;
double U;
double t;
// função pra printar o role
double strobe; // estrobo pra quanto tem só duas ondas
double step = 0.001; // define o passo temporal


void mysyst( const state_type &x , state_type &dxdt , double t ){
    // sistemas de EDO pra integrar no tempo
    // na direção x
    dxdt[0] =   -A[0]*ky[0]*sin(kx[0]*x[0] + phasex[0])*cos(ky[0]*x[1]) -
                 A[1]*ky[1]*sin(kx[1]*x[0] + phasex[1])*cos(ky[1]*(x[1]-v*t));


    // na direçao y
    dxdt[1] =   A[0]*kx[0]*cos(kx[0]*x[0] + phasex[0])*sin(ky[0]*x[1]) +
                A[1]*kx[1]*cos(kx[1]*x[0] + phasex[1])*sin(ky[1]*(x[1]-v*t)) + 
                U*A[0]*ky[0];
}


int main(int argc, char** argv) {


   MPI_Init(&argc, &argv);
   int rank, size;
   
   MPI_Comm_rank(MPI_COMM_WORLD, &rank);
   MPI_Comm_size(MPI_COMM_WORLD, &size);

   int its = 10;
   // Inicialização e distribuiçao de cond. iniciais
   double *x0s;
   double *y0s;

   if (rank == 0 ){
      x0s = (double*)malloc(size*sizeof(double)); // apenas o 1o processo ganha um pedaçao
      y0s = (double*)malloc(size*sizeof(double)); // apenas o 1o processo ganha um pedaçao
      x0s[0] = 0.1;
      x0s[1] = 0.2;
      y0s[0] = 0.3;
      y0s[1] = 0.4;
   }
   else{
      x0s = (double*)malloc(1*sizeof(double)); // resto ganha pocalias apenas
      y0s = (double*)malloc(1*sizeof(double)); // resto ganha pocalias apenas
   }
   


    // parte de alocação de memoria
   double *global_x; // array final do resultado
   double *global_y; // array final do resultado

   if (rank == 0 ){
      global_x = (double*)malloc(its*size*sizeof(double)); // apenas o 1o processo ganha um pedaçao
      global_y = (double*)malloc(its*size*sizeof(double)); // apenas o 1o processo ganha um pedaçao
   }
   else{
      global_x = (double*)malloc(2*1*sizeof(double)); // apenas o 1o processo ganha um pedaçao
      global_y = (double*)malloc(2*1*sizeof(double)); 
   }


   double x0;
   double y0;
   MPI_Barrier(MPI_COMM_WORLD); // garante q tudo foi alocado e lido certinho    
   MPI_Scatter(x0s, 1, MPI_DOUBLE, &x0, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
   printf(" rank %d %lf: \n",rank,x0) ;

   // memoria para x(t) e y(t)
   double *xts = (double*)malloc(its*size*sizeof(double));
   double *yts = (double*)malloc(its*size*sizeof(double));
   
   xts[0] = x0;
   yts[0] = y0;

   state_type x = {x0, y0}; // initial conditions
   runge_kutta4 < state_type > stepper; // formato de stepper/passo/integraçao do integrador

   for (int i = 1; i < its; i++){
      xts[i] = xts[i-1] + 0.01;
   }
   
    

    
   MPI_Barrier(MPI_COMM_WORLD); // sincronia antes de juntar todos os dados

   //pega todos os dados
   MPI_Gather(xts, its, MPI_DOUBLE,
            global_x, its, MPI_DOUBLE,
            0, MPI_COMM_WORLD);
  
    // sincronia por garantia
   MPI_Barrier(MPI_COMM_WORLD);
    


    // printa os valores 
   if (rank == 0 ){
       for (int i = 0; i < size; i++){
           for (int j = 0; j < its; j++){
               printf("%6lf ",global_x[i*its + j]);
       }
       printf("\n");        
       }
   }


   MPI_Finalize();
   //free(global_data);
   return 0;
}