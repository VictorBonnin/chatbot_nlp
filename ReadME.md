# Twitter Sentiment Analyzer API & Chatbot

Ce projet permet :
- d’analyser le **sentiment** d’un tweet en fonction du texte, du pays, du moment de la journée,
- de donner des **conseils personnalisés** sur le meilleur moment pour poster,
- d’interroger l’API via une **interface utilisateur Streamlit**.

---

## Prérequis

- Python 3.9+ recommandé
- Les fichiers d’entraînement et les modèles déjà entraînés disponibles dans notre pipeline (`sentiment_pipeline.joblib`)
- Les fichiers de données (dans `projet_data/train.csv`, etc.)

---

##  des dépendances : 
```bash
pip install -r requirements.txt
```

## Lancer le projet :
### L'API
```bash
uvicorn twitter_api:app --reload
```
```bash
http://localhost:8000/docs
```


### Streamlit
```bash
streamlit run .\streamlit.py 
```