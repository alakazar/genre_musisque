
fichier_modele = 'modele_genre_musical.pkl'

try:

    with open(fichier_modele, 'wb') as fichier:
        pass
    print(f"Le fichier {fichier_modele} a été vidé avec succès.")
except FileNotFoundError:
    print(f"Erreur : le fichier {fichier_modele} n'existe pas.")
except Exception as e:
    print(f"Une erreur est survenue : {e}")
