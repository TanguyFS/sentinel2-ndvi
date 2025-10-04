# -*- coding: utf-8 -*-
"""
Created on Sat Oct  4 13:00:52 2025

@author: Tanguy
"""
from matplotlib.colors import ListedColormap, BoundaryNorm
from pathlib import Path     
import rasterio              
import numpy as np            
import matplotlib.pyplot as plt  
plt.close('all')

day = "2025-09-30" #date du jour choisi pour les données 


base = Path(r"C:\Users\Tanguy\Documents\s2")  #chemin du dossier de travail
data = base / "data" #chemin des données
out  = base / "outputs" #chemin des résultats 

'''
for f in data.rglob(day+"*.tif*"):
    print(f.name)'''
  
    
########### Calcul de b04
  
    
b04 = next(data.rglob(day + "*b04*.tiff"),None) #permet de choisir le fichier b04 s'il existe 

if b04 is None:
    print("Aucun fichier B04 trouvé pour cette date.")
else:
    print("Fichier trouvé :", b04.name)

    
    
with rasterio.open(b04) as src : 
    #print(src.meta) #affiche les informations du fichier
    b04_data = src.read(1)

#print(b04_data.maxn()) #permet de voir si c'est codé sur 65535 ou 10000
b04_norm = b04_data/65535 #normalisation entre 0 et 1
#print(b04_norm)
    
plt.figure()
plt.title("Map dans la bande b04")
plt.imshow(b04_norm, cmap='Reds')
plt.colorbar(label = "Réflectance (0-1)")
plt.show()


########### Calcul de b08 

    
b08 = next(data.rglob(day + "*b08*.tiff"),None) #permet de choisir le fichier b08 s'il existe 

if b08 is None:
    print("Aucun fichier B08 trouvé pour cette date.")
else:
    print("Fichier trouvé :", b08.name)

    
with rasterio.open(b08) as src : 
    #print(src.meta) #affiche les informations du fichier
    b08_data = src.read(1)

#print(b04_data.maxn()) #permet de voir si c'est codé sur 65535 ou 10000
b08_norm = b08_data/65535 #normalisation entre 0 et 1
#print(b08_norm)
    
plt.figure()
plt.title("Map dans la bande b08")
plt.imshow(b08_norm, cmap='gray')
plt.colorbar(label = "Réflectance (0-1)")
plt.show()


########### Calcul et affichage de NVDI

breaks = [-1, -0.5, 0, 0.025, 0.05, 0.075, 0.10, 0.125, 0.175, 0.20, 0.25, 0.40, 1.0]
hex_colors = [
    "#0c0c0c",  # NDVI < -0.5
    "#bfbfbf",
    "#eaeaea",
    "#fffacc",
    "#fffefa",
    "#bcb76b",
    "#ccc782",
    "#bdb86b",
    "#a3cc59",
    "#91bf51",
    "#81b347",
    "#81b347",
    "#004500",  # NDVI -> 1
]

cmap = ListedColormap(hex_colors)
norm = BoundaryNorm(breaks, cmap.N, clip=True)

print("B04 shape:", b04_norm.shape, " | B08 shape:", b08_norm.shape)

eps = 1e-12
ndvi =(b08_norm - b04_norm)/(b08_norm+b04_norm+eps)
ndvi = np.clip(ndvi, -1, 1)

plt.figure()
im = plt.imshow(ndvi, cmap=cmap, norm=norm)  # vert = végétation
plt.colorbar(im, label="NDVI (-1 à 1)")
plt.title(f"NDVI – {day}")
plt.axis("off")
plt.show()


########### comparaison NVDI 







ndvi_cop = next(data.rglob(day + "*NDVI*.tiff"),None) #permet de choisir le fichier NVDI s'il existe 

if ndvi_cop is None:
    print("Aucun fichier B08 trouvé pour cette date.")
else:
    print("Fichier trouvé :", ndvi_cop.name)

    
with rasterio.open(ndvi_cop) as src : 
    #print(src.meta) #affiche les informations du fichier
    ndvi_cop_data = src.read(1)
print(ndvi_cop_data.min(), ndvi_cop_data.max())
ndvi_cop_data = ndvi_cop_data*2/65535 -1
    
plt.figure()
plt.title("NDVI exemple")
plt.imshow(ndvi_cop_data, cmap=cmap, norm=norm)
plt.colorbar(label = "NDVI (-1 à 1)")
plt.show()


diff = ndvi - ndvi_cop_data

plt.figure()
plt.imshow(diff, cmap="bwr", vmin=-0.2, vmax=0.2)
plt.title("Différence NDVI (Mon calcul - Copernicus)")
plt.colorbar(label="Δ NDVI")
plt.show()



























