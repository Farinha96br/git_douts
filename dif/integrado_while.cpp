#include <stdio.h>
#include <boost/numeric/odeint.hpp>
#include <math.h>       /* fmod */
#include <iostream>
#include <fstream>
#include <math.h>
#include <cstdlib>
#include <ctime>
#include <iomanip>

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

FILE *outfile;
string output_local;

// the integration methods will always call them in the form f(x, dxdt, t) 
//void mysyst2( const state_type &x , state_type &dxdt , double t ){
//    // sistemas de EDO pra integrar no tempo
//    // na direçao X
//    dxdt[0] = - (A[0]*ky[0]*cos(ky[0]*x[1] + phasex[0])*sin(kx[0]*x[0]) + 
//                 A[1]*ky[1]*cos(ky[1]*x[1] + phasex[1])*sin(kx[1]*(x[0]-(w[1]/kx[1] - w[0]/kx[0])*t))) + 
//                 U*A[0]*kx[0];
//    // na direção Y
//    dxdt[1] =    A[0]*kx[0]*sin(ky[0]*x[1] + phasex[0])*cos(kx[0]*x[0]) + 
//                 A[1]*kx[1]*sin(ky[1]*x[1] + phasex[1])*cos(kx[1]*(x[0]-(w[1]/kx[1] - w[0]/kx[0])*t));
//}


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
    double iterations = atof(argv[4]);  // numero de interaçõe
    string out_folder = string(argv[5]); // saida do arquivo
    double var = atof(argv[6]);

    // Constantes do sistema
    A = {1,var};
    kx = {3,3};
    ky = {3,3};
    v = 1;
    phasex = {0,M_PI/2};
    U = 0;
    double tau = abs(2.0*M_PI/(v*ky[1])); // usado p mapas

    //Saida de arquivos com nome formatado;
    char ns[100];
    sprintf(ns,"%06d",n1); // ajeita o nome
    output_local = out_folder + "/traj/" + ns + ".dat";
    outfile = fopen(output_local.c_str(),"w");

    // define o estrobo
    //strobe = tau; // usado p mapas
    strobe = 0.01; // Usado pra ver a trajetoria da particula em sí

    double tf = iterations*strobe; // calcula o tempo final dado as N iteraçoes do estrobo
    state_type x = {x0, y0}; // initial conditions
    runge_kutta4 < state_type > stepper; // formato de stepper/passo/integraçao do integrador

    if (n1 == 0){
        FILE *reportfile; // inicializa o arquivo
        string reportlocal; // string de onde vai ser salvo o role
        reportlocal = out_folder + "/report.dat"; ///
        reportfile = fopen(reportlocal.c_str(),"w");
        fprintf(reportfile, "#tf = %lf \t step = %lf \n", tf, step);
        fprintf(reportfile, "#i \t A \t w \t kx \t ky \t phasex\n");
        fprintf(reportfile, "1 \t %lf \t %lf \t %lf \t %lf \t %lf \n",A[0],w[0],kx[0],ky[0],phasex[0]);
        fprintf(reportfile, "1 \t %lf \t %lf \t %lf \t %lf \t %lf \n",A[1],w[1],kx[1],ky[1],phasex[1]);
        fclose(reportfile);
    }
    
    int strobe_c = 0;
    while (t < tf){     
        if ((t > strobe_c*strobe - step/2) && (t < strobe_c*strobe + step/2)){
            //cout << t << '\t' << x[0] << '\t' << x[1] <<  endl;
            fprintf(outfile, "%lf \t %lf \t %lf \n",t,x[0],x[1]);
            strobe_c++;
        }
        stepper.do_step(mysyst, x, t, step);  
        t += step;
    }

    fclose(outfile); // fecha o arquivo de saida
}


