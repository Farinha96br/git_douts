#include <stdio.h>  // biblioteca padrão
#include <iostream> // enstrada e saida de dados
#include <fstream>
#include <math.h>   // matematica
#include <vector>

double *linspace(double x0,double xf,int N){
    double dx = (xf - x0)/(N-1);
    double *x = (double*)malloc(N*sizeof(double));
    for (int i = 0; i < N; i++){
        x[i] = dx*i;
    }
    return x;
}

using namespace std;

int main(int argc, char const *argv[]){
    

    FILE *outfile; // cria o pointer do arquivo
    outfile = fopen("teste.dat","w"); // inicializa o arquivo de fato
    
    int NX = 5;
    int NY = 3;
    double *x = linspace(0,1,NX);
    double *y = linspace(0,2,NY);

    double startx[NX*NY];
    double starty[NX*NY];


    for (int i = 0; i < NX; i++){
        for (int j = 0; j < NY; j++){
            startx[i*NY+j] = x[j];
            starty[i*NY+j] = y[i];
        }    /* code */
    }

    for (int i = 0; i < NX; i++){
        for (int j = 0; j < NY; j++){
            printf("%lf ",startx[i*NY+j]);
        }    /* code */
        printf("\n");
    }
    printf("-----\n");
    for (int i = 0; i < NX; i++){
        for (int j = 0; j < NY; j++){
            printf("%lf ",starty[i*NY+j]);
        }    /* code */
        printf("\n");
    }
    
    



    
    
    





    

    
    








    

    fclose(outfile); // close the file



    return 0;
}

