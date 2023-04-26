//#include <iostream>
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


// the integration methods will always call them in the form f(x, dxdt, t) 
double A[2] = {1,0.1};
double w[2] = {3,6};
double kx[2] = {3,3};
double ky[2] = {3,3};
double phasey[2] = {0,M_PI/2};


void mysyst( const state_type &x , state_type &dxdt , double t )
{   // sistemas de EDO pra integrar no tempo
    // na direçao X
    dxdt[0] = - (A[0]*ky[0]*cos(ky[0]*x[1] + phasey[0])*sin(kx[0]*x[0]) + 
                 A[1]*ky[1]*cos(ky[1]*x[1] + phasey[1])*sin(kx[1]*(x[0]-(w[1]/kx[1] - w[0]/kx[0])*t)));
    // na direção Y
    dxdt[1] =    A[0]*kx[0]*sin(ky[0]*x[1] + phasey[0])*cos(kx[0]*x[0]) + A[1]*kx[1]*sin(ky[1]*x[1] + 
                phasey[1])*cos(kx[1]*(x[0]-(w[1]/kx[1] - w[0]/kx[0])*t));

}

// função pra printar o role
double strobe = abs(2.0*M_PI/((6/3 - 3/3)*3)); // estrobo pra quanto tem só duas ondas

int strobe_c = 0;
double step = 0.01;
void write_mine( const state_type &x , double t ){   
    /*if ( (t > strobe_c*strobe - step/2) && (t < strobe_c*strobe + step/2)) {
      cout << t << '\t' << x[0] << '\t' << x[1] <<  endl;
      strobe_c++;
    }
    */
    if (fmod(t,strobe) < step){
        cout << t << '\t' << x[0] << '\t' << x[1] <<  endl;
    }
}


int main(int argc, char** argv)
{   
    int n1 = atoi(argv[1]); // indice da particula p salvar o nome
    double x0 = atof(argv[2]); // x' inicial (já normalizado)
    double y0 = atof(argv[3]); // y' inicial (já normalizado)
    int iterations = 1000;
    double tf = iterations*strobe;
    state_type x = {x0, y0}; // initial conditions
    runge_kutta4< state_type > stepper;
    integrate_const(stepper , mysyst , x , 0.0 , tf , 0.01, write_mine);
    //integrate( mysyst , x , 0.0 , 10000.0 , 0.001 , write_mine );// integra de fato
}
