from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import re
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer

model = joblib.load("Fake_news_detection_SVM_99.4%")
vectorizer = joblib.load("Fake_News_Vectorizer")

tokenizer = RegexpTokenizer(r'\w+')
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    tokens = tokenizer.tokenize(text)
    cleaned_text = [lemmatizer.lemmatize(w) for w in tokens if w not in stop_words and len(w)>2]
    return ' '.join(cleaned_text)

app = FastAPI()

class NewsInput(BaseModel):
    text: str

@app.post("/predict")
def predict(data: NewsInput):
    processed_text = preprocess(data.text)
    vect_text = vectorizer.transform([processed_text])
    prediction = model.predict(vect_text)[0]
    
    return {"prediction": int(prediction)}
