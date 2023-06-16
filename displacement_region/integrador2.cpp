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
array<double,2> phasey;
double U;
double tf;

string output_local;


// the integration methods will always call them in the form f(x, dxdt, t) 
void mysyst( const state_type &x , state_type &dxdt , double t ){
    // sistemas de EDO pra integrar no tempo
    // na direçao X
    dxdt[0] = - (A[0]*ky[0]*cos(ky[0]*x[1] + phasey[0])*sin(kx[0]*x[0]) + 
                 A[1]*ky[1]*cos(ky[1]*x[1] + phasey[1])*sin(kx[1]*(x[0]-(w[1]/kx[1] - w[0]/kx[0])*t))) + 
                 U*A[0]*kx[0];
    // na direção Y
    dxdt[1] =    A[0]*kx[0]*sin(ky[0]*x[1] + phasey[0])*cos(kx[0]*x[0]) + A[1]*kx[1]*sin(ky[1]*x[1] + 
                phasey[1])*cos(kx[1]*(x[0]-(w[1]/kx[1] - w[0]/kx[0])*t));
}

// função pra printar o role
double strobe = abs(2.0*M_PI/((6/3 - 3/3)*3)); // estrobo pra quanto tem só duas ondas

int strobe_c = 0;
double step = 0.01;

void write_mine( const state_type &x , double t){   
    }

int main(int argc, char** argv)
{   
    // argumetnos da linah de comando
    int n1 = atoi(argv[1]); // indice da particula p salvar o nome
    double x0 = atof(argv[2]); // x' inicial (já normalizado)
    double y0 = atof(argv[3]); // y' inicial (já normalizado)
    double iterations = atof(argv[4]);  // numero de interaçõe
    double var = atof(argv[5]);

    // Constantes do sistema
    A = {1,var};
    w = {3,6};
    kx = {3,3};
    ky = {3,3};
    phasey = {0,M_PI/4};
    U = 0;


    tf = iterations*strobe; // calcula o tempo final dado as N iteraçoes do estrobo
    state_type x = {x0, y0}; // initial conditions
    printf("%lf \t %lf \t",x[0],x[1]);
    runge_kutta4 < state_type > stepper; // formato de passo/integraçao do integrador
    integrate_const(stepper , mysyst , x , 0.0 , tf , step);
    printf("%lf \t %lf \n",x[0],x[1]);

}


