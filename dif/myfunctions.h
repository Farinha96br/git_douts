#include <stdio.h>  // biblioteca padrão
#include <iostream>
#include <fstream>
#include <string>


using namespace std;

double U(double t,double *w,double *ky, int c_w, double fac){
    // Funçao do parametro de controle pra qdo eu quiser variar no tempo
  //return 0.5*cos(fac*(w[1]/ky[1] - w[c_w]/ky[c_w])*ky[1]);
  //return 0;
  return fac;
}


// An[0]*kx[0]*U + 
double dxdt2(double t,double x,double y,double *w, double *An, double *kx, double *ky, double *phasesx, double *phasesy,double U){
  
  return 
  An[0]*ky[0]*U + 
  An[0]*ky[0]*cos(ky[0]*y + phasesy[0])*sin(kx[0]*x + phasesx[0]) + 
  An[1]*ky[1]*cos(ky[1]*y + phasesy[1])*sin(kx[1]*(x-(w[1]/kx[1] - w[0]/kx[0])*t)+ phasesx[1]);
}

double dydt2(double t,double x,double y,double *w, double *An, double *kx, double *ky, double *phasesx, double *phasesy){

  return -1*(
  An[0]*kx[0]*sin(ky[0]*x + phasesy[0])*cos(kx[0]*x + phasesx[0]) + 
  An[1]*kx[1]*sin(ky[1]*x + phasesy[1])*cos(kx[1]*(x-(w[1]/kx[1] - w[0]/kx[0])*t)+ phasesx[1])
  );
}

