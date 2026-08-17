
from pathlib import Path
import pickle
import re
from functools import lru_cache

import numpy as np
from keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "Artifacts" / "BiGRU_Model.keras"
TOKENIZER_PATH = BASE_DIR / "Artifacts" / "tokenizer.pkl"

MAX_SEQUENCE_LENGTH = 50

EMOTION_LABELS = [
    "sadness",
    "joy",
    "love",
    "anger",
    "fear",
    "surprise",
]

EMOTION_EMOJIS = {
    "sadness": "😢",
    "joy": "😄",
    "love": "❤️",
    "anger": "😠",
    "fear": "😨",
    "surprise": "😲",
}


# ============================================================
# TEXT PREPROCESSING
# ============================================================

def preprocess_text(text: str) -> str:
    """
    Clean raw text exactly according to the original backend logic.

    Original pipeline:
    1. Convert to lowercase
    2. Remove apostrophes
    3. Remove special characters/punctuation
    4. Remove extra spaces
    """

    text = text.lower()
    text = re.sub(r"'", "", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


# ============================================================
# LOAD MODEL + TOKENIZER
# ============================================================

@lru_cache(maxsize=1)
def load_resources():
    """
    Load the BiGRU model and tokenizer once.

    Streamlit reruns the Python script whenever the user
    interacts with the UI. Caching prevents the model from
    being loaded again on every interaction.

    Returns:
        model, tokenizer
    """

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"BiGRU model not found:\n{MODEL_PATH}\n\n"
            "Make sure the file exists at:\n"
            "Artifacts/BiGRU_Model.keras"
        )

    if not TOKENIZER_PATH.exists():
        raise FileNotFoundError(
            f"Tokenizer not found:\n{TOKENIZER_PATH}\n\n"
            "Make sure the file exists at:\n"
            "Artifacts/tokenizer.pkl"
        )

    print("Loading BiGRU model...")
    model = load_model(MODEL_PATH)

    print("Loading tokenizer...")
    with open(TOKENIZER_PATH, "rb") as file:
        tokenizer = pickle.load(file)

    print("Moodline model and tokenizer loaded successfully.")

    return model, tokenizer


# ============================================================
# MODEL STATUS
# ============================================================

def is_model_ready() -> bool:
    """
    Check whether both model and tokenizer are available.
    """

    try:
        load_resources()
        return True
    except Exception:
        return False


# ============================================================
# PREDICTION
# ============================================================

def predict_emotion(text: str) -> dict:
    """
    Run the complete Moodline prediction pipeline.

    Input:
        text: raw sentence from the Streamlit UI

    Returns:
        {
            "text": original input,
            "cleaned_text": cleaned input,
            "predicted_emotion": predicted emotion,
            "confidence": top probability,
            "all_probabilites": {
                "sadness": ...,
                "joy": ...,
                "love": ...,
                "anger": ...,
                "fear": ...,
                "surprise": ...
            }
        }

    The misspelling "all_probabilites" is intentionally retained
    for compatibility with the original backend response format.
    """

    # --------------------------------------------------------
    # Validate raw input
    # --------------------------------------------------------

    if not isinstance(text, str):
        raise TypeError("Input text must be a string.")

    if not text.strip():
        raise ValueError("Please enter a sentence to analyze.")

    if len(text) > 2000:
        raise ValueError("Text must be 2000 characters or fewer.")

    # --------------------------------------------------------
    # Load cached resources
    # --------------------------------------------------------

    model, tokenizer = load_resources()

    # --------------------------------------------------------
    # 1. Preprocess text
    # --------------------------------------------------------

    cleaned_text = preprocess_text(text)

    if not cleaned_text:
        raise ValueError(
            "Please enter a sentence containing letters or numbers."
        )

    # --------------------------------------------------------
    # 2. Convert words to token IDs
    # --------------------------------------------------------

    tokenized_text = tokenizer.texts_to_sequences(
        [cleaned_text]
    )

    # --------------------------------------------------------
    # 3. Pad sequence to length 50
    # --------------------------------------------------------

    padded_sequence = pad_sequences(
        tokenized_text,
        maxlen=MAX_SEQUENCE_LENGTH,
        padding="post",
        truncating="post",
    )

    # --------------------------------------------------------
    # 4. Run BiGRU model
    # --------------------------------------------------------

    probabilities = model.predict(
        padded_sequence,
        verbose=0,
    )[0]

    probabilities = np.asarray(
        probabilities,
        dtype=np.float32,
    )

    # --------------------------------------------------------
    # Safety validation
    # --------------------------------------------------------

    if len(probabilities) != len(EMOTION_LABELS):
        raise ValueError(
            "The BiGRU model output does not contain the expected "
            f"{len(EMOTION_LABELS)} emotion probabilities. "
            f"Received {len(probabilities)}."
        )

    # --------------------------------------------------------
    # 5. Find top emotion
    # --------------------------------------------------------

    top_emotion_index = int(
        np.argmax(probabilities)
    )

    predicted_emotion = EMOTION_LABELS[
        top_emotion_index
    ]

    confidence = float(
        probabilities[top_emotion_index]
    )

    # --------------------------------------------------------
    # 6. Build complete probability breakdown
    # --------------------------------------------------------

    all_probabilites = {
        label: float(probability)
        for label, probability in zip(
            EMOTION_LABELS,
            probabilities,
        )
    }

    # --------------------------------------------------------
    # 7. Return prediction
    # --------------------------------------------------------

    return {
        "text": text,
        "cleaned_text": cleaned_text,
        "predicted_emotion": predicted_emotion,
        "confidence": confidence,
        "all_probabilites": all_probabilites,
    }


# ============================================================
# OPTIONAL: CLEAR MODEL CACHE
# ============================================================

def clear_model_cache():
    """
    Clear the cached model/tokenizer.

    Normally you do not need this. It can be useful during
    development if you replace the model or tokenizer files
    while Streamlit is running.
    """

    load_resources.cache_clear()