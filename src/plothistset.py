import os
import math
import src.readWM as readWM
from oct2py import octave
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def covx(x,y):
    covariance_cross = np.correlate(x - np.mean(x), y - np.mean(y),"full" )
    return covariance_cross


def plothistset(mode):
    #VARIABLES DEFAULT
    rMinDef=140 #Valors definits al paper 140
    rMaxDef=180; #Valors definits al paper 180
    imPath = "/Users/tania.diaz/Documents/Personal/k0v4l3vsk4y4/WM-based-on-DFT/imatges/degas_2gray_L200_r175_alpha5.png"
    
    r = 175
    L = 200  #Valor del paper L = 200
    numberfiles = 500

    # DADES IMATGE
    if (mode):
        # Llegeix path de la imatge
        imPath = input("Image path: ")

        # Comprova si el directori es valid i llegeix la imatge
        if not os.path.isfile(imPath):
            raise ValueError(f"Path {imPath} is not valid.")
    
    im = Image.open(imPath)
    im = np.array(im)    
    imPath, extension = os.path.splitext(imPath)

    # DADES RADIS
    rRange = input("Enter the minimum and maximum radius, separated by a space:. If the values given are not integers, defaults values will be selected. \nRadius: ")
    
    # Comprova si és un nombre enter, si no es queda amb el valor per defecte
    try:
        rMinRead, rMaxRead = map(int, rRange.split())
        rMin = int(rMinRead)
        rMax = int(rMaxRead)
    except ValueError:
        rMin = rMinDef
        rMax = rMaxDef
        print("The values entered are not integers. Defaults values will be assigned instead.\nRadius: ", rMin, ", " ,rMax)

    # Comprova que el radi és factible amb la imatge donada. 
    m,n = im.shape
    m=m-1 # Per referenciar bé la posició dins de la matriu
    n=n-1 # Per referenciar bé la posició dins de la matriu


    if rMin >= min(m,n) / 2 or rMax >= min(m,n) / 2:
        print("Invalid radius. Select another image or a smaller radius.", r)
        exit

    # DADES MARCA
    # De moment les marques es llegeixen d'un reporsitori donat

    
    


    #PREPAREM LA IMATGE       

    # DFT
    # Transformo la imatge al domini de Fourier
    imDFT = octave.fft2(im)
    imDFTshift = octave.fftshift(imDFT)

    # EXTRACCIÓ DEL VECTOR
    # Separem els coeficients de magnitud dels coeficients de fase
    coefMag = octave.abs(imDFTshift) # Mòdul o magnitud complexa 
    

    #Extreu els radis
    arrayVectors = np.zeros((rMax-rMin+1,L))
    cont = 0
    for r in range(rMin,rMax+1) :
        aux = np.zeros(L)
        for k in range(1,L+1):
            x = math.trunc(m/2+1)+math.trunc(r*math.cos(k*math.pi/L)) #És possible q estigui llegint el vector del reves
            y = math.trunc(n/2+1)+math.trunc(r*math.sin(k*math.pi/L))
            aux[k-1] = coefMag[x][y] 
        
        arrayVectors[cont,:] = aux
        cont = cont+1

    # Normalitzem els vectors
    arrayNr = np.zeros((rMax-rMin+1,L))
    for k in range (0,rMax-rMin+1):
        arrayNr[k,:] = octave.normalize(arrayVectors[k,:],'range')

    # Comparem els vectors de la imatge amb 100 marques diferents
    arrayCov = np.zeros((rMax-rMin+1,numberfiles))
    for r in range (0,rMax-rMin+1):
        for k in range(1,numberfiles): 
            wmPath = "/Users/tania.diaz/Documents/Personal/k0v4l3vsk4y4/WM-based-on-DFT/marques/marca"+str(k)+".txt"
            
            v = readWM.readWM(wmPath)
            v2 = arrayNr[r,:]

            cov= covx(v, v2)
            arrayCov[r,k-1] = cov.max()


    # Crear la figura y los ejes
    fig, ax = plt.subplots()

    # Configurar límites del eje y
    #ax.set_ylim([0, 8])

    # Ciclo para plotear los datos
    for r in range(0,rMax+1-rMin):
        # Obtener los datos para la covarianza cruzada
        data = arrayCov[r,:]
        
        # Plotear los datos
        ax.plot(data)

    # Agregar una línea horizontal en y = 2.6
    ax.axhline(y=2.6, linestyle='-.', color='blue')

    # Mostrar la figura
    plt.show()
