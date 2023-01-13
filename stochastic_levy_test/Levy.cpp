#include <stdio.h>  // biblioteca padrão
#include <iostream>
#include <fstream>
#include <math.h>
#include <cstdlib>
#include <ctime>
#include <gsl/gsl_rng.h> // biblioteca p numeros aleatorios
#include <iomanip>
  
  
  
  

int main(int argc, char const *argv[])
{
    int gsl_rng_default_seed = 1996; // semente é o primeiro argumento
    gsl_rng *rng= gsl_rng_alloc(gsl_rng_taus); // cria o gerador de numero aleatorio
    gsl_rng_uniform(rng); // faz o numero aleatorio



    


    return 0;
}


  
  
  
  



