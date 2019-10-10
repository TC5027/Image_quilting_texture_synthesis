#!/usr/bin/env python3
import random
from Metric import metric

def selection(input,output,origin_from_input,position,patch_size,shared_size,M):
    """
    On cherche à trouver un patch qui devra etre positionné à l'emplacement : position
    Pour cela on va sélectionner le patch dans la continuité des pixels déja placé et M aléatoires mais de metric acceptable (càd relativement faible)
    On renvoie au final le patch parmi ceux là minimisant la metric

    """
    a,b,c = input.shape
    liste_candidats = [] #liste d'indice (x,y) on accède au patch en faisant input[x:(x+patch_size),y:(y+patch_size)]
    for _ in range(M):
        """
        on choisit 25 patchs au hasard dans input (désigné par une position, on accède au patch avec input[x:(x+patch_size),y:(y+patch_size)])
        et on met en candidat celui ayant la metric la plus petite parmi ces 25
        """
        x,y = random.randint(0,a-1-patch_size),random.randint(0,b-1-patch_size)
        m = metric(output,input[x:(x+patch_size),y:(y+patch_size)],position,shared_size)
        for _ in range(24):
            x_,y_ = random.randint(0,a-1-patch_size),random.randint(0,b-1-patch_size)
            value = metric(output,input[x_:(x_+patch_size),y_:(y_+patch_size)],position,shared_size)
            if value < m:
                m = value
                x,y = x_,y_
        liste_candidats.append((x,y))

    """
    on ajoute le patch qui serait dans la continuité avec une probabilité de 95%
    """
    x,y = origin_from_input[position]
    if x+patch_size<a and y+patch_size<b and random.random()<0.95:
        liste_candidats.append((x,y))

    """
    voila maintenant on a nos candidats et on choisit celui de metric le plus faible
    """

    x,y = liste_candidats[0]
    m = metric(output,input[x:(x+patch_size),y:(y+patch_size)],position,shared_size)
    for x_,y_ in liste_candidats[1:]:
        value = metric(output,input[x_:(x_+patch_size),y_:(y_+patch_size)],position,shared_size)
        if value < m:
            m = value
            x,y = x_,y_
    return(x,y)
