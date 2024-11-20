# Script pour vider le fichier modele_genre_musical.pkl
fichier_modele = 'modele_genre_musical.pkl'

try:
    # Ouvre le fichier en mode écriture binaire et écrase le contenu
    with open(fichier_modele, 'wb') as fichier:
        pass  # Ne rien écrire, ce qui le vide
    print(f"Le fichier {fichier_modele} a été vidé avec succès.")
except FileNotFoundError:
    print(f"Erreur : le fichier {fichier_modele} n'existe pas.")
except Exception as e:
    print(f"Une erreur est survenue : {e}")
