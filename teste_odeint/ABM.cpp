#include <iostream>
#include <complex>
#include <boost/array.hpp>
#include <boost/numeric/odeint.hpp>
#include <boost/version.hpp>

using namespace std;
typedef array< complex<double>, 3> state_type;
using namespace boost::numeric::odeint;


const double omega1 = -0.0136;
const double omega2 = 0.01619048;
const double omega3 = -0.03090909;

const double lambda1 = -0.0026;
const double lambda2 = 0.00404762;
const double lambda3 = -0.00045455;


struct mima
{
    double m_gamma1,m_gamma2,m_gamma3;

    mima( double gamma1 = 0.0,double gamma2=0.0,double gamma3=0.0 )
    : m_gamma1( gamma1 ),m_gamma2( gamma2 ),m_gamma3( gamma3 ) { }

    void operator()( const state_type &x , state_type &dxdt , double t ) const
    {
        const complex< double > I( 0.0 , 1.0 );
        dxdt[0] = -I*omega1*x[0]+lambda1*conj(x[1])*conj(x[2])+m_gamma1*x[0];
        dxdt[1] = -I*omega2*x[1]+lambda2*conj(x[2])*conj(x[0])+m_gamma2*x[1];
        dxdt[2] = -I*omega3*x[2]+lambda3*conj(x[0])*conj(x[1])+m_gamma3*x[2];
    }
};


void write_lorenz( const state_type &x , const double t )
{
  if(fmod(t,5)==0){
    cout << t << '\t' << x[0].real() << '\t' << x[0].imag() << '\t' << x[1].real() << '\t' << x[1].imag() << '\t' << x[2].real()  << '\t' << x[2].imag()  << endl;
  }
}

struct push_back_state_and_time
{
    std::vector< state_type >& m_states;
    std::vector< double >& m_times;

    push_back_state_and_time( std::vector< state_type > &states , std::vector< double > &times )
    : m_states( states ) , m_times( times ) { }

    void operator()( const state_type &x , double t )
    {
        m_states.push_back( x );
        m_times.push_back( t );
    }
};

int main() {

    vector<state_type> x_vec;
    vector<double> times;
    state_type x;
    vector<double> psi2;
    


        adams_bashforth_moulton< 4 , state_type > stepper;
        x[0] = complex<double>(0.1,0.0);
        x[1] = complex<double>(0.1,0.0);
        x[2] = complex<double>(0.1,0.0);
        size_t steps = integrate_adaptive( stepper , mima(-0.1,0.01,-0.1) , x , 0.0 , 15000.0 , 1e-3,write_lorenz);

   		


       
  
    
 
    
    
}
