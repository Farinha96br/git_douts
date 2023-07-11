#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define Nx 250
#define Ny 250
#define dt 1.0e-3 
#define D  100.0   //D = D/(Delta x)^2
#define tf 3.0

double f(int x, int y, double *phi){
    // recebe os indices da da posiçao da rede, e retorna o novo valor
	int xp1, xm1, yp1, ym1;
	xp1= (x+1)%Nx;
	xm1= (x-1+Nx)%Nx;
	yp1= (y+1)%Ny;
	ym1= (y-1+Ny)%Ny;
	return (phi[xp1*Ny+y] + phi[xm1*Ny+y] + phi[x*Ny+yp1] + phi[x*Ny+ym1] - 4.0*phi[x*Ny+y]);
}

void write(int n, double *phi){
    // funçao pra escrever num arquivo o estado
	int x, y;
	FILE *file;
	char name[100];
	sprintf(name, "data/phi-%d.dat", n);
	file= fopen(name, "w");
	for(x= 0; x< Nx; x++){
		for(y= 0; y< Ny; y++){
			fprintf(file, "%.5e ", phi[x*Ny+y]);
		}
		fprintf(file, "\n");
	}
	fclose(file);
}

int main(int argc, char **argv){
	int x, y; 
	double *phi, *p_t;

	phi= (double *) calloc(Nx*Ny, sizeof(double));
	p_t= (double *) calloc(Nx*Ny, sizeof(double));

//condição inicial - começo
	for(x= 0; x< Nx; x++){
		for(y= 0; y< Ny; y++){
			if(sqrt((x-0.5*Nx)*(x-0.5*Nx) + (y-0.5*Ny)*(y-0.5*Ny)) < 25.0){
				phi[x*Ny+y]= 0.0;
			}else{
				phi[x*Ny+y]= 1.0;
			}
		}
	}

//condição inicial
	
//solução da eq. da difusão - começo
int c = 0;
double t = 0.0;
	while (t < tf){
		write(c, phi);
		for(x= 0; x< Nx; x++){
			for(y= 0; y< Ny; y++){
				p_t[x*Ny+y]= phi[x*Ny+y] + 0.5*dt*D*f(x, y, phi);
			}
		}
		for(x= 0; x< Nx; x++){
			for(y= 0; y< Ny; y++){
				phi[x*Ny+y]+= dt*D*f(x, y, p_t);
			}
		}
		t+=dt;
		c++;
	}

	free(phi);
	free(p_t);
	return 0;
}





