#include <stdio.h>  // biblioteca padrão
#include <iostream> // enstrada e saida de dados
#include <fstream>
#include <math.h>   // matematica
#include <string.h>

#define N 10


using namespace std;

int main(int argc, char const *argv[])
{

    // 100 valores de tamanho 64 + 100 valores p caracteres especiais \t \n 
    int arrsize = N * 32 + N;
    char finalarray[arrsize];
    char temp[32];

    double data[N];

    for (int i = 0; i < N; i++){
        data[i] = i*atof(argv[1]);
        //printf("%s",finalarray[arrsize-1]);
    }
    
    sprintf(finalarray,"%s ",argv[1]);
    printf("%s \n",finalarray);
    sprintf(finalarray,"%s %lf",finalarray,data[0]);
    printf("%s \n",finalarray);
    for (int i = 1; i < N; i++){
        sprintf(finalarray,"%s %lf",finalarray,data[i]);
    }
    sprintf(finalarray,"%s\n",finalarray);

    printf("%s \n",finalarray);



    FILE *outfile; // cria o pointer do arquivo
    outfile = fopen("teste.dat","a"); // inicializa o arquivo de fato
    
    fprintf(outfile, "%s",finalarray); // de fato escreve no arquivo
    


    fclose(outfile);
    return 0;
}

