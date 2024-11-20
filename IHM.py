import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import os
import threading
import time
import joblib
import numpy as np
import librosa
from sklearn.preprocessing import StandardScaler
import Trouver_genre_musique

# Initialisation de pygame pour le son
pygame.mixer.init()

# Charger le modèle de prédiction (assurez-vous que le modèle est déjà enregistré avec joblib)
try:
    model = joblib.load('modele_genre_musical.pkl')
    scaler = joblib.load('scaler.pkl')  # Si vous utilisez un scaler pour normaliser les données
except Exception as e:
    print(f"Erreur lors du chargement du modèle ou du scaler : {e}")

# Création de la fenêtre principale en plein écran
root = tk.Tk()
root.title("Analyse du genre de la musique")
root.attributes("-fullscreen", True)  # Mode plein écran
root.configure(bg="#f3f3f3")  # Fond gris clair

# Variables globales
chemin_fichier = tk.StringVar()
musique_en_pause = False  # Indique si la musique est en pause
resultat_genre = tk.StringVar(value="")  # Variable pour stocker le résultat de l'analyse


# Fonction pour quitter le mode plein écran avec la touche Échap
def quitter_plein_ecran(event):
    root.attributes("-fullscreen", False)


def selectionner_fichier():
    fichier_path = filedialog.askopenfilename(
        title="Sélectionner un fichier audio",
        filetypes=[("Fichiers Audio", "*.wav *.mp3")]
    )
    if fichier_path:
        chemin_fichier.set(fichier_path)
        nom_fichier = os.path.basename(fichier_path)
        etiquette_chemin.config(text=f"Fichier sélectionné : {nom_fichier}")
        jouer_son(fichier_path)
    else:
        messagebox.showwarning("Avertissement", "Aucun fichier n'a été sélectionné.")


# Fonction pour jouer le fichier .wav sélectionné
def jouer_son(fichier_path):
    global musique_en_pause
    try:
        extension = os.path.splitext(fichier_path)[1].lower()
        if extension not in [".mp3", ".wav"]:
            raise ValueError("Format non supporté. Veuillez sélectionner un fichier MP3 ou WAV.")

        pygame.mixer.music.load(fichier_path)
        pygame.mixer.music.play()
        bouton_pause.config(text="Pause")
        musique_en_pause = False
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de lire le fichier audio : {e}")


# Fonction pour mettre en pause ou reprendre la musique
def pause_ou_reprendre():
    global musique_en_pause
    if musique_en_pause:
        pygame.mixer.music.unpause()
        bouton_pause.config(text="Pause")
        musique_en_pause = False
    else:
        pygame.mixer.music.pause()
        bouton_pause.config(text="Reprendre")
        musique_en_pause = True


# Fonction pour effectuer l'analyse du genre
def analyse_genre():
    fichier_path = chemin_fichier.get()
    if not fichier_path:
        messagebox.showwarning("Avertissement", "Veuillez sélectionner un fichier audio.")
        return

    # Fonction pour extraire les caractéristiques audio
    def extraire_caracteristiques(fichier_path):
        y, sr = librosa.load(fichier_path, sr=None)

        # Extraire les caractéristiques audio (par exemple, MFCC, Chroma, Spectral Contrast, etc.)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_mean = np.mean(mfcc, axis=1)

        # Fusionner les caractéristiques dans un vecteur
        features = mfcc_mean
        return features

    # Extraire les caractéristiques audio
    features = extraire_caracteristiques(fichier_path)
    features = scaler.transform([features])  # Si vous utilisez un scaler pour normaliser

    # Effectuer la prédiction
    genre_pred = model.predict(features)[0]

    # Mise à jour du label pour afficher le résultat
    resultat_genre.set(f"Le genre de la musique est : {genre_pred}")
    rotation_label.config(text=resultat_genre.get(), font=("Segoe UI", 20), fg="#0078D7")


# Fonction pour démarrer l'animation de chargement
def demarrer_animation():
    while not resultat_genre.get():
        for _ in range(5):
            rotation_label.config(text="•" * _ + "   " * (5 - _) + "Analyzing")
            time.sleep(0.2)
            root.update_idletasks()


# Création d'un bandeau gris foncé pour le titre
bandeau_titre = tk.Frame(root, bg="#333333", padx=20, pady=10)  # Cadre sombre autour du titre
bandeau_titre.pack(fill="x", pady=(0, 20))  # Remplit horizontalement avec un espacement en bas

# Création de l'étiquette du titre à l'intérieur du bandeau
titre_principal = tk.Label(
    bandeau_titre,
    text="Analyse du Genre de la Musique",
    font=("Segoe UI", 32, "bold"),
    fg="#FFFFFF",  # Texte blanc pour contraste
    bg="#333333"  # Fond assorti au bandeau
)
titre_principal.pack()

# Création d'un cadre gris foncé pour la section à gauche
cadre_gauche = tk.Frame(root, bg="#333333", padx=20, pady=20)
cadre_gauche.pack(side="left", fill="y", padx=(20, 10), pady=20)

# Bouton pour ouvrir l'explorateur de fichiers et sélectionner un fichier .wav
bouton_selectionner = tk.Button(
    cadre_gauche,
    text="Sélectionner un fichier .wav",
    font=("Segoe UI", 14),
    command=selectionner_fichier,
    fg="#333333",
    bg="#e5e5e5",
    activebackground="#d5d5d5",
    padx=30,
    pady=15,
    relief="flat"
)
bouton_selectionner.pack(pady=15)

# Étiquette pour afficher le nom du fichier sélectionné
etiquette_chemin = tk.Label(
    cadre_gauche,
    text="",
    font=("Segoe UI", 14),
    fg="#ffffff",
    bg="#333333",
    wraplength=400,
    justify="center"
)
etiquette_chemin.pack(pady=10)

# Bouton pour mettre en pause ou reprendre la musique
bouton_pause = tk.Button(
    cadre_gauche,
    text="Pause",
    font=("Segoe UI", 14),
    command=pause_ou_reprendre,
    fg="#333333",
    bg="#e5e5e5",
    activebackground="#d5d5d5",
    padx=30,
    pady=15,
    relief="flat"
)
bouton_pause.pack(pady=10)

# Bouton pour lancer l'analyse du genre (placé en bas du cadre gauche)
bouton_analyse = tk.Button(
    cadre_gauche,
    text="Analyse du genre de la musique",
    font=("Segoe UI", 14),
    command=lambda: threading.Thread(target=analyse_genre).start(),
    fg="#333333",
    bg="#e5e5e5",
    activebackground="#d5d5d5",
    padx=30,
    pady=15,
    relief="flat"
)
bouton_analyse.pack(side="bottom", pady=20)

# Cadre de droite (partie pour afficher le chargement et le résultat)
cadre_droit = tk.Frame(root, bg="#f3f3f3", padx=20, pady=20)
cadre_droit.pack(side="right", fill="both", expand=True)

# Zone de texte pour l'animation de chargement (centrée dans le cadre droit)
rotation_label = tk.Label(
    cadre_droit,
    text="",
    font=("Segoe UI", 18),
    fg="#0078D7",
    bg="#f3f3f3"
)
rotation_label.pack(expand=True)  # Centre le label de chargement

# Associe la touche Échap pour quitter le plein écran
root.bind("<Escape>", quitter_plein_ecran)

# Lancement de la boucle principale de l'interface
root.mainloop()
