from typing import List

position = 0


def to_list(informations, type_installation):
    print(type_installation)
    print(type(type_installation))
    colonnes = informations[0]
    donnees = informations[1]
    donnees_list = []
    for item in donnees:
        donnees_list.append(dict(zip(colonnes, item)))

    if type_installation == "glissade":
        position = 1
    elif type_installation == "piscine":
        position = 3
    elif type_installation == "patinoire":
        position = 2

    # donnees_list = donnees_list.sort(key=trier_par_nom_inst)
    return donnees_list


def trier_par_nom_inst(liste):
    return liste[position]
