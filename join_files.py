import glob, os
os.chdir(".")
wrNS=open("NS-trajectory.dat","w")
dirs=glob.glob("Lev*")
dirs.sort()
print(dirs)
print ("NS trajectory")
for file in dirs:
    if os.path.isdir(file+"/Run"):
        print(file)
        name=str(os.getcwd())+"/"+file+"/Run/MatterObservers/InertialCenterOfMass.dat"
        f=open(name,"r")
        for line in f:
            coords=line.split()
            if len(coords) == 4 and coords[0]!='#':
                wrNS.write(line)
        f.close()
    else:
        print "directory", file, "doesn't have Run subdirectory"
wrNS.close()
print("\n\n")


wrBH=open("BH-trajectory.dat","w")
print("BH trajectory")
for file in dirs:
    if os.path.isdir(file+"/Run"):
        print(file)
        name=str(os.getcwd())+"/"+file+"/Run/ApparentHorizon/Trajectory_AhA.dat"
        f=open(name,"r")
        for line in f:
            coords=line.split()
            if len(coords) == 4 and coords[0]!='#':
                wrBH.write(line)
        f.close()
    else:
        print "directory", file, "doesn't have Run subdirectory"
wrBH.close()


