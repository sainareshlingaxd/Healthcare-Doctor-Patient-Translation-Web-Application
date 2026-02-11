
import google.generativeai as genai
import streamlit as st
import os
import toml

def check_models():
    try:
        # Load key
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
        elif "general" in st.secrets and "GEMINI_API_KEY" in st.secrets["general"]:
            api_key = st.secrets["general"]["GEMINI_API_KEY"]
        else:
            api_key = os.getenv("GEMINI_API_KEY")
            
        if not api_key:
            # Try to load from file manually
            try:
                secrets = toml.load(".streamlit/secrets.toml")
                api_key = secrets.get("GEMINI_API_KEY") or secrets.get("general", {}).get("GEMINI_API_KEY")
            except:
                pass
                
        if not api_key:
            print("No API Key found.")
            return

        genai.configure(api_key=api_key)
        print("Available models:")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_models()
