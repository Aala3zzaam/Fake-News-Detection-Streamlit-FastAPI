import streamlit as st 
import requests

st.title("📰 Fake News Detector")

user_input = st.text_area("Enter a news article or headline: ")

if st.button('Predict'):
    if user_input.strip() != "":
        payload = {"text": user_input.strip()} 
        try:
            response = requests.post("http://127.0.0.1:8000/predict", json=payload)
            result = response.json()
            prediction = result["prediction"]
            
            if prediction == 0:
                st.subheader("Prediction: 🚨 Fake News")
                st.error("The input looks like FAKE news.")
            else:
                st.subheader("Prediction: ✅ Real News")
                st.success("The input looks like REAL news.")
        except Exception as e:
            st.error(f"Error: {e}")
