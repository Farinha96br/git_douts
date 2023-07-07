#include <stdio.h>  // biblioteca padrão
#include <iostream>
#include <fstream>
#include <math.h>
#include <cstdlib>
#include <ctime>
#include <gsl/gsl_rng.h> // biblioteca p numeros aleatorios
#include <iomanip>
  
double exp_icft(double x, double beta){
    return -log(1-x)/beta;
}

double ptc_x(double L,double theta){
    return cos(theta)*L;
}

double ptc_y(double L,double theta){
    return sin(theta)*L;
}

  
  
  
using namespace std;
int main(int argc, char const *argv[])
{
    int n1 = atoi(argv[1]);
    // parametros pra cada particula
    double iterations = atof(argv[2]);  // numero de interaçõe
    string out_folder = string(argv[3]); // saida do arquivo
    double var = atof(argv[4]);

    //int gsl_rng_default_seed = n1; // semente é o primeiro argumento
    gsl_rng *rng= gsl_rng_alloc(gsl_rng_taus); // cria o gerador de numero aleatorio
    gsl_rng_set(rng,n1+1);//

    
    //gsl_rng_uniform(rng); // faz o numero aleatorio
    
    ofstream myfile;
    char ns[100];
    sprintf(ns,"%05d",n1); // ajeita o nome
    myfile.open((out_folder + "/traj/" + ns + ".dat").c_str()); // salva cada ponto individualmente

    double x = 0;
    double y = 0;
    double L;
    double theta;
    double t;
    while (t <= iterations) {
        myfile << t << "\t" << x << "\t" << y <<"\n";
        L = exp_icft(gsl_rng_uniform(rng),var);
        theta = gsl_rng_uniform(rng)*2*3.14159265359;
        x += ptc_x(L,theta);
        y += ptc_y(L,theta);
        t += 1;
    }
  myfile.close();
  cout << "DONE " << n1 << "\n";




    


    return 0;
}


  
  
  
  



