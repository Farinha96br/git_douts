import MDSplus as mds
import matplotlib.pyplot as plt

## SHOTS INPORTANTES
# 33770 descarga pra fazer o espectro S(k,)


shot_number = 32556

# "RP18PVR"     Para tensão aplicada (ou potencial flutuante) nas sondas (até 8 sinais)
# "RP18PIR"   Para corrente nas mesmas até 8 sondas
# "RP18PVF"   Para potencial flutuante em sondas extras.

# DO SCRIPT DO MATLAB

#   Assim, no matlab, os dados de potencial flutuante (ou tensão aplicada) da primeira sonda por
#   v = mdsvalue('\TCABR_NI01::TOP.ACQSIGNALS.RP18PVR1.signal');

#   os dados da corrente de saturação iônica da oitava sonda podem ser obtidos por
#   i = mdsvalue('\TCABR_NI01::TOP.ACQSIGNALS.RP18PIR8.signal');

#   e os dados de potencial flutuante da quarta sonda extra por
#   v = mdsvalue('\TCABR_NI01::TOP.ACQSIGNALS.RP18PVF4.signal');


fig, ax = plt.subplots(8,1)
for i in range(0,8):
    istr = str(i+1)
    conn = mds.Connection('tcabrcl.if.usp.br:8000')     # connect to the MDSplus server
    conn.openTree('tcabr_shot', shot_number)            # Open the "tcabr_shot" experiment (set of signals), of a specific shot
    ip = conn.get('\\RP18PVF' + istr + '.signal').data()            # get the plasma current signal
    t  = conn.get('DIM_OF(\\RP18PVF' + istr + '.signal)').data()    # get the plasma current time axis
    ip_label = conn.get('UNITS_OF(\\RP18PVF' + istr + '.signal)').data()
    t_label  = conn.get('UNITS_OF(DIM_OF(\\RP18PVF' + istr + '.signal))').data()
    conn.closeAllTrees()

    ax[i].plot(t, ip, lw = 0.5, c = "black")
    ax[i].set_ylabel(ip_label)
    ax[i].set_ylim(-100,100)


    if i != 7:
        ax[i].set_xticks([])
    if i != 3:
        ax[i].set_xlabel(" ")


plt.show()
