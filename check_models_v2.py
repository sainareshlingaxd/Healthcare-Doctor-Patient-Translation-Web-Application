
import google.generativeai as genai
import streamlit as st
import os
import toml

def check_models():
    try:
        # Load key
        api_key = None
        try:
            secrets = toml.load(".streamlit/secrets.toml")
            api_key = secrets.get("GEMINI_API_KEY") or secrets.get("general", {}).get("GEMINI_API_KEY")
        except:
            pass
            
        if not api_key:
            api_key = os.getenv("GEMINI_API_KEY")
            
        if not api_key:
            with open("models_debug.txt", "w") as f:
                f.write("No API Key found.")
            return

        genai.configure(api_key=api_key)
        models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                models.append(m.name)
        
        with open("models_debug.txt", "w") as f:
            f.write("\n".join(models))
    except Exception as e:
        with open("models_debug.txt", "w") as f:
            f.write(f"Error: {e}")

if __name__ == "__main__":
    check_models()
