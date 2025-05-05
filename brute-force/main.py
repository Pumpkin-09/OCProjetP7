import csv
from decimal import Decimal
from itertools import combinations
import re
import os


def recuperation_csv(fichier_csv):
    liste_actions = []
    with open(fichier_csv, "r") as f:
        lecture_csv = csv.reader(f, delimiter=",")
        next(lecture_csv)
        for ligne in lecture_csv:
            element_modifier = re.sub("%", "", ligne[2])
            ligne[2] = element_modifier
            liste_actions.append(ligne)
        return liste_actions


def calcul_benefice(cout, pourcentage):
    pourcentage = Decimal(pourcentage) / Decimal("100")
    return pourcentage * cout


def affichage_liste_action(meilleur_benefice, cout_total):
    print(f"Voici la meilleur combinaison d'action pour un maximum de {cout_total}€ d'investissement sur 2 ans:")
    for i in range(len(meilleur_benefice)-1):
        print(meilleur_benefice[i])
    print(f"Bénéfice: {meilleur_benefice[-1]}")


def main():
    meilleur_benefice = [Decimal("0")]
    chemin = os.path.dirname(os.path.abspath(__file__))
    fichier_csv = os.path.join(chemin, "Liste_actions.csv")
    liste_actions = recuperation_csv(fichier_csv)
    for i in range(1, len(liste_actions) + 1):
        for combinaison in combinations(liste_actions, i):
            cout_total = Decimal("0")
            benefice = Decimal("0")

            for action in combinaison:
                cout = Decimal(action[1])
                pourcentage = Decimal(action[2])
                benefice += calcul_benefice(cout, pourcentage)
                cout_total += cout
            if cout_total <= 500 and benefice > meilleur_benefice[-1]:
                    combinaison_liste = list(combinaison)
                    combinaison_liste.append(benefice)
                    meilleur_benefice = combinaison_liste
                    total_cout = cout_total
    affichage_liste_action(meilleur_benefice, total_cout)


main()