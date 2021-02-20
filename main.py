import scipy.io
import matplotlib.pyplot as plt
import numpy as np




def obliczanko_dystansu(x1, y1, x2, y2):
    d=np.sqrt((x1-x2)**2+(y1-y2)**2)
    return d


def algorytm_szukania(x,y,z,x_punktu,y_punktu,liczba_punktow):
    obszar =0.05
    liczba_wymaganych_punktow = 0
    while(liczba_wymaganych_punktow<=liczba_punktow):
        spr_iksy = []
        spr_igreki = []
        spr_zety =[]
        obszar = obszar*2
        minX = x_punktu - obszar
        maxX = x_punktu + obszar
        minY = y_punktu - obszar
        maxY = y_punktu + obszar

        for i in range(len(x)):
            if(((x[i] >= minX) & (x[i] <= maxX) )& ((y[i] >= minY)& (y[i] <= maxY))):
                spr_iksy.append(x[i])
                spr_igreki.append(y[i])
                spr_zety.append(z[i])
        liczba_wymaganych_punktow = len(spr_iksy)

    wagi = []
    #kod liczenia wagi odleglosci
    for j in range(len(spr_iksy)):
        d =obliczanko_dystansu(x_punktu, y_punktu, spr_iksy[j], spr_igreki[j])
        if (d ==0):
            wagi.append(0)
        else:
            waga = 1/(d*d)
            wagi.append(waga)
    if (0 in wagi):
        #sprawdzan czy nie trafilem przypadkiem w zadany punkt
        idx = wagi.index(0)
        z_idw = spr_zety[idx]
    else:
        wt = np.transpose(wagi)
        z_idw = np.dot(spr_zety, wt) / sum(wagi)
    return z_idw


if __name__ == '__main__':
    mat = scipy.io.loadmat('data_map.mat')
    data = mat["data_map"]

    #algorytm interpolacji bazowany na  https://www.geodose.com/2019/09/3d-terrain-modelling-in-python.html

    iksy = data[:,0]
    igreki = data[:,1]
    zety = data[:,2]
    fig = plt.figure()
    ax = fig.add_subplot(111,projection = '3d')

    mX = max(iksy)
    miX = min(iksy)
    mY = max(igreki)
    miY = min(igreki)

    X = np.arange(miX,mX,((mX-miX)/91))
    Y = np.arange(miY, mY, ((mY - miY) / 91))
    X1,Y1 = np.meshgrid(X,Y)


    zety1 = np.zeros((len(X1),len(Y1)))

    nowe_zety = []

    for i in range(len(X1)):
        for j in range(len(Y1)):
            nowe_zety.append(algorytm_szukania(iksy,igreki,zety,X[i],Y[j],3))
        print(f"[{i}/{len(X1)}]")
    nowe_zety = np.array(nowe_zety)

    ax.scatter(X1,Y1,nowe_zety,c=nowe_zety,s=1)

    plt.show()
