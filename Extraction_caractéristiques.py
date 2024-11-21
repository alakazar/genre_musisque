import os
import numpy as np
import librosa
import logging

# Configuration des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Chemin vers le dossier contenant les fichiers audio
DATA_PATH = "data/genres_original"

# Paramètres pour l'extraction des caractéristiques
SAMPLE_RATE = 22050
N_MFCC = 13

def extract_features(file_path):
    """
    Extrait les caractéristiques d'un fichier audio.
    """
    try:
        # Charger l'audio
        audio, sr = librosa.load(file_path, sr=SAMPLE_RATE)

        # MFCCs (13 coefficients)
        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=N_MFCC)
        mfcc_mean = np.mean(mfcc, axis=1)

        # Chroma (tonalité)
        chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
        chroma_mean = np.mean(chroma, axis=1)

        # Spectral Contrast
        spectral_contrast = librosa.feature.spectral_contrast(y=audio, sr=sr)
        spectral_contrast_mean = np.mean(spectral_contrast, axis=1)

        # RMS (Root Mean Square Energy)
        rms = librosa.feature.rms(y=audio)
        rms_mean = np.mean(rms)

        # Combiner toutes les caractéristiques dans un seul vecteur
        features = np.hstack([mfcc_mean, chroma_mean, spectral_contrast_mean, rms_mean])
        return features

    except Exception as e:
        logging.error(f"Erreur lors de l'extraction des caractéristiques pour {file_path}: {e}")
        return None

def process_audio_directory(data_path):
    """
    Parcourt le dossier audio et extrait les caractéristiques pour chaque fichier.
    """
    feature_list = []
    file_names = []
    genres = os.listdir(data_path)

    for genre in genres:
        genre_path = os.path.join(data_path, genre)
        if os.path.isdir(genre_path):
            logging.info(f"Traitement du genre: {genre}")
            for file_name in os.listdir(genre_path):
                if file_name.endswith(".wav"):
                    file_path = os.path.join(genre_path, file_name)
                    features = extract_features(file_path)
                    if features is not None:
                        feature_list.append(features)
                        file_names.append(file_name)

    return np.array(feature_list), file_names

if __name__ == "__main__":
    logging.info("Début du traitement...")
    features, files = process_audio_directory(DATA_PATH)
    if features.size > 0:
        logging.info(f"Extraction réussie de {len(features)} fichiers audio.")
        # Exemple : Sauvegarder les caractéristiques pour une analyse ultérieure
        np.save("features.npy", features)
        logging.info("Caractéristiques sauvegardées dans features.npy")
    else:
        logging.error("Aucune caractéristique extraite.")
