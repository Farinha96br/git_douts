#include <stdio.h>  // biblioteca padrão
#include <iostream> // enstrada e saida de dados
#include <fstream>
#include <math.h>   // matematica



using namespace std;


double logistic(double x, double r){
    return x*r*(1-x);
}


int main(int argc, char const *argv[])
{
    


    int its = 1000;
    double x;

    FILE *outfile; // cria o pointer do arquivo
    outfile = fopen("logistic_map_0.5001.dat","w"); // inicializa o arquivo de fato

    for (double r = 0; r < 4; r+=0.001){
        printf("%lf \n",r);
        fprintf(outfile, "%lf ",r);
        x = 0.5001;
        for (int i = 0; i < its; i++){
            fprintf(outfile, "%lf ",x);
            x = logistic(x,r);   
        }
        fprintf(outfile, "\n");
    }
    
    
 
    fclose(outfile); // close the file



    return 0;
}

