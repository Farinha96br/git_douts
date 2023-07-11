#include <stdio.h>  // biblioteca padrão
#include <iostream> // enstrada e saida de dados
#include <fstream>
#include <math.h>   // matematica



using namespace std;

int main(int argc, char const *argv[])
{
    

    FILE *infile; // cria o pointer do arquivo
    infile = fopen("data.dat","r"); // inicializa o arquivo de fato
    
    for (int i = 0; i < 10; i++){ // loop fodase
        fprintf(outfile, "teste %d %d",i,i*2) // de fato escreve no arquivo
    }

    fclose(outfile); // close the file



    return 0;
}

