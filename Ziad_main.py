import os
import librosa
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import logging

# Configuration des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Chemin vers les données audio
DATA_PATH = "data/genres_original"

# Paramètres pour l'extraction des caractéristiques
SAMPLE_RATE = 22050
N_MFCC = 13
MAX_PAD_LENGTH = 216  # Longueur des MFCCs après padding


def extract_features(file_path):
    """
    Extrait les caractéristiques d'un fichier audio (MFCCs, Chroma, Spectral Contrast, RMS).
    :param file_path: Chemin vers le fichier audio.
    :return: Un tableau Numpy contenant les caractéristiques extraites.
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


def load_data(data_path):
    """
    Charge les données audio et extrait les caractéristiques pour chaque fichier.
    :param data_path: Chemin vers le dossier contenant les fichiers audio.
    :return: Tuple (X, y) où X est un tableau des caractéristiques et y les labels.
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


def load_model(model_path):
    """
    Charge le modèle préalablement entraîné.
    :param model_path: Chemin vers le fichier du modèle.
    :return: Modèle Random Forest chargé.
    """
    try:
        model = joblib.load(model_path)
        logging.info("Modèle chargé avec succès.")
        return model
    except Exception as e:
        logging.error(f"Erreur lors du chargement du modèle: {e}")
        return None


def predict_genre(file_path, model):
    """
    Prédit le genre d'un fichier audio en utilisant le modèle chargé.
    :param file_path: Chemin vers le fichier audio.
    :param model: Modèle Random Forest chargé.
    :return: Le genre prédit du fichier audio.
    """
    features = extract_features(file_path)
    if features is None:
        logging.error(f"Impossible d'extraire les caractéristiques de {file_path}")
        return None
    features = features.reshape(1, -1)  # Applatir les caractéristiques pour la prédiction
    prediction = model.predict(features)
    return prediction[0]


def main():
    logging.info("Chargement des données...")
    X, y = load_data(DATA_PATH)

    # Vérifier les dimensions
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

    # Sauvegarde du modèle
    MODEL_PATH = "audio_classifier_rf_model.pkl"
    joblib.dump(model, MODEL_PATH)
    logging.info(f"Modèle sauvegardé dans {MODEL_PATH}")

    # Demander à l'utilisateur de prédire le genre d'un fichier audio
    while True:
        user_input = input("Voulez-vous prédire le genre d'un fichier audio ? (O/N): ").strip().lower()
        if user_input == 'o':
            while True:
                file_path = input("Entrez le chemin du fichier .wav à prédire (ou tapez 0 pour quitter) : ").strip()
                if file_path == '0':
                    logging.info("Fermeture du programme.")
                    return
                elif os.path.exists(file_path) and file_path.endswith(".wav"):
                    # Charger le modèle
                    model = load_model(MODEL_PATH)
                    if model:
                        predicted_genre = predict_genre(file_path, model)
                        if predicted_genre:
                            logging.info(f"Le genre prédit est : {predicted_genre}")
                            print(f"Le genre prédit est : {predicted_genre}")
                    break
                else:
                    logging.error("Le fichier n'existe pas ou n'est pas au format .wav. Veuillez essayer à nouveau.")
        elif user_input == 'n':
            logging.info("Fermeture du programme.")
            break
        else:
            logging.error("Entrée invalide, veuillez répondre par O ou N.")


if __name__ == "__main__":
    main()
