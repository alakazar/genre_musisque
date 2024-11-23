import os
import numpy as np
import librosa
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DATA_PATH = "data/genres_original"
MODEL_PATH = "modele_genre_musical.pkl"

SAMPLE_RATE = 22050
N_MFCC = 13
MAX_PAD_LENGTH = 216


def extract_features(file_path):
    """
    Extrait les caractéristiques d'un fichier audio.
    """
    try:
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


def load_data(data_path):
    """
    Charge les données audio et extrait les caractéristiques pour chaque fichier.
    """
    X = []
    y = []
    labels = os.listdir(data_path)

    for label in labels:
        label_path = os.path.join(data_path, label)
        if os.path.isdir(label_path):
            logging.info(f"Traitement du dossier: {label}")
            for file in os.listdir(label_path):
                if file.endswith(".wav"):
                    file_path = os.path.join(label_path, file)
                    features = extract_features(file_path)
                    if features is not None:
                        X.append(features)
                        y.append(label)

    return np.array(X), np.array(y)


def main():
    logging.info("Chargement des données...")
    X, y = load_data(DATA_PATH)

    if len(X) == 0 or len(y) == 0:
        logging.error("Aucune donnée n'a été chargée. Vérifiez les fichiers.")
        return

    # Diviser les données en ensemble d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    logging.info("Entraînement du modèle Random Forest...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    logging.info("Évaluation du modèle...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    logging.info(f"Précision du modèle: {accuracy:.2f}")
    print(classification_report(y_test, y_pred))

    # Sauvegarde du modèle dans modele_genre_musical.pkl
    joblib.dump(model, MODEL_PATH)
    logging.info(f"Modèle sauvegardé dans {MODEL_PATH}")


if __name__ == "__main__":
    main()
