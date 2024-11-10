import os
import numpy as np
import librosa
import pandas as pds

# Définir les genres et les chemins vers chaque dossier de genre
genres = ['blues','classical','country','disco','hiphop','metal','pop','reggae','rock'] # Ne marche pas avec le jazz à voir pourquoi
base_path = 'Data\\genres_original' # Répertoire contenant les dossiers 'classical' et 'pop'

# Initialiser une liste pour stocker les données
data = []

# Parcourir chaque genre et charger les fichiers audio
for genre in genres:
    folder_path = os.path.join(base_path, genre)
      # Label numérique : 0 pour classical, 1 pour pop

    # Charger chaque fichier dans le dossier du genre
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        y, sr = librosa.load(file_path, sr=22050)  # Charger l'audio avec une fréquence d'échantillonnage de 22050 Hz

        # Extraire les caractéristiques MFCCs moyennes pour chaque fichier
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfccs_mean = np.mean(mfccs.T, axis=0)  # Moyenne sur l'axe du temps

        # Ajouter les caractéristiques et le label au dataset
        data.append([mfccs_mean, genre])

# Conversion en DataFrame pour une utilisation plus facile
df = pds.DataFrame(data, columns=['features', 'label'])

# Créer les matrices de caractéristiques et de labels
X = np.array(df['features'].tolist())  # Caractéristiques
y = df['label'].values  # Labels

print(df)