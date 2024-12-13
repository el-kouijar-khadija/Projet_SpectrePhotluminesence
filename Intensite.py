import os
import sys
import re
from recherche_plot import filtrer_donnees , afficher_graphique

# Lecture des données depuis le fichier
def lire_fichier(fichier):
    donnees = []
    try:
        with open(fichier, "r") as fd:
            for ligne in fd:
                # Vérifie si la ligne est valide (deux nombres séparés par un espace)
                if re.match(r"^\s*\d+(\.\d+)?\s+\d+(\.\d+)?\s*$", ligne):
                    longueur, intensite = map(float, ligne.split())  
                    
#ligne.split() divise la ligne en une liste de mots (en fonction des espaces).
#map(float, ...) convertit chaque élément en un nombre flottant (float).
#Les deux valeurs (longueur d'onde et intensité) sont attribuées respectivement à longueur et intensite.
  
                    donnees.append((longueur, intensite))  
    except FileNotFoundError:
        print(f"Erreur : le fichier {fichier} est introuvable.")
        sys.exit(1)  # Arrête le programme en cas d'erreur
    return donnees


# Normalisation des intensités
def normaliser_donnees(donnees):
    # Trouver la valeur maximale en utilisant une boucle
    intensite_max = 0
    for _, intensite in donnees:
        if intensite > intensite_max:
            intensite_max = intensite

    # Évite la division par zéro en cas de liste vide
    if intensite_max == 0: 
        intensite_max = 1

    # Diviser chaque intensité par la valeur maximale
    donnees_normalisees=[] 
    for longueur, intensite in donnees :
      donnees_normalisees.append((longueur, intensite / intensite_max)); 
    return donnees_normalisees


# Organisation des données en fenêtres
def creer_fenetres(donnees, pas):
    fenetres = {} 
    for longueur, intensite in donnees:
        borne_inf = int(longueur // pas) * pas 
        borne_sup = borne_inf + pas
        
#longueur // pas effectue une division entière de la longueur d'onde par pas. 
#Cela permet de déterminer dans quelle fenêtre (plage) se situe cette longueur d'onde.
#Ensuite, borne_inferieure est le début de la fenêtre (multiplication par pas 
#pour s'assurer que c'est un multiple de pas), 
#et borne_superieure est la fin de la fenêtre (ajouter simplement pas). 

        cle = f"[{borne_inf}-{borne_sup}[" 
        if cle not in fenetres:
            fenetres[cle] = []
        fenetres[cle].append(intensite)
    return fenetres


#La clé du dictionnaire est une chaîne de caractères qui représente la plage de 
#la fenêtre. Elle est formée par la notation [borne_inferieure-borne_superieure[, 
#ce qui est une façon de spécifier une plage ouverte à droite.
#Par exemple, si pas = 10, et que longueur = 15, la clé pourrait être [10-20[.

# Calcul des statistiques pour chaque fenêtre
def calculer_statistiques(fenetres):
    stats = {}
    for fenetre, intensites in fenetres.items(): 
        intensites.sort()  # Trie les intensités
        if intensites:
            stats[fenetre] = {
                "nombre": len(intensites),
                "minimum": intensites[0],
                "moyenne": sum(intensites) / len(intensites),
                "maximum": intensites[-1]
            }
        else:
            stats[fenetre] = {"nombre": 0, "minimum": 0, "moyenne": 0, "maximum": 0}
    return stats

# Affichage des résultats
def afficher_resultats(stats):
    for fenetre, valeurs in sorted(stats.items()):
        print(f"Fenêtre {fenetre}:")
        print(f"  Nombre de données: {valeurs['nombre']}")
        print(f"  Minimum: {valeurs['minimum']}")
        print(f"  Moyenne: {valeurs['moyenne']:.2f}")
        print(f"  Maximum: {valeurs['maximum']}")

# Fonction principale
def main():
    if len(sys.argv) < 2:
        print("Usage : python3 intensite.py <fichier> [<pas>]")
        sys.exit(1)

    fichier = sys.argv[1] 
    if len(sys.argv) > 2 :
        pas = int(sys.argv[2])
    else : 
        pas = 10

    donnees = lire_fichier(fichier) 
    donnees_normalisees = normaliser_donnees(donnees) 
    fenetres = creer_fenetres(donnees_normalisees, pas)
    stats = calculer_statistiques(fenetres)
    afficher_resultats(stats)
    
    # Demander les bornes à l'utilisateur
    try:
        borne_inf = float(input("Entrez la borne inférieure de l'intervalle (nm) : ")) 
        borne_sup = float(input("Entrez la borne supérieure de l'intervalle (nm) : "))
        if borne_inf >= borne_sup:
            raise ValueError("La borne inférieure doit être strictement inférieure à la borne supérieure.")
    except ValueError as e:
        print(f"Erreur : {e}", file=sys.stderr)
        sys.exit(1)


    donnees_filtrees = filtrer_donnees(donnees_normalisees, borne_inf, borne_sup) 
    afficher_graphique(donnees_filtrees, borne_inf, borne_sup) 
    

# Point d'entrée du programme
if _name_ == "_main_":
    main()
