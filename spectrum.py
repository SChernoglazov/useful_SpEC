import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pylab as py
import os
import sys

from pylab import zeros
from pylab import figure,clf,rcParams,FixedLocator,subplot,contourf,axis

def GetSliceDims(filename):
    f = open(filename,'r')
    Nx = 0
    Ny = 0
    ReadHeader = 0
    while True:
        line = f.readline()
        if line == '':
            Ny = Ny+1
            print("Reached end of file.")
            break
        elif line[0]=='#':
            if ReadHeader > 0:
                Ny = Ny+1
                break
            ReadHeader = 1
        else:
            str_input = line.split()
            if len(str_input)==4:
                Nx = Nx+1
            else:
                Ny = Ny+1
                Nx = 0  
    f.close()
    print("Nx=", Nx, "Ny=",Ny)
    return [Nx,Ny]

def GetNextSlice(filename,Nx,Ny):
    f = open(filename,'r')
    mOutput = zeros([Ny,Nx,4])
    line = f.readline()
    while line[0]=='#':
        line = f.readline()
    for j in range(0,Ny):
        for i in range(0,Nx):
            str_input = line.split()
            if len(str_input)!=4:
                print("Bad format in GetNextSlice",line,j,i)
                break
            else:
                for k in range(0,4):
                    mOutput[j,i,k] = float(str_input[k])
            line = f.readline()                                                                                                                                           
        if j<Ny-1:
            line = f.readline()
    if(len(line)>0):
        str_input = line.split()
    return mOutput


nIntervals = 256 ## (r_max - r_min)/delta_r
print("Get file dimensions")
filename= 'b2fine_hor.dat' 
Nx,Ny = GetSliceDims(filename)
mData = GetNextSlice(filename, Nx, Ny)

EnArray=zeros([Ny,Nx])
for i in range (Ny): 
    for j in range (Nx):
        EnArray[i,j]=np.sqrt(mData[i,j,3])

EnKreal=np.fft.fft2(EnArray)

EnK=np.abs(np.fft.fft2(EnArray))


EnKradial=zeros([Ny*Ny,2])
Kradius=zeros([Ny*Ny])

ExpFactor = 0.3907

for i in range (Ny): 
    for j in range (Ny):
        rad=np.sqrt(float(i*i+j*j)) /(Ny*ExpFactor)
        EnKradial[i*Ny+j,0]=rad
        EnKradial[i*Ny+j,1]=EnK[i,j]
        Kradius[i*Ny+j] = rad

Kradius.sort()
dK=float(Kradius[-1]-Kradius[0])/(nIntervals-1)

print(dK)

EnEqDistributed=zeros([nIntervals])
RadEqDistributed=zeros([nIntervals])
for i in range (Ny*Ny):
    j=int(EnKradial[i][0]//dK)+1
    RadEqDistributed[j]=j*dK/18000
    EnEqDistributed[j]+=(EnKradial[i][1]**2)*EnKradial[i][0]


plt.loglog(RadEqDistributed, EnEqDistributed)
#plt.loglog(EnEqDistributed)
plt.ylabel('b2')
plt.xlabel('k_xy/2pi (cm^-1)')
plt.savefig("spectrum.png")
plt.show()
    
