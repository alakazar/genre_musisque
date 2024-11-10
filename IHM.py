import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import os
import threading
import time

# Initialisation de pygame pour le son
pygame.mixer.init()

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

# Fonction pour ouvrir l'explorateur de fichiers et sélectionner un fichier .wav
def selectionner_fichier():
    fichier_path = filedialog.askopenfilename(
        title="Sélectionner un fichier .wav",
        filetypes=[("Fichiers WAV", "*.wav")]
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

# Fonction simulant le traitement d'analyse de genre
def analyse_genre():
    resultat_genre.set("")
    bouton_analyse.config(state="disabled")
    threading.Thread(target=demarrer_animation).start()

    time.sleep(5)
    resultat_genre.set("Le genre de la musique est : Pop")
    bouton_analyse.config(state="normal")

# Fonction pour démarrer l'animation de chargement
def demarrer_animation():
    while not resultat_genre.get():
        for _ in range(5):
            rotation_label.config(text="•" * _ + "   " * (5 - _) + "Analyzing...")
            time.sleep(0.2)
            root.update_idletasks()

# Création d'un titre principal
titre_principal = tk.Label(
    root,
    text="Analyse du Genre de la Musique",
    font=("Segoe UI", 32, "bold"),
    fg="#0078D7",  # Bleu Microsoft
    bg="#f3f3f3"
)
titre_principal.pack(pady=(30, 10))

# Bouton pour ouvrir l'explorateur de fichiers et sélectionner un fichier .wav
bouton_selectionner = tk.Button(
    root,
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
    root,
    text="",
    font=("Segoe UI", 14),
    fg="#555555",
    bg="#f3f3f3",
    wraplength=900,
    justify="center"
)
etiquette_chemin.pack(pady=10)

# Bouton pour mettre en pause ou reprendre la musique
bouton_pause = tk.Button(
    root,
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

# Bouton pour lancer l'analyse du genre
bouton_analyse = tk.Button(
    root,
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
bouton_analyse.pack(pady=20)

# Zone de texte pour l'animation de chargement
rotation_label = tk.Label(
    root,
    text="",
    font=("Segoe UI", 14),
    fg="#0078D7",
    bg="#f3f3f3"
)
rotation_label.pack(pady=15)

# Étiquette pour afficher le résultat de l'analyse
etiquette_resultat = tk.Label(
    root,
    textvariable=resultat_genre,
    font=("Segoe UI", 18),
    fg="#333333",
    bg="#f3f3f3"
)
etiquette_resultat.pack(pady=10)

# Ajout d'un bouton Quitter
bouton_quitter = tk.Button(
    root,
    text="Quitter",
    font=("Segoe UI", 14),
    command=root.destroy,
    fg="#333333",
    bg="#e5e5e5",
    activebackground="#d5d5d5",
    padx=30,
    pady=15,
    relief="flat"
)
bouton_quitter.pack(side="bottom", pady=30)

# Associe la touche Échap pour quitter le plein écran
root.bind("<Escape>", quitter_plein_ecran)

# Lancement de la boucle principale de l'interface
root.mainloop()
