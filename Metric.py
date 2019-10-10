#!/usr/bin/env python3

def diff(rgb1,rgb2):
    """
    différence classique entre valeurs rgb
    """
    return(sum((e1-e2)**2 for e1,e2 in zip(rgb1,rgb2)))

def metric(output,new_bloc,position,shared_size):
    """
    renvoie la valeur de la différence des pixels où se superposent new_bloc sur sa futur position et l'output déja synthétisé

    rappel : position désigne le point en haut à gauche d'où doit partir new_bloc
    """
    valeur = 0
    a,b,c = new_bloc.shape

    x,y = position

    if x == 0:
        """cas de la synthèse de la premiere ligne, pas de bloc au dessus du coup"""
        for i,ligne in enumerate(new_bloc):
            for j,element in enumerate(ligne[:shared_size]):
                valeur += diff(element,output[x+i,y+j])
    elif y == 0:
        """cas de la synthèse d'un bloc d'une nouvelle ligne pas de bloc à gauche"""
        for i,ligne in enumerate(new_bloc[:shared_size]):
            for j,element in enumerate(ligne):
                valeur += diff(element,output[x+i,y+j])
    else:
        """cas le plus général avec prédécesseur en haut et à gauche"""
        for i,ligne in enumerate(new_bloc[:shared_size]):
            for j,element in enumerate(ligne):
                valeur += diff(element,output[x+i,y+j])
        for i,ligne in enumerate(new_bloc[shared_size:]):
            for j,element in enumerate(ligne[:shared_size]):
                valeur += diff(element,output[x+i+shared_size,y+j])
    return(valeur)
