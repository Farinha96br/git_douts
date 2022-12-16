#include <stdio.h>  // biblioteca padrão
#include <iostream>
#include <fstream>
#include <math.h>
#include <cstdlib>
#include <ctime>
#include <gsl/gsl_rng.h> // biblioteca p numeros aleatorios
#include <iomanip>

// recebe uma posição xn e retorna a posição após um tempo dt
// teste do git???




double dxdt2(double t,double x,double y,double *w, double *An, double *kx, double *ky,int c_w, int nw, double *phases){
  // derivada em x em relaçao ao tempo
  double R = 0;
  for (int i = 0; i < nw; i++) {
    R += An[i]*ky[i]*sin(kx[i]*x)*sin(ky[i]*(y-(w[i]/ky[i] - w[c_w]/ky[c_w])*t) + phases[i]);
  }
  return R;
}

double dydt2(double t,double x,double y,double *w, double *An, double *kx, double *ky, int c_w, int nw, double *phases, double U){
  // derivada em y em relação ao tempo
  double R = 0;
  for (int i = 0; i < nw; i++) {
    R += An[i]*kx[i]*cos(kx[i]*x)*cos(ky[i]*(y-(w[i]/ky[i] - w[c_w]/ky[c_w])*t) + phases[i]);
  }
  return R+U*An[c_w]*kx[c_w];
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
  double iterations = atof(argv[4]);  // numero de interaçõe
  string out_folder = string(argv[5]); // saida do arquivo
  double var = atoi(argv[6]);



  //  //  //   parametros originais
  double a0 = 0.18; // Raio maximo do plasma em metros
  double E0 = 3300.0; // Campo eletrico em V/m
  double B0 = 1.1;  // Campo magnético em T
  double v0 = E0/B0;// Velocidade de deriva em m/s
  double t0 = a0/E0;
  double U = 0;  // Campo elétrico radial em V/m


  // coisas do espectro
  int nw = 11;   // numero de ondas
  int c_w = 3;  // índice da onda central da transformada
  double f[nw], An[nw], kx[nw], ky[nw]; // frequencais das demais ondas

  // organiza as fases de cada onda
  double phases[nw];

  for (int i = 0; i < nw; i++) {
    if (var == 0) {
      phases[i] = 0;
    }
    if (var == 1) {
      phases[i] = 2*M_PI*gsl_rng_uniform(rng); // fases aleatorias
    }
  }


  // organiza as frequencias, Amplitudes e numeros de onda de cada onda
  // Valores experimentais

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


  /*
  An[0] = 25;
  An[1] = 25*0.4;
  f[0] = 10000;
  f[1] = 11000;
  ky[0] = 55.555;
  kx[0] = 104.719;
  ky[1] = ky[0]*sqrt(2);
  kx[1] = kx[0]*sqrt(2);
*/



  // Arquivo log das variaveis originais
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

  ofstream myfile;
  char ns[100];
  sprintf(ns,"%06d",n1); // ajeita o nome
  myfile.open((out_folder + "/traj/" + ns + ".dat").c_str()); // salva cada ponto individualmente

  double k1,k2,k3,k4;
  double l1,l2,l3,l4;
  //int c_s = 8;
  //double strobe = abs(2.0*M_PI/((w[8]/ky[8] - w[c_w]/ky[c_w])*ky[1])); // estrobo pra quanto tem só duas ondas
  double strobe = 0.1; // estrobo normalizado
  //std::cout << strobe << '\n';

  int strobe_c = 0;
  double t = 0;
  double step = 0.0001;      // passo temporal já normalizado

  if (n1 == 0) {
    ofstream logfile;
    logfile.open((out_folder +  "/log_norm.dat").c_str());
    logfile << "# dados normalizados utilizados na simulação usando " << nw << "ondas \n";
    logfile << "# dt = " << step << "\t strobe = " << strobe << "\t tfinal = " << strobe*iterations << " \n";
    logfile <<
     "#i" << "\t"  << "A" << "\t" << "w" << "\t" << "Kx" << "\t" << "Ky" << "\t" << "kycent" << "\t" <<  "v" << "\t" <<" v_rel" << "\t" << "phase" <<"\n";
    for (int i = 0; i < nw; i++) {
      logfile <<
       i << "\t"  << An[i] << "\t" << w[i] << "\t" << kx[i] << "\t" << ky[i] << "\t" << ky[c_w] << "\t" <<  w[i]/ky[i] << "\t" << w[i]/ky[i] - w[c_w]/ky[c_w] << "\t" << phases[i] << "\n";
    }
    logfile.close();
  }



  while (t <= 1.0*strobe*iterations) {
    if ( (t > strobe_c*strobe - step/2) && (t < strobe_c*strobe + step/2)) {
      myfile << t << "\t" << x << "\t" << remainder(y,2*M_PI) <<"\n";
      //cout << strobe_c << "\n";
      strobe_c++;
    }

    /// Depois da quali, arrumar a normalização pelo fator B

    double k1 = dxdt2(t,x,y,w,An,kx,ky,c_w,nw,phases);
    double l1 = dydt2(t,x,y,w,An,kx,ky,c_w,nw,phases,U);

    double k2 = dxdt2(t+step/2,x + k1*step/2, y + l1*step/2,w,An,kx,ky,c_w,nw,phases);
    double l2 = dydt2(t+step/2,x + k1*step/2, y + l1*step/2,w,An,kx,ky,c_w,nw,phases,U);

    double k3 = dxdt2(t+step/2,x + k2*step/2, y + l2*step/2,w,An,kx,ky,c_w,nw,phases);
    double l3 = dydt2(t+step/2,x + k2*step/2, y + l2*step/2,w,An,kx,ky,c_w,nw,phases,U);

    double k4 = dxdt2(t+step,x + k3*step, y + l3*step,w,An,kx,ky,c_w,nw,phases);
    double l4 = dydt2(t+step,x + k3*step, y + l3*step,w,An,kx,ky,c_w,nw,phases,U);

    x +=  (k1 +  2*k2 + 2*k3 + k4)*step/6;
    y +=  (l1 +  2*l2 + 2*l3 + l4)*step/6;
    t += step;
  }
  myfile.close();
  cout << "DONE" << n1 << "\n";


  return 0;
}
