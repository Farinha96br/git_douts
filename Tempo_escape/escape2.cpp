#include <stdio.h>  // biblioteca padrão
#include <iostream>
#include <fstream>
#include <math.h>
#include <cstdlib>
#include <ctime>
#include <gsl/gsl_rng.h> // biblioteca p numeros aleatorios


double Ulin(double x){
  return 0.5 - 0.5*x;
}

double Ucte(double x){
  return 0;
}

double gaussian(double x, double xc, double sigma){
  // funçao Gaussiana normalizada
  // wc = centro do pico
  // sigma = largura da distribuiçao
  // sigma grande => curva larga
  return 10*exp(-0.5*(pow((x-xc)/sigma,2)))/(sigma*sqrt(2*M_PI));
  //return exp(-0.5*(pow((x-xc)/sigma,2)))/(sigma*sqrt(2*M_PI)) ;
}

double dxdt2(double t,double x,double y,double *w, double *An, double *kx, double *ky,int c_w, int nw, double *phases){
  // derivada em x em relaçao ao tempo
  double R = 0;
  for (int i = 0; i < nw; i++) {
    R += An[i]*ky[i]*sin(kx[i]*x)*sin(ky[i]*(y-(w[i]/ky[i] - w[c_w]/ky[c_w])*t) + phases[i]);
  }
  return R;
}

double dydt2(double t,double x,double y,double *w, double *An, double *kx, double *ky, int c_w, int nw, double *phases){

  // derivada em y em relação ao tempo
  double R = 0;
  for (int i = 0; i < nw; i++) {
    R += An[i]*kx[i]*cos(kx[i]*x)*cos(ky[i]*(y-(w[i]/ky[i] - w[c_w]/ky[c_w])*t) + phases[i]);
  }
  return R + Ucte(x)*An[c_w]*kx[c_w];
}






using namespace std;

int main(int argc, char const *argv[]) {
  // setup das do gerador aleatorio
  int gsl_rng_default_seed = 1996; // semente é o primeiro argumento
	gsl_rng *rng= gsl_rng_alloc(gsl_rng_taus);
  // nome indice da particula
  int n1 = atoi(argv[1]);
  // parametros pra cada particula
  double x = atof(argv[2]); // x' inicial (já normalizado)
  double y = atof(argv[3]); // y' inicial (já normalizado)
  string out_folder = string(argv[4]); // saida do arquivo
  double var =  atof(argv[5]);


  //  //  //   parametros originais
  double a0 = 0.18; // Raio maximo do plasma em metros
  double E0 = 3300.0; // Campo eletrico em V/m
  double B0 = 1.1;  // Campo magnético em T
  double v0 = E0/B0;// Velocidade de deriva em m/s
  double t0 = a0/E0;


  // coisas do espectro
  int nw = 2;   // numero de ondas
  int c_w = 0;  // índice da onda central da transformada
  double f[nw], An[nw], kx[nw], ky[nw]; // frequencais das demais ondas

  // organiza as fases de cada onda
  double phases[nw];
  int p = 0;
  for (int i = 0; i < nw; i++) {
    if (p == 0) {
      phases[i] = 0; // em fase
    }
    if (p == 1) {
      phases[i] = 2*M_PI*gsl_rng_uniform(rng); // fases aleatori
    }
    //phases[i] = i*2*3.1415/51;
    //std::cout << phases[i] << '\n';
  }


  // organiza as frequencias, Amplitudes e numeros de onda de cada onda
  // Valores experimentais

  /*
  ky[0] =50.36;
  ky[1] =58.68;
  ky[2] =62.00;
  ky[3] =61.111111;
  ky[4] =61.111111;
  ky[5] =65.63;
  ky[6] =71.913;
  ky[7] =76.662;
  ky[8] =81.192;
  ky[9] =84.97;
  ky[10]=88.02;

  f[0]= 24819.0;
  f[1]= 28020.0;
  f[2]= 32089.0;
  f[3]= 37371.0;
  f[4]= 41047.0;
  f[5]= 44089.0;
  f[6]= 46423.0;
  f[7]= 49157.0;
  f[8]= 52645.0;
  f[9]= 56224.0;
  f[10]=60025.0;

  An[0] =20.0;
  An[1] =23.0;
  An[2] =27.0;
  An[3] =32.0;
  An[4] =27.0;
  An[5] =25.0;
  An[6] =23.0;
  An[7] =23.0;
  An[8] =27.0;
  An[9] =25.0;
  An[10]=20.0;

  for (int i = 0; i < nw; i++) {
      kx[i] = ky[i]*sqrt(2);
  }
*/

  An[0] = 25;
  f[0] = 10000;
  ky[0] = 55.555;
  kx[0] = 104.719;

  An[1] = An[0]*var;
  f[1] = 11000;
  kx[1] = kx[0]*sqrt(2);
  ky[1] = ky[0]*sqrt(2);

  if (n1 == 0) {
    ofstream logfile;
    logfile.open((out_folder +  "/log_orig.dat").c_str());
    logfile << "#dados utilizados na simulação usando " << nw << "ondas \n";
    logfile <<
     "#i" << "\t"  << "A" << "\t" << "F" << "\t" << "Kx" << "\t" << "Ky" << "\t" << "kycent" << "\t" <<  "v" << "\t" <<" v_rel" << "\t" << "phase" <<"\n";
    for (int i = 0; i < nw; i++) {
      logfile <<
       i << "\t"  << An[i] << "\t" << f[i] << "\t" << kx[i] << "\t" << ky[i] << "\t" << ky[c_w] << "\t" <<  f[i]*2*M_PI/ky[i] << "\t" << f[i]*2*M_PI/ky[i] - f[c_w]*2*M_PI/ky[c_w] << "\t" << phases[i] << "\n";
    }
    logfile.close();
  }


  double w[nw];              // omega normalizado do modelo
  for (int i = 0; i < nw; i++) {
    w[i] = f[i]*2.0*M_PI*t0;
    kx[i] = kx[i]*a0;
    ky[i] = ky[i]*a0;
    An[i] = An[i]/(E0*a0);
  }

  //std::cout << "step = " << step << '\n';

  double k1,k2,k3,k4;
  double l1,l2,l3,l4;
  //double strobe = abs(2.0*M_PI/((w[8]/ky[8] - w[c_w]/ky[c_w])*ky[1])); // estrobo pra quanto tem só duas ondas
  //std::cout << strobe << '\n';

  double t = 0;
  double step = 0.001;      // passo temporal já normalizado

  double x0 = x;
  double y0 = y;
  double tmax = 500.0;
  while (t <= tmax) {
    if (x >= 1.05) {
      cout  << x0 << "\t" << remainder(y0,2*M_PI) << "\t" << t << "\n";
      //cout << x0 << "\t" << remainder(y0,2*M_PI) << "\t" << t << " Escaped \n";
      //cout << "DONE" << ns << "\n";
      return 0;
    }

    double k1 = dxdt2(t,x,y,w,An,kx,ky,c_w,nw,phases);
    double l1 = dydt2(t,x,y,w,An,kx,ky,c_w,nw,phases);

    double k2 = dxdt2(t+step/2,x + k1*step/2, y + l1*step/2,w,An,kx,ky,c_w,nw,phases);
    double l2 = dydt2(t+step/2,x + k1*step/2, y + l1*step/2,w,An,kx,ky,c_w,nw,phases);

    double k3 = dxdt2(t+step/2,x + k2*step/2, y + l2*step/2,w,An,kx,ky,c_w,nw,phases);
    double l3 = dydt2(t+step/2,x + k2*step/2, y + l2*step/2,w,An,kx,ky,c_w,nw,phases);

    double k4 = dxdt2(t+step,x + k3*step, y + l3*step,w,An,kx,ky,c_w,nw,phases);
    double l4 = dydt2(t+step,x + k3*step, y + l3*step,w,An,kx,ky,c_w,nw,phases);

    x +=  (k1 +  2*k2 + 2*k3 + k4)*step/6;
    y +=  (l1 +  2*l2 + 2*l3 + l4)*step/6;
    t += step;

  }
  // Casodas particulas que nao escaparam
  cout << x0 << "\t" << remainder(y0,2*M_PI) << "\t" << tmax << "\n";
  //cout << x0 << "\t" << remainder(y0,2*M_PI) << "\t" << 500 << " Traped \n";

  //cout << "DONE" << ns << "\n";
  return 0;



}
