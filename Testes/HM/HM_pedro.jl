using PyPlot, Random, FFTW, DelimitedFiles

function mindist2(x, val)
    # using enumerate to avoid indexing
    min_i = 0
    min_x = Inf
    for (i, xi) in enumerate(x)
        dist = abs(xi - val)
        if dist < min_x
            min_x = dist
            min_i = i
        end
    end
    return min_i
end

function main()
	nx, ny = 64, 64 # number of grid points
	Lx, Ly = 2.0*pi, 2.0*pi      # size of the domain in each direction

	# constructing the physical grid (x,y)
	dx, dy = Lx/nx, Ly/ny
	 x = 0:dx:Lx-dx
	 y = 0:dy:Ly-dy

	X  = zeros(nx,ny)
	Y  = zeros(nx,ny)
	for j in 1:ny, i in 1:nx
	     X[i, j] = x[i]
	     Y[i, j] = y[j]
	end

	# constructing the wavenumber grid (k,l)
	k  = 2.0*pi/Lx * [0:nx/2; -nx/2+1:-1];
	l  = 2.0*pi/Ly * [0:ny/2; -ny/2+1:-1];

	Kx = zeros(nx, ny)
	Ky = zeros(nx, ny)
	for j in 1:ny, i in 1:nx
	    Kx[i, j] = k[i] #cria o grid em Kx
	    Ky[i, j] = l[j] #cria o grid em Ky
	end
    
    ksq = @. Kx^2 + Ky^2 #faz k^2
	kqt = @. Kx^4 + Ky^4 + 2 * Kx^2 * Ky^2# faz k^4
    invksq = 1 ./(1 .+ksq) #faz 1/(1+k^2)
    
    
    #Definicoes de tempo
    dt = 0.025 # the time step
	tfin = 1000 # the final time for the integration
	nstep  = Int(tfin/dt) + 1;  # the total number of time steps
    t = 0:dt:tfin; 
    time = 0
	nc = Int(nx/32)

    #Cria as condicoes iniciais
    #Random.seed!(1235)
	psi0 = randn(nx, ny) #cria as condicoes inicias aleatoriamentes
	psih = fft(psi0) #calcula a fft das condicoes iniciais
	psih[1, 1] = 0 #filtra os divergentes
	psih[@. ksq > (10)^2 ] .= 0 #faz uma filtragem inicial
	psih[@. ksq < (3)^2 ] .= 0
	psi0 = real(ifft(psih)) #recalculo usando as filtragens 
	phih = invksq.*psih           # calculate \hat{phi}
	psi =  real(ifft(psih))       # calculate ζ(x,y,t)
	phix = real(ifft(im*Kx.*phih))     # calculate phix velocity u(x,y,t)
	phiy = real(ifft(im*Ky.*phih))     # calculate phiy velocity v(x,y,t)
	psix =  real(ifft(im*Kx.*psih))    # calculate ∂psi/∂x
	psiy =  real(ifft(im*Ky.*psih))    # calculate ∂psi/∂y

    #Faz o plot das condicoes iniciais
    #figure(1)
    phi = real(ifft(phih))
	#pcolormesh(X, Y, phi)
	#colorbar()
	#quiver(X[1:nc:end,1:nc:end], Y[1:nc:end,1:nc:end], -1 .*phix[1:nc:end,1:nc:end], -1 .*phiy[1:nc:end,1:nc:end])
	#xlabel(L"x")
	#ylabel(L"y")
	#title(string("Potencial & E at t=", time))
	#axis("square")
	#draw();
	
	#savefig("HMI.png")
	
	#parametros
	nu = 2.0e-04      
	vu = 0.0
	v = zeros(2,0)
	pos = zeros(2,0)
	npos = [x[15],y[50]]
	nv = [0,0]
	pos = hcat(pos,npos)
	v = hcat(v,nv)
	
	#fig = figure()
	
	for j = 2:nstep
	    
	    phih = invksq.*psih               # calculate \hat{ψ}
		phix = real(ifft(im*Kx.*phih))     # calculate phix velocity u(x,y,t)
		phiy = real(ifft(im*Ky.*phih))     # calculate phiy velocity v(x,y,t)
		psix =  real(ifft(im*Kx.*psih))    # calculate ∂psi/∂x
		psiy =  real(ifft(im*Ky.*psih))    # calculate ∂psi/∂y

	    # now we are ready to calculate the r.h.s. of our PDE
	    #rhs = -fft(phix.*psiy - phiy.*psix) - nu.*(-ksq.*phih+ksq.*psih)+vu.*fft(phiy)
	    
		k1 = -fft(phix.*psiy - phiy.*psix) - nu.*(-ksq.*phih+ksq.*psih)+vu.*fft(phiy)
	    
		psihk1 = psih + dt*k1/2.0
		phihk1 = invksq.*psihk1
		phixk1 = real(ifft(im*Kx.*phihk1))     # calculate phix velocity u(x,y,t)
		phiyk1 = real(ifft(im*Ky.*phihk1))     # calculate phiy velocity v(x,y,t)
		psixk1 =  real(ifft(im*Kx.*psihk1))    # calculate ∂psi/∂x
		psiyk1 =  real(ifft(im*Ky.*psihk1))    # calculate ∂psi/∂y
		k2 = -fft(phixk1.*psiyk1 - phiyk1.*psixk1) - nu.*(-ksq.*phihk1+ksq.*psihk1)+vu.*fft(phiyk1)
		
		psihk2 = psih + dt*k2/2.0
		phihk2 = invksq.*psihk2
		phixk2 = real(ifft(im*Kx.*phihk2))     # calculate phix velocity u(x,y,t)
		phiyk2 = real(ifft(im*Ky.*phihk2))     # calculate phiy velocity v(x,y,t)
		psixk2 =  real(ifft(im*Kx.*psihk2))    # calculate ∂psi/∂x
		psiyk2 =  real(ifft(im*Ky.*psihk2))    # calculate ∂psi/∂y
		k3 = -fft(phixk2.*psiyk2 - phiyk2.*psixk2) - nu.*(-ksq.*phihk2+ksq.*psihk2)+vu.*fft(phiyk2)
		
		psihk3 = psih + dt*k3
		phihk3 = invksq.*psihk3
		phixk3 = real(ifft(im*Kx.*phihk3))     # calculate phix velocity u(x,y,t)
		phiyk3 = real(ifft(im*Ky.*phihk3))     # calculate phiy velocity v(x,y,t)
		psixk3 =  real(ifft(im*Kx.*psihk3))    # calculate ∂psi/∂x
		psiyk3 =  real(ifft(im*Ky.*psihk3))    # calculate ∂psi/∂y
		
		k4 =  -fft(phixk3.*psiyk3 - phiyk3.*psixk3) - nu.*(-ksq.*phihk3+ksq.*psihk3)+vu.*fft(phiyk3)

		#println(rhs)
	    psih = psih + (dt/6)*(k1+2*k2+2*k3+k4)         # time-step forward using the simplest Euler scheme
		phih = invksq.*psih
	    psi = real(ifft(psih))
		

		
		
		if any(isnan, psi)
			println("Entrou")
			 println(j)
			 #println(phibk)
			 break
		 end

	
	end
	time = tfin
	phih = invksq.*psih               # calculate \hat{ψ}
	phi = real(ifft(phih))
	phix = real(ifft(im*Kx.*phih))     # calculate phix velocity u(x,y,t)
	phiy = real(ifft(im*Ky.*phih))     # calculate phiy velocity v(x,y,t)
	
	pcolormesh(X, Y, phi)
	colorbar()
	quiver(X[1:nc:end,1:nc:end], Y[1:nc:end,1:nc:end], -1 .*phix[1:nc:end,1:nc:end], -1 .*phiy[1:nc:end,1:nc:end])
	xlabel(L"x")
	ylabel(L"y")
	title(string("Potencial & E at t=", time))
	draw()
	axis("square");
	savefig("HMF.png")


	tempo = 0
	dt = 0.1
	for i in 1:1000
		npx = npos[1]+ 20.0*real(-ifft(-im*Ky.*phih))[mindist2(x,npos[1]),mindist2(y,npos[2])]*dt
		npy = npos[2]+ 20.0*real(ifft(im*Kx.*phih))[mindist2(x,npos[1]),mindist2(y,npos[2])]*dt
		nvx =0#  real(ifft(-im*Ky.*phih))[mindist2(x,npx)]	
		nvy = 0# real(ifft(im*Kx.*phih))[mindist2(y,npy)]
		
		npos = [mod(npx,2*pi),mod(npy,2*pi)]
		nv = [nvx,nvy]
		#println( real(ifft(im*Ky.*phih))  )
		pos = hcat(pos,npos)
		v = hcat(v,nv)
		end
#=

	#println(phiy)
	npx = npos[1]+nv[1]*dt
	npy = npos[2]+nv[2]*dt
	nvx = nv[1]	+ dt*real(ifft(-im*Ky.*phih))[mindist2(x,npx)]	
	nvy = nv[2]	+ dt*real(ifft(im*Kx.*phih))[mindist2(y,npy)]

	npos = [npx,npy]
	nv = [nvx,nvy]
	pos = hcat(pos,npos)
	v = hcat(v,nv)
=#
	#clf()
#=
	pcolormesh(X, Y, phi)
	colorbar()
	quiver(X[1:nc:end,1:nc:end], Y[1:nc:end,1:nc:end], -1 .*phix[1:nc:end,1:nc:end], -1 .*phiy[1:nc:end,1:nc:end])
	xlabel(L"x")
	ylabel(L"y")
	title(string("Potencial & E at t=", time))
	draw()
	axis("square");
	savefig("HMF.png")
=#
pplot = transpose(pos)
mpplot = mod.(pplot,2*pi)
#print(pplot[:,1])
writedlm("Poth.csv",phih,"\t")
writedlm("File.csv",pplot,"\t")
writedlm("v.csv",transpose(v),"\t")
plot(mpplot[:,1],mpplot[:,2])
draw()
savefig("part.png")
end
main()
