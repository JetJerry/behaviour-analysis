# Behaviour Analysis with RNNs, LSTMs & GRUs

This project performs **text emotion classification** using deep learning models.

The notebook classifies text into 6 emotions:

* Sadness
* Joy
* Love
* Anger
* Fear
* Surprise

## Models Used

The notebook compares:

* Simple RNN
* LSTM
* GRU
* Bidirectional GRU (BiGRU)

The final **Bidirectional GRU** model is evaluated using accuracy, loss, confusion matrix, and sample predictions.

## Dataset

The project uses the **DAIR-AI Emotion dataset** from Hugging Face.

## Workflow

1. Load the dataset
2. Explore the data
3. Tokenize and pad text
4. Train RNN, LSTM, and GRU models
5. Compare model performance
6. Train an advanced Bidirectional GRU
7. Evaluate predictions
8. Save the trained model and tokenizer

## Saved Files

The notebook saves the trained model and tokenizer inside the `Artifacts/` folder:

```text
Artifacts/
├── BiGRU_Modle.keras
└── tokenizer.pkl
```

## Requirements

Install the required libraries:

```bash
pip install tensorflow pandas numpy matplotlib seaborn scikit-learn datasets
```

## How to Run

Open `behaviour.ipynb` in **Jupyter Notebook or VS Code** and run the cells from top to bottom.


## Backend

The backend is built with **FastAPI**. It:

1. Loads the BiGRU model and tokenizer when the server starts.
2. Cleans and preprocesses the input text.
3. Tokenizes and pads the text.
4. Runs behaviour prediction.
5. Returns the predicted emotion, confidence score, and probabilities for all emotions.

### API Endpoints

| Endpoint   | Method | Description                    |
| ---------- | ------ | ------------------------------ |
| `/`        | GET    | Opens the web interface        |
| `/health`  | GET    | Checks server and model status |
| `/predict` | POST   | Predicts emotion from text     |

The API accepts text between **1 and 2000 characters**.

## Project Structure

```text
Project/
├── behaviour.ipynb
├── main.py
├── Artifacts/
│   ├── BiGRU_Model.keras
│   └── tokenizer.pkl
└── static/
    └── index.html
```

The backend loads the model and tokenizer from the `Artifacts/` directory.

## Requirements

```bash
pip install tensorflow fastapi uvicorn numpy pydantic
```

## Run the Backend

```bash
uvicorn main:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

## Workflow

```text
User Text
   ↓
FastAPI Backend
   ↓
Text Preprocessing
   ↓
Tokenization + Padding
   ↓
BiGRU Model
   ↓
Emotion + Confidence
   ↓
API Response
```

Run Frontend:
Steamlit: streamlit run app.py

