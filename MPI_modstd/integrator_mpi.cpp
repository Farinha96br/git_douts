#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <boost/numeric/odeint.hpp>
#include<gsl/gsl_rng.h> 

using namespace boost::numeric::odeint;
using namespace std;

// Inicializa as variaveis do sisema, amplitudes, frequencias etc...
//array<double,1> phasex;
double k;
double M; // numero de ondas
double t;
// função pra printar o role
double strobe; // estrobo pra quanto tem só duas ondas
double step; // define o passo temporal


    
  



int main(int argc, char** argv) {
   MPI_Init(&argc, &argv);
   int gencase = atoi(argv[1]); // 0 = grid de pontos, 1 = pontos aleatorios
   int L0 = atoi(argv[2]); // linha dos dados que começa a ler
   int its = atoi(argv[3]);
   int M = atoi(argv[4]);
   double K = atof(argv[5]);

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
         int NX = 9; // numero de pontos em X
         int NY = 9; // numero de pontos em Y
         double dx;
         double p0x =   0;
         double pfx =   2*3.1415;
         double p0y =  -3.1415;
         double pfy =   3.1415;
         if (NX == 1){
            dx = 0;
         }
         else{
            dx = (pfx - p0x)/(NX-1.0); // faz o passo usando a ideia do linspace
         }
         double dy = (pfy - p0y)/(NY-1.0); // 
         for (int i = 0; i < size; i++){
            x0s[i] = ((i+L0)/NX)*dx + p0x;
            y0s[i] = ((i+L0)%NY)*dy + p0y;
               //printf("%d %lf %lf\n",i+L0,x0s[i],y0s[i]);
         }
      }
      // pontos iniciais aleatorios, usando L0 como seed
      if (gencase == 1){
         gsl_rng_default_seed = L0; 
         gsl_rng *w = gsl_rng_alloc(gsl_rng_taus); 
         for (int i = 0; i < size; i++){
            x0s[i] = gsl_rng_uniform(w)*2.0*M_PI;
            y0s[i] = gsl_rng_uniform(w)*4.0 - 2.0;
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
   step = 2*M_PI/5000;
   strobe = 2*M_PI;


   double tf = its*strobe;
   printf("x: %lf y %lf \n",x0 ,y0);
  
   double p = y0;
   double q = x0;



	
   // inicializa as fases aleatorias
   double tempsum;
   double phases[2*M+1];
   
   gsl_rng_default_seed = 1996; 
   gsl_rng *w = gsl_rng_alloc(gsl_rng_taus); 
   for (int i = 0; i < 2*M+1; i++){
      phases[i] = gsl_rng_uniform(w)*2.0*M_PI;
      //phases[i] = 0;

      //printf("%d %lf\n",i,phases[i]);
   }
   gsl_rng_free(w);

   int c = 0;
   t = 0;

   while (t < tf){    
      if ((t > c*strobe - step/2) && (t < c*strobe + step/2)){
   		//printf(" rank:%d x[0]: %lf: \n",rank,x[0]) ;
         xts[c] = q;
			yts[c] = p;
			c++;
      }
      q += step*p;
      tempsum = 0;
      

      for (int m = -M; m <= M; m++){
         tempsum += sin(q-m*t+phases[m+M]);
      }
      //tempsum = tempsum/(2*M+1);
      p += step*tempsum*K/(4*M_PI*M_PI);

      
        
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
      sprintf(outx,"%s/q.dat",argv[7]);
      filex = fopen(outx,"a");

      FILE *filey;
      char outy[100];
      sprintf(outy,"%s/p.dat",argv[7]);
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