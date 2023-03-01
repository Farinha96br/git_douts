#include <stdio.h>  // biblioteca padrão
#include <iostream>
#include <fstream>
#include <math.h>
#include <cstdlib>
#include <ctime>
#include <gsl/gsl_rng.h> // biblioteca p numeros aleatorios
#include <iomanip>

// recebe uma posição xn e retorna a posição após um tempo dt


double U(double t,double *w,double *ky, int c_w, double fac){
  //return 0.5*cos(fac*(w[1]/ky[1] - w[c_w]/ky[c_w])*ky[1]);
  //return 0;
  return fac;
}


double dxdtn(double t,double x,double y,double *w, double *An, double *kx, double *ky,int c_w, int nw, double *phases){
  // derivada em x em relaçao ao tempo
  double R = 0;
  for (int i = 0; i < nw; i++) {
    R += An[i]*ky[i]*sin(kx[i]*x)*sin(ky[i]*(y-(w[i]/ky[i] - w[c_w]/ky[c_w])*t) + phases[i]);
  }
  return R;
}

double dydtn(double t,double x,double y,double *w, double *An, double *kx, double *ky, int c_w, int nw, double *phases, double fac){
  // derivada em y em relação ao tempo
  double R = 0;
  for (int i = 0; i < nw; i++) {
    R += An[i]*kx[i]*cos(kx[i]*x)*cos(ky[i]*(y-(w[i]/ky[i] - w[c_w]/ky[c_w])*t) + phases[i]);
  }
  //return R+fac*An[c_w]*kx[c_w];
  return R;
}

double dydt2(double t,double x,double y,double *w, double *An, double *kx, double *ky){

  return An[0]*kx[0]*cos(kx[0]*x)*cos(ky[0]*y) + An[1]*kx[1]*cos(kx[1]*x)*cos(ky[1]*(y-(w[1]/ky[1] - w[0]/ky[0])*t));
}

double dxdt2(double t,double x,double y,double *w, double *An, double *kx, double *ky){

  return An[0]*ky[0]*sin(kx[0]*x)*sin(ky[0]*y) + An[1]*ky[1]*sin(kx[1]*x)*sin(ky[1]*(y-(w[1]/ky[1] - w[0]/ky[0])*t));
}


using namespace std;

int main(int argc, char const *argv[]) {
  // setup das do gerador aleatorio
  //int gsl_rng_default_seed = 1996; // semente é o primeiro argumento
	//gsl_rng *rng= gsl_rng_alloc(gsl_rng_taus);
  // nome indice da particula
  int n1 = atoi(argv[1]);
  // parametros pra cada particula
  double x = atof(argv[2]); // x' inicial (já normalizado)
  double y = atof(argv[3]); // y' inicial (já normalizadtmax = atof(argv[4]);  // numero de interaçõe
  double tmax = atof(argv[4]);
  string out_folder = string(argv[5]); // saida do arquivo
  double var = atof(argv[6]);

  //  //  //   parametros originais
  // double U = 0;  // Campo elétrico radial em V/m

  // coisas do espectro
  int nw = 2;   // numero de ondas
  int c_w = 0;  // índice da onda central da transformada
  double An[nw], kx[nw], ky[nw], w[nw]; // frequencais das demais ondas

  // organiza as fases de cada onda
  double phases[nw];
  int p_c = 0;
  for (int i = 0; i < nw; i++) {
    if (p_c == 0) {
      phases[i] = 0;
    }
    //if (p_c == 1) {
    //  phases[i] = 2*M_PI*gsl_rng_uniform(rng); // fases aleatorias
    //}
  }

  An[0] = 1;
   w[0] = 6;
  kx[0] = 12*3.1415;
  ky[0] = 6;
  
  An[1] = var;
  w[1] = 10;
  kx[1] = 12;
  ky[1] = 6;
  
  ofstream myfile;
  char ns[100];
  sprintf(ns,"%06d",n1); // ajeita o nome
  myfile.open((out_folder + "/traj/" + ns + ".dat").c_str()); // salva cada ponto individualmente


  //int c_s = 8;

  int strobe_c = 0;
  double t = 0;
  double step = 0.001;      // passo temporal já normalizado

  // FAZ LA O ARQUIVO COM OS DADOS NORMALIZADOS
  if (n1 == 0) {
    ofstream logfile;
    logfile.open((out_folder +  "/log_norm.dat").c_str());
    logfile << "# dados normalizados utilizados na simulação usando " << nw << "ondas \n";
    logfile << "# dt = " << step << "\t tfinal = " << tmax << " \n";
    logfile <<
     "#i" << "\t"  << "A" << "\t" << "w" << "\t" << "Kx" << "\t" << "Ky" << "\t" << "kycent" << "\t" <<  "v" << "\t" <<" v_rel" << "\t" << "phase" <<"\n";
    for (int i = 0; i < nw; i++) {
      logfile <<
       i << "\t"  << An[i] << "\t" << w[i] << "\t" << kx[i] << "\t" << ky[i] << "\t" << ky[c_w] << "\t" <<  w[i]/ky[i] << "\t" << w[i]/ky[i] - w[c_w]/ky[c_w] << "\t" << phases[i] << "\n";
    }
    logfile.close();
  }

  double k1,k2,k3,k4;
  double l1,l2,l3,l4;

  double cellx = 3.1415/kx[0];
  double celly = 3.1415/ky[0];
  double dmax = sqrt(cellx*cellx + celly*celly);
  double x0 = x;
  double y0 = y;


  //  Loop de integracao
  while (t <= tmax) {
    if ( sqrt((x-x0)*(x-x0) + (y-y0)*(y-y0)) > 3*dmax ) {
      myfile << x << "\t" << remainder(y,2*M_PI) << 1 << "\n";
      myfile.close();
      return 0;
    }
    /// Depois da quali, arrumar a normalização pelo fator B

    double k1 = dxdt2(t,x,y,w,An,kx,ky);
    double l1 = dydt2(t,x,y,w,An,kx,ky);

    double k2 = dxdt2(t+step/2,x + k1*step/2, y + l1*step/2,w,An,kx,ky);
    double l2 = dydt2(t+step/2,x + k1*step/2, y + l1*step/2,w,An,kx,ky);

    double k3 = dxdt2(t+step/2,x + k2*step/2, y + l2*step/2,w,An,kx,ky);
    double l3 = dydt2(t+step/2,x + k2*step/2, y + l2*step/2,w,An,kx,ky);

    double k4 = dxdt2(t+step,x + k3*step, y + l3*step,w,An,kx,ky);
    double l4 = dydt2(t+step,x + k3*step, y + l3*step,w,An,kx,ky);

    x +=  (k1 +  2*k2 + 2*k3 + k4)*step/6;
    y +=  (l1 +  2*l2 + 2*l3 + l4)*step/6;
    t += step;
  }
  
  myfile << x << "\t" << remainder(y,2*M_PI) << 0 << "\n";
  myfile.close();
  cout << "DONE: " << n1 << " ";

  return 0;
}
