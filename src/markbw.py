
import os
import math
import src.readWM as readWM
from oct2py import octave
from PIL import Image
import numpy as np


def markbw(mode) :

    # DEFAULT VALUES
    L = 200
    rDef = 175
    alphaDef = 5
    imPath = "/Users/tania.diaz/Documents/Personal/k0v4l3vsk4y4/WM-based-on-DFT/imatges/degas_2gray.png"
    wmPath = "/Users/tania.diaz/Documents/Personal/k0v4l3vsk4y4/WM-based-on-DFT/marques/marca23.txt"    
    imDef = 10000; # def imatges (nomes serveix x mostrar visualment els coef de mag)
    complexi = 1j

    if (mode):
        # Llegeix path de la imatge
        imPath = input("Image path: ")

        # Comprova si el directori es valid i llegeix la imatge
        if not os.path.isfile(imPath):
            raise ValueError(f"Directory {imPath} is not valid.")
    

    try:
        im = Image.open(imPath).convert('L')
    except:
        im = Image.open(imPath)

    im = np.array(im)   
    imPath, extension = os.path.splitext(imPath)

    r = input("Give me the radius. If the value given is not an integer, a default value will be selected. \nRadius: ")
    
    # Comprova si és un nombre enter, si no es queda amb el valor per defecte
    try:
        r = int(r)
    except ValueError:
        r = rDef
        print("The value entered is not an integer. A default value will be assigned instead.\nRadius: ", r)

    # Comprova que el radi és factible amb la imatge donada. 
    m,n = im.shape
    m=m-1 # Per referenciar bé la posició dins de la matriu
    n=n-1 # Per referenciar bé la posició dins de la matriu

    if r >= min(m,n) / 2 :
        print("Invalid radius. Select another image or a smaller radius.", r)
        exit

    # Llegeix variable alpha
    alpha = input("Give me the alpha. If the value given is not an integer, a default value will be selected. \nAlpha: ")
    
    # Comprova si és un nombre enter, si no es queda amb el valor per defecte
    try:
        alpha = int(alpha)
    except ValueError:
        alpha = alphaDef
        print("The value entered is not an integer. A default value will be assigned instead.\nAlpha: ", alpha)

    if (mode):
        # Llegeix path de la marca
        wmPath = input("Give me the path  of the txt file that contains the mark. Mark path: ")

        # Comprova si el directori es valid i llegeix la imatge
        if not os.path.isfile(wmPath):
            raise ValueError(f"Directory {wmPath} is not valid.")
    
    # Llegim la marca
    v = readWM.readWM(wmPath)



    # Transformo la imatge al domini de Fourier
    imDFT = octave.fft2(im); 
    imDFTshift = octave.fftshift(imDFT); # Traslladem els coeficients de baixa freqüència al centre

    # Separem els coeficients de magnitud dels coeficients de fase
    coefMag = octave.abs(imDFTshift) # Mòdul o magnitud complexa 
    coefPhase = octave.angle(imDFTshift) # Angle de fase

    # Definim marca
    wm = octave.zeros (octave.size(coefMag))

    for k in range(1,L+1) :
        # Marca L punts distribuïts uniformemente entre [-pi,pi] (comença per -pi!) en el radi r
        x = math.trunc(m/2+1) + math.trunc(r*math.cos(k*math.pi/L))
        y = math.trunc(n/2+1)+math.trunc(r*math.sin(k*math.pi/L))
        
        for s in range(-1,2):
            for t in range (-1,2):
                wm[x][y]= wm[x][y] + coefMag[x+s][y+t]
            
        wm[x][y]  = v[k-1]*wm[x][y] /9
    

    # Omple el costat esquerra de la matriu amb simetria inversa
    for i in range (1,m+1) : 
        for j in range (1,int(n/2)+1):
            wm[i][j] = wm[m-i][n-j]

    # Incrustem la marca en la matriu
    coefMagWM = coefMag + alpha * wm

    # Combinem els coeficients de magnitud amb els coeficients de fase
    imDFTwm = octave.zeros(octave.size(coefMagWM))
    imDFTwm = coefMagWM*octave.exp(complexi*coefPhase)


    # Transforma de nou al domini espacial (Inverteix la transformada de Fourier)
    imWM = octave.ifft2(octave.ifftshift(imDFTwm)); 
    imWM = octave.uint8(octave.real(imWM))

    # Guarda la imatge
    fileName = imPath+"_L"+str(L)+"_r"+str(r)+"_alpha"+str(alpha)+".png"
    imagen = Image.fromarray(imWM.astype('uint8'))
    imagen.save(fileName)
