#include <stdio.h>  // biblioteca padrão
#include <iostream>
#include <fstream>
#include <math.h>
#include <cstdlib>
#include <ctime>
#include <iomanip>



using namespace std;

int main(int argc, char const *argv[]){
    int n1 = atoi(argv[1]);
    sleep(n1);
    cout << n1 << "\n";
    ofstream myfile;
    char ns[100];
    sprintf(ns,"%06d",n1); // ajeita o nome
    myfile.open((string(ns) + ".dat").c_str()); // salva cada ponto individualmente


    for (int i = 0; i < n1; i++){
            myfile << i << "\n";
        }
}
