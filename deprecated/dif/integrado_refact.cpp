#include <stdio.h>
#include <boost/numeric/odeint.hpp>
#include <math.h>       /* fmod */
#include <unistd.h>

using namespace boost::numeric::odeint;
using namespace std;


// state_type = double
// problema com duas dimensoes, ou estado do sistema
// x == x[0] e y = x[1] nesse caso
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



FILE *filex; // cria o pointer do arquivo
FILE *filey; // cria o pointer do arquivo



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



// função pra printar o role
double strobe; // estrobo pra quanto tem só duas ondas
double step = 0.001; // define o passo temporal


int main(int argc, char** argv)
{   
    // argumetnos da linha de comando
    int n1 = atoi(argv[1]); // indice da particula p salvar o nome
    double x0 = atof(argv[2]); // x' inicial (já normalizado)
    double y0 = atof(argv[3]); // y' inicial (já normalizado)
    int it = atoi(argv[4]);  // numero de interaçõe
    char *out_folder = argv[5];
    double var = atof(argv[6]);

    // Constantes do sistema
    A = {1,var};
    kx = {3,3};
    ky = {3,3};
    v = 1;
    phasex = {0,M_PI/16};
    U = 0;
    double tau = abs(2.0*M_PI/(v*ky[1])); // usado p mapas

    //Saida de arquivos com nome formatado;

    double datax[it];
    double datay[it];
    if (n1 == 0){
        double datat[it];
    }
    


   

    // define o estrobo
    strobe = 0.01; // usado p mapas
    //strobe = 0.01; // Usado pra ver a trajetoria da particula em sí

    double tf = it*strobe; // calcula o tempo final dado as N iteraçoes do estrobo
    state_type x = {x0, y0}; // initial conditions
    runge_kutta4 < state_type > stepper; // formato de stepper/passo/integraçao do integrador


    // Isso aqui gera o artigo com relatorio dos dados
    if (n1 == 0){
        FILE *reportfile; // inicializa o arquivo
        char reportlocal[150]; // string de onde vai ser salvo o role
        sprintf(reportlocal,"%s/report.log",out_folder);
        reportfile = fopen(reportlocal,"w");
        fprintf(reportfile, "#tf = %lf \t step = %lf \n", tf, step);
        fprintf(reportfile, "#i \t A \t w \t kx \t ky \t phasex\n");
        fprintf(reportfile, "1 \t %lf \t %lf \t %lf \t %lf \t %lf \n",A[0],w[0],kx[0],ky[0],phasex[0]);
        fprintf(reportfile, "1 \t %lf \t %lf \t %lf \t %lf \t %lf \n",A[1],w[1],kx[1],ky[1],phasex[1]);
        fclose(reportfile);
    }
    


    

    t = 0;
    int c = 0;
    while (t < tf){     
        if ((t > c*strobe - step/2) && (t < c*strobe + step/2)){
            //cout << t << '\t' << x[0] << '\t' << x[1] <<  endl;
            //fprintf(outfile, "%lf \t %lf \t %lf \n",t,x[0],x[1]);
            datax[c] = x[0];
            datay[c] = x[1];
            c++;
        }
        stepper.do_step(mysyst, x, t, step);  
        t += step;
    }
    
    // Agora é a parte que escreve nos arquivos mesmo
    int arrsize = it*100 + it;
    char writex[arrsize];
    char writey[arrsize];
    sprintf(writex,"%d ",n1);
    sprintf(writey,"%d ",n1);
    sprintf(writex,"%s %lf",writex,datax[0]);
    sprintf(writey,"%s %lf",writey,datay[0]);
    for (int i = 1; i < it; i++){
        sprintf(writex,"%s %lf",writex,datax[i]);
        sprintf(writey,"%s %lf",writey,datay[i]);
    }


    char writelocx[100];

    sprintf(writelocx,"%s/datax.dat",out_folder);
    filex = fopen(writelocx,"a"); // inicializa o arquivo de fato
    fprintf(filex, "%s\n",writex); // de fato escreve no arquivo
    char writelocy[100];
    sprintf(writelocy,"%s/datay.dat",out_folder);
    filey = fopen(writelocy,"a"); // inicializa o arquivo de fato
    fprintf(filey,"%s\n",writey); // de fato escreve no arquivo
    


    // salva o arquivo de tempo separado so por garantia
    c = 0;
    t = 0;
    if (n1 == 0){
        char writeloct[100];
        FILE *filet; // cria o pointer do arquivo
        sprintf(writeloct,"%s/datat.dat",out_folder);
        filet = fopen(writeloct,"w"); // inicializa o arquivo de fato
        while (t < tf){     
            if ((t > c*strobe - step/2) && (t < c*strobe + step/2)){
                fprintf(filet,"%lf ",t);
                c++;
            }
        t += step;
        }
    fclose(filet);
    }

    
    fclose(filex);
    fclose(filey);


}


