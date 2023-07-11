#include <stdio.h>  // biblioteca padrão
#include <iostream> // enstrada e saida de dados
#include <fstream>
#include <math.h>   // matematica



using namespace std;

int main(int argc, char const *argv[])
{
    
    double dy = 0.25;
    int size = 12;
    int NY = 5;
    int L0 = 5;
    double *y0s;
    y0s = (double*)malloc(size*sizeof(double)); // apenas o 1o processo ganha um pedaçao

    for (int i = 0; i < size; i++){
        y0s[i] = ((i+L0)/NY)*dy;
        printf("%d %lf\n",i+L0,y0s[i]);
    }

    return 0;
}

