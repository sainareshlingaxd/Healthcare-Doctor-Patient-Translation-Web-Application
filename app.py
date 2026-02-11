
import streamlit as st
from modules import db, llm_service, audio_utils
import os
import hashlib
import time
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Page Config
st.set_page_config(
    page_title="MediTranslate | Doctor-Patient Bridge",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables early
if 'db_initialized' not in st.session_state:
    db.init_db()
    st.session_state['db_initialized'] = True
if 'audio_key_index' not in st.session_state:
    st.session_state['audio_key_index'] = 0
if 'processed_audio_hashes' not in st.session_state:
    st.session_state['processed_audio_hashes'] = set()
if 'is_processing' not in st.session_state:
    st.session_state['is_processing'] = False

# Only Refresh if we aren't currently middle of a translation or recording action
if not st.session_state['is_processing']:
    st_autorefresh(interval=5000, key="datarefresh") # 5 seconds for better stability

# Load CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar Logic
# ... (rest of sidebar code)
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #00D1FF; font-family: Outfit;'>MediTranslate</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    role = st.radio("My Role", ("Doctor", "Patient"), help="Select your current role in the conversation.")
    
    st.markdown("---")
    st.subheader("Language Settings")
    
    # Language Selection Logic
    if role == "Doctor":
        target_language = st.selectbox(
            "Translate to (Patient's Language)", 
            ["Spanish", "French", "Hindi", "Chinese", "German", "Telugu", "Tamil"],
            index=2 
        )
    else:
        target_language = st.selectbox(
            "Translate to (Doctor's Language)", ["English"], index=0
        )

    st.markdown("---")
    st.subheader("Search & Filter")
    search_query = st.text_input("🔍 Search matches in history", placeholder="Keywords...")
    
    st.markdown("---")
    st.subheader("Actions")
    
    if st.button("✨ Generate AI Medical Summary", use_container_width=True):
        st.session_state['is_processing'] = True
        history_all = db.get_history()
        full_text = "\n".join([f"{msg[0]}: {msg[1]}" for msg in history_all])
        with st.status("Analyzing conversation...", expanded=True) as status:
            summary = llm_service.summarize_conversation(full_text)
            status.update(label="Summary Generated!", state="complete", expanded=False)
        st.session_state['show_summary'] = summary
        st.session_state['is_processing'] = False
        st.rerun()

    if st.button("🗑️ Clear Conversation", use_container_width=True, type="secondary"):
        db.clear_history()
        st.rerun()

# Main Interface
st.markdown("<div class='main-header'>Doctor-Patient Translation Bridge</div>", unsafe_allow_html=True)

if 'show_summary' in st.session_state:
    with st.expander("📊 Latest AI Medical Summary", expanded=True):
        st.markdown(st.session_state['show_summary'])
        if st.button("Close Summary"):
            del st.session_state['show_summary']
            st.rerun()

# Handle Search vs History
if search_query:
    history = db.search_messages(search_query)
else:
    history = db.get_history()

# Chat Display Container
chat_container = st.container()
with chat_container:
    if not history:
        st.info("No messages yet. Start the conversation below!")
    for msg in history:
        msg_role, original, translated, audio_path, timestamp = msg
        display_original = original
        display_translated = translated
        if search_query:
            import re
            insensitive_search = re.compile(re.escape(search_query), re.IGNORECASE)
            display_original = insensitive_search.sub(f"<mark style='background: #ffd700; color: black;'>{search_query}</mark>", original)
            display_translated = insensitive_search.sub(f"<mark style='background: #ffd700; color: black;'>{search_query}</mark>", translated)

        bubble_class = "doctor-msg" if msg_role == "Doctor" else "patient-msg"
        st.markdown(f"""
        <div class="message-bubble {bubble_class}">
            <div class="role-label">{msg_role}</div>
            <div class="original-text">{display_original}</div>
            <div class="translated-text">Translated: {display_translated}</div>
            <div class="timestamp">{timestamp}</div>
        </div>
        """, unsafe_allow_html=True)
        if audio_path and os.path.exists(audio_path):
            st.audio(audio_path)

# Input Area
st.markdown("---")
input_col, audio_col = st.columns([0.8, 0.2])

with input_col:
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("", placeholder=f"Type message as {role}...", label_visibility="collapsed")
        submit_button = st.form_submit_button("Send ➔", use_container_width=True)

with audio_col:
    audio_value = st.audio_input("Record", key=f"audio_input_{st.session_state['audio_key_index']}")
    # Show manual send button once audio is captured
    send_voice = st.button("Send Voice 🎤", use_container_width=True, type="primary", disabled=not audio_value)

# TEXT SUBMISSION
if submit_button and user_input:
    st.session_state['is_processing'] = True
    with st.spinner("Translating..."):
        translated_text = llm_service.translate_text(user_input, target_language)
        db.save_message(role, user_input, translated_text)
    st.session_state['is_processing'] = False
    st.rerun()

# AUDIO SUBMISSION (Manual Trigger)
if audio_value and send_voice:
    st.session_state['is_processing'] = True
    with st.spinner("Processing Audio Message..."):
        audio_bytes = audio_value.getvalue()
        audio_path = audio_utils.save_audio(audio_bytes)
        
        result = llm_service.transcribe_and_translate(audio_path, target_language)
        
        original_text = "[Audio Message]"
        translated_text = result
        
        if "Original:" in result and "| Translated:" in result:
            parts = result.split("| Translated:")
            original_text = parts[0].replace("Original:", "").strip()
            translated_text = parts[1].strip()
        
        db.save_message(role, original_text, translated_text, audio_path)
        
        # Reset the recorder by changing its key
        st.session_state['audio_key_index'] += 1
        
    st.session_state['is_processing'] = False
    st.rerun()

