# 🏥 MediTranslate: AI-Powered Healthcare Bridge

## � Screenshots
![Interface Overview](app_screenshot1.png)
![Voice Translation and Input](app_screenshot2.png)

## �📋 Project Overview
**MediTranslate** is a high-performance, full-stack web application designed to facilitate seamless, real-time communication between doctors and patients speaking different languages. Built for the **Nao Assignment**, this application leverages cutting-edge Generative AI to provide clinical-grade translation, voice processing, and medical summarization within a premium, user-centric interface.

## ✅ Features: Attempted & Completed

### Mandatory Requirements (All Completed)
- [x] **Real-Time Translation**: Synchronized translation between Doctor and Patient roles.
- [x] **Two-Way Role Support**: Dedicated interfaces for 'Doctor' and 'Patient' with role-specific language defaults.
- [x] **Text Chat Interface**: A modern, premium chat UI with clear visual distinction (glassmorphism bubbles).
- [x] **Audio Recording & Playback**: Native browser recording supported with instant playback in the conversation thread.
- [x] **Conversation Logging**: All interactions (text, audio paths, and translations) are persisted in a local SQLite database.
- [x] **Contextual Search**: Case-insensitive keyword search with real-time text highlighting.
- [x] **AI Medical Summary**: Intelligent extraction of symptoms, medications, and diagnoses using Gemini 1.5/2.5 Pro.

### Advanced Enhancements (Ship-Grade)
- [x] **Cross-Tab Synchronization**: Real-time message broadcasting across multiple browser windows using `st_autorefresh`.
- [x] **Manual Voice Control**: Added a "Send Voice 🎤" button to prevent accidental transmissions and infinite loops.
- [x] **Multi-Layer Deduplication**: Content hashing prevents redundant AI calls for the same audio data.
- [x] **Professional Aesthetics**: Custom CSS injection for a state-of-the-art Healthcare OS feel.

## 🛠️ Tech Stack
-   **Frontend/Backend**: [Streamlit](https://streamlit.io/) (Python Framework)
-   **AI Engine**: [Google Gemini 2.5 Flash](https://ai.google.dev/) (Transcription & Translation) & **Gemini 2.5 Pro** (Summarization)
-   **Database**: SQLite3 (Local relational storage)
-   **Real-time Engine**: `streamlit-autorefresh` for polling-based state sync.
-   **Styling**: Custom Vanilla CSS (Modular design tokens).

## 🧠 AI Tools & Resources Leveraged
- **Gemini 2.5 Flash**: Optimal for multimodal tasks (Audio-to-Text) and low-latency translation.
- **Gemini 2.5 Pro**: Utilized for the 'Medical Scribe' feature due to its superior reasoning in clinical summarizing.
- **Python-UUID/Hashlib**: For unique audio identity and duplicate prevention.

## 🚧 Known Limitations & Trade-offs
- **Polling vs WebSockets**: Due to the fast-tracked nature of the project (12-hour limit), I used a high-frequency polling approach (`st_autorefresh`) for real-time updates instead of an external WebSocket server. This ensures 100% reliability in a serverless/Streamlit environment.
- **Local Audio Storage**: Audio files are stored in a `/audio_files` directory. In a scaled production environment, these would be moved to S3 or Google Cloud Storage.
- **User Authentication**: Roles are currently session-based for demonstration speed. A production-ready version would implement OAuth or JWT-based auth.

## 📦 How to Run Locally

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set API Key**:
   Create `.streamlit/secrets.toml` and add:
   ```toml
   [general]
   GEMINI_API_KEY = "your_key_here"
   ```

3. **Launch**:
   ```bash
   python -m streamlit run app.py
   ```

---
*Created as part of the Nao Technical Assessment.*
