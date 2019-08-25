#!/usr/bin/env python3

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pylab as py
import os
import sys

from pylab import zeros,log10,linspace,sin,cos
from pylab import figure,clf,rcParams,FixedLocator,subplot,contourf,axis

# File options
horOrVert = 'hor'
filedir = os.getcwd() + "/"
outputdir = filedir

if len(sys.argv) != 3:
    print("Need two arguments.")
    print("./"+sys.argv[0]+" <prefix> <offset>")
    exit()

prefix = sys.argv[1]
offset = int(sys.argv[2])

filepath = filedir+prefix+"_"+horOrVert+".dat"
SkipToStep = 0
FilePrefix = prefix+"_"+horOrVert
Fscale = 1.
F0 = 0
colouraxis = zeros([100])
useLog = 0
coeff=1
low=-1
added=0

if useLog:
    for i in range(0, 100):
        colouraxis[i] = low+i*added/99.
else:
    for i in range(0,100):
        colouraxis[i] =5 + float(i)*40/99


if useLog:
    LegendTag = [-16,-14,-12,-10,-8,-6,-4,-2,0,2,4,6,8,10,12,14]
    LegendName = "$\\log_{10}(b2)$"
else:
    LegendTag = [5,10,15,20,25,30,35,40]
    LegendName = "$MRI$"
cmapname = 'inferno'

# Plotting options
XMin = -100.
XMax = 100.
if horOrVert == 'hor':
    YMin = -100.
    YMax = 100.0
elif horOrVert == 'vert':
    YMin = -100
    YMax = 100
bgcolor = 'black'

                                  
# Function calibrated for SliceData in SpEC                                                                                                                                   
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
    f = open(filename,'r')
    Nt = 0
    Nc = 0
    for line in f:
        Nc = Nc+1
        if Nc == (Nx+1)*Ny :
            Nc = 0
            Nt = Nt+1
    print("Nt=",Nt, "Nx=", Nx, "Ny=",Ny)
    return [Nt,Nx,Ny]

def GetNextSlice(f,Nx,Ny):
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
        # SpEC skips one line when indexing non-leading index
        if j<Ny-1:
            line = f.readline()
    if(len(line)>0):
        str_input = line.split()
        NextTime = float(str_input[1])
    else:
        NextTime = 'NaN'
    return mOutput,NextTime


print("Get file dimensions")
Nt,Nx,Ny = GetSliceDims(filepath)
print(Nt,Nx,Ny)

# Plotting...
figure(figsize=(12,12))
clf()
# Set plot parameters to make beautiful plots
minorLocatorX   = FixedLocator(linspace(XMin,XMax,5))
minorLocatorY   = FixedLocator(linspace(YMin,YMax,21))
majorLocatorX   = FixedLocator(linspace(XMin,XMax,5))
majorLocatorY   = FixedLocator(linspace(XMin,XMax,5))
dX = (XMax-XMin)/4.
Xlab = ["%.0f"%XMin,"%.0f"%(XMin+dX),"%.0f"%(XMin+2*dX),"%.0f"%(XMin+3*dX),"%.0f"%XMax]
dY = (YMax-YMin)/4.
Ylab = ["%.0f"%YMin,"%.0f"%(YMin+dY),"%.0f"%(YMin+2*dY),"%.0f"%(YMin+3*dY),"%.0f"%YMax]

rcParams['figure.figsize']  = 12, 12
rcParams['lines.linewidth'] = 1.5
rcParams['font.family']     = 'serif'
rcParams['font.weight']     = 'bold'
rcParams['font.size']       = 30
rcParams['font.sans-serif'] = 'serif'
rcParams['text.usetex']     = False
rcParams['axes.linewidth']  = 1.5
rcParams['axes.titlesize']  = 'medium'
rcParams['axes.labelsize']  = 'medium'
rcParams['xtick.major.size'] = 8
rcParams['xtick.minor.size'] = 4
rcParams['xtick.major.pad']  = 8
rcParams['xtick.minor.pad']  = 8
rcParams['xtick.color']      = bgcolor
rcParams['xtick.labelsize']  = 'medium'
rcParams['xtick.direction']  = 'in'
rcParams['ytick.major.size'] = 8
rcParams['ytick.minor.size'] = 4
rcParams['ytick.major.pad']  = 8
rcParams['ytick.minor.pad']  = 8
rcParams['ytick.color']      = bgcolor
rcParams['ytick.labelsize']  = 'medium'
rcParams['ytick.direction']  = 'in'
rcParams['axes.linewidth'] = 3

f = open(filepath,'r')
if SkipToStep>0:
    Nskip = SkipToStep*(Nx+1)*Ny
    Buff = [next(f) for x in range(Nskip)]

YawAngle=42.08
PitchAngle=0.0005
ExpansionFactor=0.39
FinestCell=float(120)/float(384)*ExpansionFactor
print(FinestCell)

line = f.readline()
str_input = line.split()
NextTime = float(str_input[1])
for t in range(SkipToStep,Nt):
    LastTime = NextTime
    print("Stamp ",t," at time ",LastTime)
    mData,NextTime = GetNextSlice(f,Nx,Ny)
    while(NextTime != 'NaN' and NextTime <= LastTime):
        print("Skipping stamp ",t," at time ",NextTime)
        mDummy,NextTime = GetNextSlice(f,Nx,Ny)
        t = t+1

    X = mData[:,:,0]*1.475
    Y = mData[:,:,1]*1.475
    Z = mData[:,:,2]*1.475
    F = mData[:,:,3]
    if (horOrVert == 'hor'):
        for i in range(0,Nx):
            for j in range(0,Ny):
                F[i,j] = abs(mData[i,j,3]*Fscale)/(4*FinestCell)
                x=X[i,j]
                y=Y[i,j]
                X1=x*cos(YawAngle)+y*sin(YawAngle)
                Y1=-x*sin(YawAngle)+y*cos(YawAngle)
                if ((abs(X1)<69.03) and (abs(Y1)<69.03)):
                    F[i,j] = abs(mData[i,j,3]*Fscale)/(2*FinestCell)
                if ((abs(X1)<34.515) and (abs(Y1)<34.515)):        
                    F[i,j] = abs(mData[i,j,3]*Fscale)/FinestCell
    if (horOrVert == 'vert'):
        for i in range(0,Nx):
            for j in range(0,Ny):
                F[i,j] = abs(mData[i,j,3]*Fscale)/(4*FinestCell)
                x=X[i,j]
                z=Z[i,j]
                X1=x*cos(PitchAngle)+z*sin(PitchAngle)
                Y1=-x*sin(PitchAngle)+z*cos(PitchAngle)
                if ((abs(X1)<abs(34.515/sin(YawAngle))) and (abs(Y1)<abs(34.514))):
                    F[i,j] = abs(mData[i,j,3]*Fscale)/(2*FinestCell)
                if ((abs(X1)<abs(17.25/sin(YawAngle))) and (abs(Y1)<abs(17.25))):
                    F[i,j] = abs(mData[i,j,3]*Fscale)/(1*FinestCell)

    fig, axes = plt.subplots(nrows=1, ncols=1)
    fig.set_size_inches((12,12))
    sp=subplot(111)
    if useLog == 1:
        if horOrVert == 'vert':
            im2 = contourf(X, Z, log10(F+F0), colouraxis,cmap=cmapname)
        elif horOrVert == 'hor':
            im2 = contourf(X, Y, log10(F+F0), colouraxis,cmap=cmapname)
    else:
        if horOrVert == 'vert':
            im2 = contourf(X, Z, F+F0, colouraxis,cmap=cmapname)
        elif horOrVert == 'hor':
            im2 = contourf(X, Y, F+F0, colouraxis,cmap=cmapname)
    plt.xlabel("$X [km]$",fontsize=36,color=bgcolor)
    plt.ylabel("$Y [km]$",fontsize=36,color=bgcolor)

#    dt = LastTime*0.00496
    dt = LastTime
    titlestring = "t - $t_{\\rm merge}$ = %.02f ms" % (dt)
    plt.title(titlestring,fontsize=36,color=bgcolor)

    ax = plt.gca()
    ax.xaxis.set_major_locator(majorLocatorX)
    ax.xaxis.set_minor_locator(minorLocatorX)
    ax.xaxis.set_ticklabels(Xlab,fontsize=32,color=bgcolor)
    ax.xaxis.set_tick_params(which='minor', length=5, width=2)
    ax.xaxis.set_tick_params(which='major', width=3,length=10)
    ax.yaxis.set_major_locator(majorLocatorY)
    ax.yaxis.set_minor_locator(minorLocatorY)
    ax.yaxis.set_ticklabels(Ylab,fontsize=32,color=bgcolor)
    ax.yaxis.set_tick_params(which='minor', length=5, width=2)
    ax.yaxis.set_tick_params(which='major', width=3,length=10)

    axis([XMin, XMax, YMin, YMax])

    cbar_ax2 = fig.add_axes([0.88, 0.15, 0.03, 0.7])
    cbar2 = fig.colorbar(im2, ticks=LegendTag,cax=cbar_ax2)
    cbar2.set_label(label=LegendName,fontsize=36,color=bgcolor)
    outputname = outputdir+"/"+FilePrefix+"%04d"%(t+offset)+".png"

    plt.subplots_adjust(left=0.15, bottom=0.15, top=0.85, right=0.85)
    plt.savefig(outputname)
    plt.close(fig)

#cmd = "ffmpeg -f image2 -i "+outputdir+FilePrefix+"%04d.jpg -vf scale=1024:1024 -framerate 20 "+outputdir+FilePrefix+".mpg"
#os.system(cmd)
