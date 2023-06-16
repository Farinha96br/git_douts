#include <stdio.h>  // biblioteca padrão
#include <iostream>
#include <fstream>
#include <math.h>
#include <cstdlib>
#include <ctime>
#include <iomanip>
#include "myfunctions.h"
#include <string>



// recebe uma posição xn e retorna a posição após um tempo dt
using namespace std;

int main(int argc, char const *argv[]) {
    // parametros pra cada particula
  int n1 = atoi(argv[1]); // indice da particula p salvar o nome
  double x = atof(argv[2]); // x' inicial (já normalizado)
  double y = atof(argv[3]); // y' inicial (já normalizado)
  double iterations = atof(argv[4]);  // numero de interaçõe
  string out_folder = string(argv[5]); // saida do arquivo
  double var1 = atof(argv[6]); // Em geral a variavel que a gente quer variar
  // quantidade das ondas
  int c_w = 0;  // índice da onda central da transformada
  int nw = 2; 
  double An[nw], kx[nw], ky[nw], w[nw],phasesx[nw], phasesy[nw]; // arrays da cois das ondas

  // Parametros das ondas em si:

  // Valores de amplitude na verdade sao A_do_programa = A/B0

  An[0] = 1;
   w[0] = 3; // usando Nx pq ai tem a velocidade igual a 1
  kx[0] = 3;
  ky[0] = 3;
  phasesx[0] = 0;
  phasesy[0] = 0;

  An[1] = 0.0;
  w[1] = 6;
  kx[1] = 3;
  ky[1] = 3;
  phasesx[1] = 0;
  phasesy[1] = M_PI/2;
  double U = var1;

  // ajeita o nome do arquivo de saida dos pontos
  ofstream myfile;
  char ns[100];
  sprintf(ns,"%06d",n1); // ajeita o nome
  myfile.open((out_folder + "/traj/" + ns + ".dat").c_str()); // salva cada ponto individualmente

  //double strobe = abs(2.0*M_PI/((w[1]/ky[1] - w[c_w]/ky[c_w])*ky[1])); // estrobo pra quanto tem só duas ondas
  double strobe = 0.01; // estrobo
  double t = 0;
  double step = 0.0001;      

  // FAZ O ARQUIVO COM OS DADOS NORMALIZADOS
  if (n1 == 0) {
    ofstream logfile;
    logfile.open((out_folder +  "/log_norm.dat").c_str());
    logfile << "# dados normalizados utilizados na simulação usando " << nw << "ondas \n";
    logfile << "# dt = " << step << "\t strobe = " << strobe << "\t tfinal = " << strobe*iterations << " \n";
    logfile <<
     "#i" << "\t"  << "A" << "\t" << "w" << "\t" << "Kx" << "\t" << "Ky" << "\t" << "kycent" << "\t" <<  "v" << "\t" <<" v_rel" << "\t" << "phasex \t" << "phasey" <<"\n";
    for (int i = 0; i < nw; i++) {
      logfile <<
       i << "\t"  << An[i] << "\t" << w[i] << "\t" << kx[i] << "\t" << ky[i] << "\t" << ky[c_w] << "\t" <<  w[i]/ky[i] << "\t" << w[i]/ky[i] - w[c_w]/ky[c_w] << "\t" << phasesx[i] << "\t" << phasesy[i] << "\n";
    }
    logfile.close();
  }

  // pedaços do RK4
  double k1,k2,k3,k4;
  double l1,l2,l3,l4;
 
  int strobe_c = 0; // contador do estrobo
  //  Loop de integracao
  while (t <= 1.0*strobe*iterations) {
    if ( (t > strobe_c*strobe - step/2) && (t < strobe_c*strobe + step/2)) {
      myfile << t << "\t" << x << "\t" << y << "\t" << k1 << "\t" << l1 << "\n";
      //cout << strobe_c << "\n";
      strobe_c++;
    }

    k1 = dydt2(t,x,y,w,An,kx,ky,phasesx,phasesy);
    l1 = dxdt2(t,x,y,w,An,kx,ky,phasesx,phasesy,U);
    
    k2 = dydt2(t+step/2,x + k1*step/2, y + l1*step/2,w,An,kx,ky,phasesx,phasesy);
    l2 = dxdt2(t+step/2,x + k1*step/2, y + l1*step/2,w,An,kx,ky,phasesx,phasesy,U);
    
    k3 = dydt2(t+step/2,x + k2*step/2, y + l2*step/2,w,An,kx,ky,phasesx,phasesy);
    l3 = dxdt2(t+step/2,x + k2*step/2, y + l2*step/2,w,An,kx,ky,phasesx,phasesy,U);
    
    k4 = dydt2(t+step,x + k3*step, y + l3*step,w,An,kx,ky,phasesx,phasesy);
    l4 = dxdt2(t+step,x + k3*step, y + l3*step,w,An,kx,ky,phasesx,phasesy,U);

    y +=  (k1 +  2*k2 + 2*k3 + k4)*step/6;
    x +=  (l1 +  2*l2 + 2*l3 + l4)*step/6;
    t += step;
  }
  myfile.close();
  cout << "DONE: " << n1 << " ";
  return 0;
}
