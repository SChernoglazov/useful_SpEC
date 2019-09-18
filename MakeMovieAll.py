#!/usr/bin/env python3

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pylab as py
import os, glob
import sys

from pylab import zeros,log10,linspace
from pylab import figure,clf,rcParams,FixedLocator,subplot,contourf,axis

# File options
horOrVert = 'hor'
filedir = os.getcwd() + "/"
outputdir = filedir

dirs=glob.glob("Lev*")
dirs.sort()
print(dirs)

prefix1 = "b2"
prefix2 = "Density"

SkipToStep = 0
Fscale = 1.
F0 = 1.e-17
colouraxis1 = zeros([100])
colouraxis2 = zeros([100])
useLog = 1
coeff=-1
low1=-16
added1=7
low2=-9
added2=7

for i in range(0, 100):
    colouraxis1[i] = low1+float(i)*added1/99
    colouraxis2[i] = low2+float(i)*added2/99

i=0

LegendTag = [-16,-14,-12,-10,-8,-6,-4,-2,0,2,4,6,8,10,12,14]
LegendName1 = "$\\log_{10}(b_2)$"
LegendName2 = "$\\log_{10}(\\rho)$"

cmapname = 'inferno'

# Plotting options
XMin = -56.
XMax = 56.
if horOrVert == 'hor':
    YMin = -56.
    YMax = 56.0
elif horOrVert == 'vert':
    YMin = -3.36
    YMax = 3.36
bgcolor = 'black'

                                  
# Function calibrated for SliceData in SpEC                                                                                                                                   
def ReadMagneticEnergy(filename):
    f=open(filename,'r')
    out = []
    x = []
    y = []
    for line in f:
        row = [float(i) for i in line.split()]
        out.append(row)
        x.append(row[0])
        y.append(row[1])
    return x,y

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

MagName=filedir+"JoinedL1/MatterObservers/MagneticEnergy.dat"
XMag,YMag =ReadMagneticEnergy(MagName)

for file in dirs:
    currentdir= filedir+file+"/Run/SliceData/"
    filepath1 = currentdir+prefix1+"_"+horOrVert+".dat"
    filepath2 = currentdir+prefix2+"_"+horOrVert+".dat"
    print("Get file dimensions of", file)
    Nt,Nx,Ny = GetSliceDims(filepath1)
    print(Nt,Nx,Ny)

    # Plotting...
    #figure(figsize=(24,24))
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

    f1 = open(filepath1,'r')
    f2 = open(filepath2,'r')


    if SkipToStep>0:
        Nskip = SkipToStep*(Nx+1)*Ny
        Buff1 = [next(f1) for x in range(Nskip)]
        Buff2 = [next(f2) for x in range(Nskip)]
    
    line1 = f1.readline()
    str_input = line1.split()
    NextTime1 = float(str_input[1])
    print(NextTime1)
    for t in range(SkipToStep,Nt):
        LastTime = NextTime1
        print("Stamp ",t," at time ",LastTime)
        mData1,NextTime1 = GetNextSlice(f1,Nx,Ny)
        mData2,NextTime2 = GetNextSlice(f2,Nx,Ny)
        while(NextTime1 != 'NaN' and NextTime1 <= LastTime):
            print("Skipping stamp ",t," at time ",NextTime)
            mDummy1, NextTime1 = GetNextSlice(f1,Nx,Ny)
            mDummy2, NextTime2 = GetNextSlice(f2,Nx,Ny)
            t = t+1
        
        X1 = mData1[:,:,0]*1.475
        Y1 = mData1[:,:,1]*1.475
        Z1 = mData1[:,:,2]*1.475
        F1 = mData1[:,:,3] 
        
        X2 = mData2[:,:,0]*1.475
        Y2 = mData2[:,:,1]*1.475
        Z2 = mData2[:,:,2]*1.475
        F2 = mData2[:,:,3]
        
        #    fig, axes  = plt.subplots(nrows=2, ncols=2)
        
        fig = plt.figure()
        fig.set_size_inches((40,24))
        ax1 = plt.subplot2grid((3,4),(0,0), colspan=2, rowspan=2)
        ax2 = plt.subplot2grid((3,4),(0,2), colspan=2, rowspan=2)
        ax3 = plt.subplot2grid((3,4),(2,1), colspan=2)
        #    ax1 = fig.add_subplot(2,2,1)
        #    ax2 = fig.add_subplot(2,2,2)
        #    ax3 = fig.add_subplot(2,1,2)
            
        if horOrVert == 'vert':
            im2 = contourf(X1, Z1, log10(F1+F0), colouraxis1,cmap=cmapname)
            im3 = contourf(X2, Z2, log10(F2+F0), colouraxis2,cmap=cmapname)
        elif horOrVert == 'hor':
            im2 = ax1.contourf(X1, Y1, log10(F1+F0), colouraxis1,cmap=cmapname)
            im3 = ax2.contourf(X2, Y2, log10(F2+F0), colouraxis2,cmap=cmapname)

        ax1.set_xlabel("$X [km]$",fontsize=36,color=bgcolor)
        ax1.set_ylabel("$Y [km]$",fontsize=36,color=bgcolor)
        
        ax2.set_xlabel("$X [km]$",fontsize=36,color=bgcolor)
        ax2.set_ylabel("$Y [km]$",fontsize=36,color=bgcolor)

        #    dt = LastTime*0.00496
        dt = LastTime
        titlestring = "t - $t_{\\rm merge}$ = %.02f ms" % (dt)
        ax1.set_title(titlestring,fontsize=36,color=bgcolor)
        ax2.set_title(titlestring,fontsize=36,color=bgcolor)
        
        #    ax = plt.gca()
        ax1.xaxis.set_major_locator(majorLocatorX)
        ax1.xaxis.set_minor_locator(minorLocatorX)
        ax1.xaxis.set_ticklabels(Xlab,fontsize=32,color=bgcolor)
        ax1.xaxis.set_tick_params(which='minor', length=5, width=2)
        ax1.xaxis.set_tick_params(which='major', width=3,length=10)
        ax1.yaxis.set_major_locator(majorLocatorY)
        ax1.yaxis.set_minor_locator(minorLocatorY)
        ax1.yaxis.set_ticklabels(Ylab,fontsize=32,color=bgcolor)
        ax1.yaxis.set_tick_params(which='minor', length=5, width=2)
        ax1.yaxis.set_tick_params(which='major', width=3,length=10)
        ax1.set(xlim=(XMin,XMax), ylim=(YMin,YMax))
            
        ax2.xaxis.set_major_locator(majorLocatorX)
        ax2.xaxis.set_minor_locator(minorLocatorX)
        ax2.xaxis.set_ticklabels(Xlab,fontsize=32,color=bgcolor)
        ax2.xaxis.set_tick_params(which='minor', length=5, width=2)
        ax2.xaxis.set_tick_params(which='major', width=3,length=10)
        ax2.yaxis.set_major_locator(majorLocatorY)
        ax2.yaxis.set_minor_locator(minorLocatorY)
        ax2.yaxis.set_ticklabels(Ylab,fontsize=32,color=bgcolor)
        ax2.yaxis.set_tick_params(which='minor', length=5, width=2)
        ax2.yaxis.set_tick_params(which='major', width=3,length=10)
        ax2.set(xlim=(XMin,XMax), ylim=(YMin,YMax))
        #    axis([XMin, XMax, YMin, YMax])
    
        ax3.plot(XMag,YMag)
        ax3.axvline(x=dt, color='k', linestyle='--')
        ax3.set_title("Magnetic energy",fontsize=36,color=bgcolor)
        ax3.set_xlabel("time",fontsize=36,color=bgcolor)
        ax3.set_ylabel("$b^2$",fontsize=36,color=bgcolor)
        #   cbar_ax2 = fig.add_axes([0.55, 0.15, 0.03, 0.4])
        cbar1 = fig.colorbar(im2, ticks=LegendTag, ax=ax1)
        cbar1.set_label(label=LegendName1,fontsize=36,color=bgcolor)
        cbar2 = fig.colorbar(im3, ticks=LegendTag, ax=ax2)
        cbar2.set_label(label=LegendName2,fontsize=36,color=bgcolor)

        outputname = outputdir+"slice/everything"+"%04d"%i+".png"
        i=i+1
        plt.savefig(outputname)
        plt.close(fig)
    f1.close()
    f2.close()

