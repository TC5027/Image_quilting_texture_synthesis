#!/usr/bin/env python3

from PIL import Image
import numpy as np
import sys

""" traitement des arguments """
entree = sys.argv[1]
sortie = sys.argv[2]
M,nb_etapes_ligne,nb_etapes_colonne = [int(parametre) for parametre in sys.argv[3:]]

inputpil = Image.open(entree)
input = np.asarray(inputpil)[:256,:256] #On ne travaille qu'avec une image de taille maximale 256*256

from Coupe import coupe
from Selection import selection

shared_size = 6
patch_size = 32

output = np.zeros(((patch_size-shared_size)*(nb_etapes_colonne-1) + patch_size,(patch_size-shared_size)*(nb_etapes_ligne-1) + patch_size,3))
origin_from_input = np.zeros(((patch_size-shared_size)*(nb_etapes_colonne-1) + patch_size,(patch_size-shared_size)*(nb_etapes_ligne-1) + patch_size,2),dtype = np.uint8)


list_j = list((patch_size-shared_size)*k for k in range(1,nb_etapes_ligne))
list_i = list((patch_size-shared_size)*k for k in range(nb_etapes_colonne))

""" On initialise output en haut à gauche """
output[:patch_size,:patch_size] = input[:patch_size,:patch_size]
origin_from_input[:patch_size,:patch_size] = np.array([[(i,j) for j in range(patch_size)] for i in range(patch_size)])
""" Et on est parti ! """
for i in list_i:
    if i != 0:
        position = (i,0)
        x,y = selection(input,output,origin_from_input,position,patch_size,shared_size,M)
        coupe(input,output,origin_from_input,x,y,position,shared_size,patch_size)
    for j in list_j:
        position = (i,j)
        x,y = selection(input,output,origin_from_input,position,patch_size,shared_size,M)
        coupe(input,output,origin_from_input,x,y,position,shared_size,patch_size)


image=np.uint8(output)

nouvelle_imgpil = Image.fromarray(image)
nouvelle_imgpil.save(sortie)
