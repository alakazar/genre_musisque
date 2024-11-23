import os
import librosa
import numpy as np
import joblib


MODEL_PATH = "modele_genre_musical.pkl"

def extract_features(file_path):
    """
    Extrait les caractéristiques d'un fichier audio (MFCC, Chroma, Spectral Contrast, RMS).
    :param file_path: Chemin vers le fichier audio.
    :return: Un tableau numpy contenant les caractéristiques extraites ou None en cas d'erreur.
    """
    try:
        # Charger l'audio
        audio, sr = librosa.load(file_path, sr=22050)

        # MFCCs (13 coefficients)
        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
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

        # Combiner toutes les caractéristiques
        features = np.hstack([mfcc_mean, chroma_mean, spectral_contrast_mean, rms_mean])
        return features

    except Exception as e:
        return None

def predict_genre(file_path):
    """
    Prédit le genre musical d'un fichier audio en utilisant un modèle préalablement sauvegardé.
    :param file_path: Chemin vers le fichier audio.
    :return: Genre prédit ou "Erreur" en cas de problème.
    """
    try:
        if not os.path.exists(file_path) or not file_path.lower().endswith(('.mp3', '.wav')):
            return "Erreur"

        features = extract_features(file_path)
        if features is None:
            return "Erreur"

        model = joblib.load(MODEL_PATH)

        features = features.reshape(1, -1)
        prediction = model.predict(features)
        return prediction[0]

    except Exception as e:
        return "Erreur"
