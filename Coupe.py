#!/usr/bin/env python3
import numpy as np

def diff(rgb1,rgb2):
    """
    différence classique entre valeurs rgb
    """
    return(sum((e1-e2)**2 for e1,e2 in zip(rgb1,rgb2)))

def coupe(input,output,origin_from_input,x,y,position,shared_size,patch_size):
    """
    Etant donné le patch dont le bord haut gauche est positionné en position (l'argument) on va
    trouver la découpe optimale et ensuite positionner les pixels ayant survécu à la découpe dans l'output
    et enfin mettre à jour origin_from_input de par cette ajout de pixel

    poursuite: faire le floutage sur la frontière en utilisant un filtre sur les pixels autour
    """
    patch = input[x:(x+patch_size),y:(y+patch_size)]
    patch_size = len(patch)
    px,py = position

    """
    On commence par la frontière verticale (sauf si on est en début de ligne)

    On construit la matrice de taille patch_size * shared_size avec comme valeur la différence entre les pixels de output et de patch
    """
    if py != 0:
        matrice_differences = np.zeros((patch_size,shared_size))
        for i in range(patch_size):
            for j in range(shared_size):
                matrice_differences[i,j] = diff(patch[i,j],output[px+i,py+j])

        matrice_provenance = np.zeros((patch_size-1,shared_size),dtype = np.int8) #matrice indiquant d'ou vient le précédent dans l'étape de descente de l'algorithme de RO (Bellman)

        for i in range(1,patch_size):
            for j in range(shared_size):
                """ On a 3 cas : tout à gauche ou tout à droite et dans ce cas 2 provenances possibles ou ailleurs et dans ce cas 3 provenances possibles (-1,0,1) """
                if j == 0:
                    if matrice_differences[i-1,j+0] <= matrice_differences[i-1,j+1]:
                        matrice_provenance[i-1,j] = 0
                        matrice_differences[i,j]+=matrice_differences[i-1,j+0]
                    else:
                        matrice_provenance[i-1,j] = 1
                        matrice_differences[i,j]+=matrice_differences[i-1,j+1]
                elif j == shared_size-1:
                    if matrice_differences[i-1,j-1] <= matrice_differences[i-1,j+0]:
                        matrice_provenance[i-1,j] = -1
                        matrice_differences[i,j]+=matrice_differences[i-1,j-1]
                    else:
                        matrice_provenance[i-1,j] = 0
                        matrice_differences[i,j]+=matrice_differences[i-1,j+0]
                else:
                    if matrice_differences[i-1,j-1] <= matrice_differences[i-1,j+0] and matrice_differences[i-1,j-1] <= matrice_differences[i-1,j+1]:
                        matrice_provenance[i-1,j] = -1
                        matrice_differences[i,j]+=matrice_differences[i-1,j-1]
                    elif matrice_differences[i-1,j+0] <= matrice_differences[i-1,j-1] and matrice_differences[i-1,j+0] <= matrice_differences[i-1,j+1]:
                        matrice_provenance[i-1,j] = 0
                        matrice_differences[i,j]+=matrice_differences[i-1,j+0]
                    else:
                        matrice_provenance[i-1,j] = 1
                        matrice_differences[i,j]+=matrice_differences[i-1,j+1]

        """ On part du min de la dernière ligne et on remonte en suivant les indications de matrice_provenance qui nous donne la coupe, à laquelle il faut rajouter le décalage (x,y) pour cohérence par rapport aux positions dans output """
        pos_mini = (patch_size-1,0)
        val_mini = matrice_differences[patch_size-1,0]
        for j in range(1,shared_size):
            if matrice_differences[patch_size-1,j] < val_mini:
                val_mini = matrice_differences[patch_size-1,j]
                pos_mini = (patch_size-1,j)

        coupe_sans_decalage = [pos_mini]
        for ligne in matrice_provenance[::-1]:
            a,b = coupe_sans_decalage[-1]
            coupe_sans_decalage.append((a-1,b+ligne[b]))

        coupe_verticale = list((px+cx,py+cy) for (cx,cy) in coupe_sans_decalage[::-1])

    else:
        coupe_verticale = list((px+cx,py) for cx in range(patch_size))


    """
    On fait ensuite si x != 0 la frontiere horizontale et les modifs en fonction sinon on fait directement les modifs
    """

    if px == 0:
        """ On recopie donc la partie de patch à droite de la coupe dans output """
        for i,a in enumerate(range(px,px+patch_size)):
            for j,b in enumerate(range(py,py+patch_size)):
                if b>=coupe_verticale[i][1]:
                    output[a,b] = patch[i,j]
                    origin_from_input[a,b] = [x+i,y+j]

    else:
        """ On fait la coupe horizontale dans ce cas et ensuite on recopie la partie de patch selon ces deux coupes """
        matrice_differences = np.zeros((shared_size,patch_size))
        for i in range(shared_size):
            for j in range(patch_size):
                matrice_differences[i,j] = diff(patch[i,j],output[px+i,py+j])

        matrice_provenance = np.zeros((shared_size,patch_size-1),dtype = np.int8)

        for j in range(1,patch_size):
            for i in range(shared_size):
                if i == 0:
                    if matrice_differences[i+0,j-1] <= matrice_differences[i+1,j-1]:
                        matrice_provenance[i,j-1] = 0
                        matrice_differences[i,j]+=matrice_differences[i+0,j-1]
                    else:
                        matrice_provenance[i,j-1] = 1
                        matrice_differences[i,j]+=matrice_differences[i+1,j-1]
                elif i == shared_size-1:
                    if matrice_differences[i-1,j-1] <= matrice_differences[i+0,j-1]:
                        matrice_provenance[i,j-1] = -1
                        matrice_differences[i,j]+=matrice_differences[i-1,j-1]
                    else:
                        matrice_provenance[i,j-1] = 0
                        matrice_differences[i,j]+=matrice_differences[i+0,j-1]
                else:
                    if matrice_differences[i-1,j-1] <= matrice_differences[i+0,j-1] and matrice_differences[i-1,j-1] <= matrice_differences[i+1,j-1]:
                        matrice_provenance[i,j-1] = -1
                        matrice_differences[i,j]+=matrice_differences[i-1,j-1]
                    elif matrice_differences[i+0,j-1] <= matrice_differences[i-1,j-1] and matrice_differences[i+0,j-1] <= matrice_differences[i+1,j-1]:
                        matrice_provenance[i,j-1] = 0
                        matrice_differences[i,j]+=matrice_differences[i+0,j-1]
                    else:
                        matrice_provenance[i,j-1] = 1
                        matrice_differences[i,j]+=matrice_differences[i+1,j-1]

        pos_mini = (0,patch_size-1)
        val_mini = matrice_differences[0,patch_size-1]
        for i in range(1,shared_size):
            if matrice_differences[i,patch_size-1] < val_mini:
                val_mini = matrice_differences[i,patch_size-1]
                pos_mini = (i,patch_size-1)

        coupe_sans_decalage = [pos_mini]
        for ligne in np.transpose(matrice_provenance)[::-1]:
            a,b = coupe_sans_decalage[-1]
            coupe_sans_decalage.append((a+ligne[a],b-1))

        coupe_horizontale = list((px+cx,py+cy) for (cx,cy) in coupe_sans_decalage[::-1])

        """ On peut finalement recopier dans output la bonne partie de patch donnée par l'information des 2 coupes """
        for i,a in enumerate(range(px,px+patch_size)):
            for j,b in enumerate(range(py,py+patch_size)):
                if a>=coupe_horizontale[j][0] and b>=coupe_verticale[i][1]:
                    output[a,b] = patch[i,j]
                    origin_from_input[a,b] = [x+i,y+j]
