#include <stdio.h>  // biblioteca padrão
#include <iostream> // enstrada e saida de dados
#include <fstream>
#include <math.h>   // matematica



using namespace std;

int main(int argc, char const *argv[])
{
    
    double dy = 0.25;
    int size = 15;
    int NY = 4;
    int NX = 3;
    int L0 = 1;
    double *y0s;
    double *x0s;
    y0s = (double*)malloc(size*sizeof(double)); // apenas o 1o processo ganha um pedaçao
    x0s = (double*)malloc(size*sizeof(double)); // apenas o 1o processo ganha um pedaçao

    for (int i = 0; i < size; i++){
        x0s[i] = ((i+L0)%NX);
        y0s[i] = ((i+L0)/NY);
        printf("%d %lf %lf\n",i+L0,x0s[i],y0s[i]);
    }

    return 0;
}

