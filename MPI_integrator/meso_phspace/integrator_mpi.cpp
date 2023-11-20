#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <boost/numeric/odeint.hpp>
#include<gsl/gsl_rng.h> 

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



int main(int argc, char** argv) {
   MPI_Init(&argc, &argv);
   int gencase = atoi(argv[1]); // 0 = grid de pontos, 1 = pontos aleatorios
   int L0 = atoi(argv[2]); // linha dos dados que começa a ler
   int its = atoi(argv[3]);
   double var = atof(argv[4]);
   double var2 = atof(argv[5]);
   // argv[6] é o arquivo de entrada
   // argv[7] é a pasta de saida

   int rank, size;
   MPI_Comm_rank(MPI_COMM_WORLD, &rank);
   MPI_Comm_size(MPI_COMM_WORLD, &size);
   //printf("argv no rank %d: %d \n",rank,L0);

   // Inicialização e distribuiçao de cond. iniciais
   double *x0s;
   double *y0s;
   // parte de alocação de memoria
   double *global_x; // array final do resultado
   double *global_y; // array final do resultado
   
   MPI_Barrier(MPI_COMM_WORLD); // garante q tudo foi alocado e lido certinho    

   if (rank == 0 ){
      x0s = (double*)malloc(size*sizeof(double)); // apenas o 1o processo ganha um pedaçao
      y0s = (double*)malloc(size*sizeof(double)); // apenas o 1o processo ganha um pedaçao
      global_x = (double*)malloc(its*size*sizeof(double)); // apenas o 1o processo ganha um pedaçao
      global_y = (double*)malloc(its*size*sizeof(double)); // apenas o 1o processo ganha um pedaçao
      // faz a lista de pontos iniciais em x e y:
      // nesse caso uma malha estilo np.meshgrid

      if (gencase == 0){
         int NX = 8; // numero de pontos em X
         int NY = 8; // numero de pontos em Y
         double p0x = 0-0.02;
         double pfx = 0+0.02;
         double p0y = 0-0.02;
         double pfy = 0+0.02;
         
         //double p0x = 0.7*2*M_PI/3;
         //double pfx = 2*M_PI/3;
         //double p0y = 0.7*2*M_PI/3;
         //double pfy = 2*M_PI/3;
         
         double dx = (pfx - p0x)/(NX-1.0); // faz o passo usando a ideia do linspace
         double dy = (pfy - p0y)/(NY-1.0); // 
         for (int i = 0; i < size; i++){
            x0s[i] = ((i+L0)%NX)*dx + p0x;
            y0s[i] = ((i+L0)/NY)*dy + p0y;
               //printf("%d %lf %lf\n",i+L0,x0s[i],y0s[i]);
         }
      }
      // pontos iniciais aleatorios, usando L0 como seed
      if (gencase == 1){
         gsl_rng_default_seed = L0; 
         gsl_rng *w = gsl_rng_alloc(gsl_rng_taus); 
         for (int i = 0; i < size; i++){
            x0s[i] = gsl_rng_uniform(w)*2.0*M_PI/3;
            y0s[i] = gsl_rng_uniform(w)*2.0*M_PI/3;
         }
         gsl_rng_free(w);
      }

      // Pontos iniciais carregados por um arquivo externo
      if (gencase == 2){
         // entrada do arqui vo
         //char intxy[100];
         //sprintf(intxy,"%s/start.dat",argv[5]);
         FILE *input_file;
         input_file = fopen(argv[6],"r");
         //
         int line = 0;
         int index_load = 0;
         double tempx, tempy;
         while (fscanf(input_file, "%lf %lf", &tempx, &tempy) == 2) {
            if ((line == L0 + index_load) && (index_load < size)){
               printf("%d %d %lf %lf \n",line,index_load,tempx,tempy);
               x0s[index_load] = tempx;
               y0s[index_load] = tempy;
               index_load++;
            }
            line++;
         }
         
      }
   }

   else{
      x0s = (double*)malloc(1*sizeof(double)); // resto ganha pocalias apenas
      y0s = (double*)malloc(1*sizeof(double)); // resto ganha pocalias apenas
      global_x = (double*)malloc(1*sizeof(double)); // apenas o 1o processo ganha um pedaçao
      global_y = (double*)malloc(1*sizeof(double)); 

   }

   // distribui as cond. iniciais
   MPI_Barrier(MPI_COMM_WORLD); // garante q tudo foi alocado e lido certinho    

   double x0;
   double y0;
   
   MPI_Barrier(MPI_COMM_WORLD); // garante q tudo foi alocado e lido certinho    
   MPI_Scatter(x0s, 1, MPI_DOUBLE, &x0, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
   MPI_Scatter(y0s, 1, MPI_DOUBLE, &y0, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
	//printf(" rank %d %lf: \n",rank,x0) ;
   // memoria para x(t) e y(t)
   MPI_Barrier(MPI_COMM_WORLD); // garante q tudo foi alocado e lido certinho    

   double *xts = (double*)malloc(its*size*sizeof(double));
   double *yts = (double*)malloc(its*size*sizeof(double));
   MPI_Barrier(MPI_COMM_WORLD); // garante q tudo foi alocado e lido certinho    

   // parametros do sistema
    // Constantes do sistema
   A = {1.0,var};
   kx = {3.0,3.0};
   ky = {3.0,3.0};
   v = 1.0;
   phasex = {0,var2};
   U = 0;
   double tau = abs(2.0*M_PI/(v*ky[1])); // usado p mapas
	step = tau/500.0; // passo eh um milesimo do periodo da perturbação;
   

   // define o estrobo
   strobe = tau; // usado p mapas
   //strobe = 0.01; // Usado pra ver a trajetoria da particula em sí
   double tf = its*strobe; // calcula o tempo final dado as N iteraçoes do estrobo
	//printf("rank %d: %lf %lf\n",rank,x0,y0);
   state_type state = {x0, y0}; // initial conditions
	runge_kutta4 < state_type > stepper; // formato de stepper/passo/integraçao do integrador
   
   //printf("rank:%d x y: %lf %lf : \n",rank,state[0],state[1]);

	// parte de integracao
	int c = 0;
   while (t < tf){    
      if ((t > c*strobe - step/2) && (t < c*strobe + step/2)){
   		//printf(" rank:%d x[0]: %lf: \n",rank,x[0]) ;
         xts[c] = state[0];
			yts[c] = state[1];
			c++;
      }
      stepper.do_step(mysyst, state, t, step);  
      t += step;
   }



   MPI_Barrier(MPI_COMM_WORLD); // sincronia antes de juntar todos os dados

   //pega todos os dados
   MPI_Gather(xts, its, MPI_DOUBLE,
            global_x, its, MPI_DOUBLE,
            0, MPI_COMM_WORLD);

   MPI_Gather(yts, its, MPI_DOUBLE,
            global_y, its, MPI_DOUBLE,
            0, MPI_COMM_WORLD);
  
    // sincronia por garantia
   MPI_Barrier(MPI_COMM_WORLD);
    


    // printa os valores 
   
   
   if (rank == 0 ){
      printf("WRITING... \n");
      FILE *filex;
      char outx[100];
      sprintf(outx,"%s/x.dat",argv[7]);
      filex = fopen(outx,"a");

      FILE *filey;
      char outy[100];
      sprintf(outy,"%s/y.dat",argv[7]);
      filey = fopen(outy,"a");


      for (int i = 0; i < size; i++){
         for (int j = 0; j < its; j++){
            //printf("%lf ",global_x[i*its + j]);
            fprintf(filex,"%lf \t",global_x[i*its + j]);
            fprintf(filey,"%lf \t",global_y[i*its + j]);
         }
      fprintf(filex,"\n");
      fprintf(filey,"\n");
      }
      fclose(filex);
      fclose(filey);
   }




   MPI_Finalize();
   free(global_x);
   free(global_y);
   free(x0s);
   free(y0s);
   free(xts);
   free(yts);

   


   return 0;
}