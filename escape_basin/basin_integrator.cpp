#include <stdio.h>
#include <boost/numeric/odeint.hpp>
#include <math.h>       /* fmod */

using namespace boost::numeric::odeint;
using namespace std;


// sistema de funções de Lorentz


//   dxdt[0] = + 0.2*3*cos(3*x[1] + phasesy[1])*sin(3*(x[0]-(6/3 - 3/3)*t)+ phasesx[1])
//   dxdt[1] =   0.2*3*sin(3*x[1] + phasesy[1])*cos(3*(x[0]-(6/3 - 3/3)*t)+ phasesx[1]);

// state_type = double
// problema com duas dimensoes, ou estado do sistema
// x == x[0] e y = x[1] nesse caso
typedef boost::array< double , 2 > state_type; 



// Variaveis do sisema, amplitudes, frequencias etc...
array<double,2> A;
array<double,2> w;
array<double,2> kx;
array<double,2> ky;
array<double,2> phasex;
double v;
double U;
double tf;
double t;

string output_local;


void mysyst( const state_type &x , state_type &dxdt , double t ){
    // sistemas de EDO pra integrar no tempo
    // na direção x
    dxdt[0] =   -A[0]*ky[0]*sin(kx[0]*x[0] + phasex[0])*cos(ky[0]*x[1]) -
                 A[1]*ky[1]*sin(kx[1]*x[0] + phasex[1])*cos(ky[1]*(x[1]-(w[1]/ky[1] - w[0]/ky[0])*t));


    // na direçao y
    dxdt[1] =   A[0]*kx[0]*cos(kx[0]*x[0] + phasex[0])*sin(ky[0]*x[1]) +
                A[1]*kx[1]*cos(kx[1]*x[0] + phasex[1])*sin(ky[1]*(x[1]-(w[1]/ky[1] - w[0]/ky[0])*t)) + 
                U*A[0]*ky[0];
}
 

double step = 0.001;

int main(int argc, char** argv)
{   
    // argumetnos da linah de comando
    double x0 = atof(argv[1]); // x' inicial (já normalizado)
    double y0 = atof(argv[2]); // y' inicial (já normalizado)
    double var = atof(argv[3]);
    // Constantes do sistema
    A = {1,0.5};
    kx = {3,3};
    ky = {3,3};
    v = var;
    phasex = {0,M_PI/2};
    U = 0;
    double tau = abs(2.0*M_PI/(v*ky[1])); // usado p mapas


    tf = tau*300; // calcula o tempo final dado as N iteraçoes do estrobo
    state_type x = {x0, y0}; // initial conditions
    runge_kutta4 < state_type > rk; // formato de passo/integraçao do integrador

    printf("%lf \t %lf \t",x[0],x[1]);
    bool escape;
    while (t <= tf){
        if (x[0] < 0 || x[0] > 2*3.14159265359){
            printf("1 \n");
            escape = true;
            break;
        }
        if (x[1] < 0 || x[1] > 2*3.14159265359){
            printf("2 \n");
            escape = true;
            break;
        }
        rk.do_step(mysyst, x, t, step);  
        t += step;
    }
    if (!escape){
        printf("0 \n");
    }
    
   
    return 0;
}


