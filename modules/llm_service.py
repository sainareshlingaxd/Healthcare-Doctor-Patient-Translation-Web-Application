
import google.generativeai as genai
import streamlit as st
import os

# Configure the API key from Streamlit secrets
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    elif "general" in st.secrets and "GEMINI_API_KEY" in st.secrets["general"]:
         genai.configure(api_key=st.secrets["general"]["GEMINI_API_KEY"])
    else:
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
except Exception as e:
    print(f"Error loading secrets: {e}")

# Recommended models for 2026 environment
PRIMARY_MODEL = 'gemini-2.5-flash'
PREMIUM_MODEL = 'gemini-2.5-pro'

def get_model(model_name=PRIMARY_MODEL):
    return genai.GenerativeModel(model_name)

def handle_error(e):
    if "429" in str(e):
        return "⚠️ Quota Exceeded/Rate Limited. Please wait a few seconds and try again. AI is currently busy."
    if "404" in str(e):
        return "⚠️ Model not found. Please check API settings."
    return f"AI Error: {e}"

def translate_text(text, target_language):
    """
    Translate text using Gemini 2.5-flash.
    """
    model = get_model(PRIMARY_MODEL)
    prompt = (
        f"You are a professional medical translator. Translate the following message into {target_language}. "
        "Maintain clinical accuracy. Return ONLY the translated text.\n\n"
        f"Message: {text}"
    )
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return handle_error(e)

def summarize_conversation(history_text):
    """
    Summarize the medical conversation.
    """
    if not history_text.strip():
        return "No conversation history to summarize."
        
    model = get_model(PREMIUM_MODEL)
    prompt = f"""
    You are a specialized medical scribe. Analyze the following conversation.
    Generate a concise, professional medical summary.
    
    Structure:
    - **Patient Concerns & Symptoms**
    - **Clinical Observations**
    - **Diagnosis/Impression**
    - **Prescribed Medications & Treatments**
    - **Follow-up Plan**
    
    Conversation History:
    {history_text}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return handle_error(e)

def transcribe_and_translate(audio_path, target_language):
    """
    Transcribe and translate using Gemini 2.5-flash.
    """
    model = get_model(PRIMARY_MODEL)
    
    try:
        myfile = genai.upload_file(audio_path)
        prompt = (
            f"1. Transcribe the audio accurately. "
            f"2. Translate the transcription into {target_language}. "
            "Return: 'Original: <transcript> | Translated: <translation>'"
        )
        
        response = model.generate_content([prompt, myfile])
        return response.text.strip()
    except Exception as e:
        return handle_error(e)
