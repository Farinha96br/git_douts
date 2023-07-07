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
double step; // define o passo temporal



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

double *linspace(double x0,double xf,int N){
    double dx = (xf - x0)/(N-1);
    double *x = (double*)malloc(N*sizeof(double));
    for (int i = 0; i < N; i++){
        x[i] = dx*i;
    }
    return x;
}


int main(int argc, char** argv) {
   MPI_Init(&argc, &argv);
   //double var = atof(argv[6]);

   int rank, size;
   
   MPI_Comm_rank(MPI_COMM_WORLD, &rank);
   MPI_Comm_size(MPI_COMM_WORLD, &size);

   int its = 100;
   // Inicialização e distribuiçao de cond. iniciais
   double *x0s;
   double *y0s;
    // parte de alocação de memoria
   double *global_x; // array final do resultado
   double *global_y; // array final do resultado

   if (rank == 0 ){
      x0s = (double*)malloc(size*sizeof(double)); // apenas o 1o processo ganha um pedaçao
      y0s = (double*)malloc(size*sizeof(double)); // apenas o 1o processo ganha um pedaçao
      global_x = (double*)malloc(its*size*sizeof(double)); // apenas o 1o processo ganha um pedaçao
      global_y = (double*)malloc(its*size*sizeof(double)); // apenas o 1o processo ganha um pedaçao

      // cond. iniciais
      x0s = linspace(0,1,size);
      y0s = linspace(0,3,size);

   }
   else{
      x0s = (double*)malloc(1*sizeof(double)); // resto ganha pocalias apenas
      y0s = (double*)malloc(1*sizeof(double)); // resto ganha pocalias apenas
      global_x = (double*)malloc(2*1*sizeof(double)); // apenas o 1o processo ganha um pedaçao
      global_y = (double*)malloc(2*1*sizeof(double)); 
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

   // parametros do sistema
    // Constantes do sistema
   A = {1,0.0};
   kx = {3,3};
   ky = {3,3};
   v = 1;
   phasex = {0,M_PI/4};
   U = 0;
   double tau = abs(2.0*M_PI/(v*ky[1])); // usado p mapas
	step = tau/1000; // passo eh um milesimo do periodo da perturbação;
   

   // define o estrobo
   strobe = tau; // usado p mapas
   //strobe = 0.01; // Usado pra ver a trajetoria da particula em sí
   double tf = its*strobe; // calcula o tempo final dado as N iteraçoes do estrobo
	
   state_type x = {x0, y0}; // initial conditions
	runge_kutta4 < state_type > stepper; // formato de stepper/passo/integraçao do integrador
   
   //printf("rank:%d x y: %lf %lf : \n",rank,x[0],x[1]);

	// parte de integracao
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

	MPI_Gather(yts, its, MPI_DOUBLE,
            global_y, its, MPI_DOUBLE,
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

	if (rank == 0 ){
       for (int i = 0; i < size; i++){
           for (int j = 0; j < its; j++){
               printf("%6lf ",global_y[i*its + j]);
       }
       printf("\n");        
       }
   }


   MPI_Finalize();
   //free(global_data);
   return 0;
}