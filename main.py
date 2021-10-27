import environment, variables, processing
from os import path
from tools import counter

workfolder = r'D:\My_files\Meus_artigos\Em_andamento\Artigo_de_solos_2019\Projetos\TOPODATA'
DEM = path.join(workfolder, 'dem.tif')
soil_obs = path.join(workfolder, 'OBS_SOIL.shp')
basins = None   # path.join(workfolder, 'watersheds.tif')

e = environment.setup(workfolder, DEM, soil_obs, basins)
i = variables.initialize(e)
c = counter.count(DEM)
d = 0
while True:
    q = raw_input("Which one do you prefer to use? (0=relative; 1=absolute; 2=cancel): ")
    if q == "0":
        px = int((float(raw_input("Enter the percentage of data to use (%): "))/100) * c.data)
    elif q == "1":
        px = int(raw_input("Enter the number of data pixels to use: "))
    elif q == "2":
        px = 0
        break
    if q in ["0", "1"]:
        print "Using %s pixels to process..." % (px)
        d = raw_input("Is that correct? (0=NO; 1=YES; 2=cancel): ")
        if d == "1":
            break
        elif d == "2":
            px = 0
            break
if px > 0:
    processing.start(i, e, n=px)