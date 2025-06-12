from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict
import joblib
import pandas as pd
import os
import re

# Charger le pipeline entraîné (à ne charger qu'une fois au démarrage)
pipeline = joblib.load("models/sentiment_pipeline.joblib")

app = FastAPI()

# Définition du schéma d'entrée (request)
class TweetRequest(BaseModel):
    clean_text_advanced: str
    Country: str
    Time_of_Tweet: str

# Route d'accueil simple (pour tester que ça marche)
@app.get("/")
def read_root():
    return {"message": "API de prédiction de sentiment - prête !"}

@app.post("/predict")
def predict_sentiment(request: TweetRequest):
    example = pd.DataFrame([{
        "clean_text_advanced": request.clean_text_advanced,
        "Country": request.Country,
        "Time of Tweet": request.Time_of_Tweet
    }])
    prediction = pipeline.predict(example)[0]
    probabilities = pipeline.predict_proba(example)[0].tolist()
    
    new_row = {
        "textID": "",
        "text": request.clean_text_advanced,
        "selected_text": "",
        "sentiment": prediction,
        "Time of Tweet": request.Time_of_Tweet,
        "Age of User": "",
        "Country": request.Country,
        "Population -2020": "",
        "Land Area (Km²)": "",
        "Density (P/Km²)": "",
        "": ""
    }
    train_file = "projet_data\\train.csv"
    
    # Créer le dossier s'il n'existe pas
    os.makedirs(os.path.dirname(train_file), exist_ok=True)
    
    if os.path.isfile(train_file):
        df_train = pd.read_csv(train_file, encoding="latin1")
        df_train = pd.concat([df_train, pd.DataFrame([new_row])], ignore_index=True)
        df_train.to_csv(train_file, index=False, encoding="utf-8")
    else:
        pd.DataFrame([new_row]).to_csv(train_file, index=False, encoding="utf-8")
    
    return {
        "prediction": prediction,
        "probabilities": probabilities
    }

# ---- CHATBOT ROUTE ----

# Conversation memory
class ChatState(BaseModel):
    step: str
    data: Dict[str, Optional[str]]

class ChatbotRequest(BaseModel):
    message: str
    state: Optional[ChatState] = None

def load_unique_values(csv_path, colname):
    df = pd.read_csv(csv_path, encoding="latin1")
    values = df[colname].dropna().unique()
    values = [str(val).strip() for val in values]
    return values

# Charge les valeurs connues depuis le CSV
COUNTRIES = load_unique_values('projet_data/train.csv', 'Country')
TIME_VALUES = load_unique_values('projet_data/train.csv', 'Time of Tweet')
SENTIMENT_VALUES = load_unique_values('projet_data/train.csv', 'sentiment')

def extract_value(user_message, value_list):
    user_message = user_message.lower()
    for value in value_list:
        pattern = rf"\b{re.escape(str(value).lower())}\b"
        if re.search(pattern, user_message):
            return value
    return None

def extract_country(user_message, country_list=COUNTRIES):
    return extract_value(user_message, country_list)

@app.post("/chatbot")
def chatbot(request: ChatbotRequest):
    state = request.state or ChatState(step="start", data={})

    # STEP 1: Ask for tweet text
    if state.step == "start":
        state.step = "await_text"
        return {
            "response": "Hi! Please enter the sentence or tweet you'd like advice on.",
            "state": state
        }

    # STEP 2: User provides tweet text
    if state.step == "await_text":
        state.data['text'] = request.message
        state.step = "await_country"
        return {
            "response": f"In which country do you plan to publish this tweet? (Countries in english)",
            "state": state
        }

    # STEP 3: User provides country (with extraction/validation)
    if state.step == "await_country":
        country = extract_country(request.message)
        if not country:
            return {
                "response": f"Sorry, I couldn't detect a country in your answer. Please type or pick among: {', '.join(COUNTRIES)}.",
                "state": state
            }
        state.data['country'] = country
        state.step = "await_time"
        return {
            "response": f"At what time of day will you post it? (Possible values: {', '.join(TIME_VALUES)})",
            "state": state
        }

    # STEP 4: User provides time (with extraction/validation)
    if state.step == "await_time":
        time_value = extract_value(request.message, TIME_VALUES)
        if not time_value:
            return {
                "response": f"Sorry, I couldn't detect a valid time in your answer. Please choose among: {', '.join(TIME_VALUES)}.",
                "state": state
            }
        state.data['time'] = time_value
        state.step = "await_goal"
        return {
            "response": f"What feeling or sentiment do you want your tweet to convey? (Possible values: {', '.join(SENTIMENT_VALUES)})",
            "state": state
        }

    # STEP 5: User provides sentiment goal (with extraction/validation), then prediction
    if state.step == "await_goal":
        goal_value = extract_value(request.message, SENTIMENT_VALUES)
        if not goal_value:
            return {
                "response": f"Sorry, I couldn't detect a valid sentiment in your answer. Please choose among: {', '.join(SENTIMENT_VALUES)}.",
                "state": state
            }
        state.data['goal'] = goal_value

        # Prédiction
        example = pd.DataFrame([{
            "clean_text_advanced": state.data['text'],
            "Country": state.data['country'],
            "Time of Tweet": state.data['time']
        }])
        prediction = pipeline.predict(example)[0]
        probabilities = pipeline.predict_proba(example)[0]

        advice = ""
        if state.data['goal'].lower() in prediction.lower():
            advice = f"Your tweet already matches your goal sentiment ({prediction})."
        else:
            advice = f"Currently, your tweet is predicted as '{prediction}'. To achieve a '{state.data['goal']}' sentiment, consider rephrasing your text or using more appropriate words for your target emotion."

        state.step = "end"
        return {
            "response": f"Analysis complete!\n- Prediction: {prediction}\n- Advice: {advice}\n\nWould you like to analyze another sentence? (Type 'restart' to begin again.)",
            "state": state
        }

    # Restart flow
    if state.step == "end" and request.message.lower().strip() == "restart":
        return {
            "response": "Let's start again! Please enter the sentence or tweet you'd like advice on.",
            "state": ChatState(step="await_text", data={})
        }

    # Fallback
    return {
        "response": "Sorry, I didn't understand. To start again, type 'restart'.",
        "state": state
    }