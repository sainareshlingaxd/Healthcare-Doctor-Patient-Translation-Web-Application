# 🏥 MediTranslate: AI-Powered Healthcare Bridge

<img width="2875" height="1559" alt="Screenshot 2026-02-11 134217" src="https://github.com/user-attachments/assets/07ed89db-1d9d-4ca3-bbed-164fcda71361" />
<img width="2878" height="1557" alt="Screenshot 2026-02-11 134241" src="https://github.com/user-attachments/assets/704f367e-03ea-463f-84a4-d39eefccb7f2" />

## 📸 Screenshots
![Interface Overview]
![Voice Translation and Input]

## Live Link
https://healthcare-doctor-patient-translation-web-application-enbnaef2.streamlit.app/

## 📋 Project Overview
**MediTranslate** is a high-performance, full-stack web application designed to facilitate seamless, real-time communication between doctors and patients speaking different languages. Built as a clinical communication bridge for the **Nao Technical Assessment**, this application leverages cutting-edge Generative AI to provide clinical-grade translation, voice processing, and medical summarization within a premium interface.

## 🏗️ Project Structure
The project is organized into modular components to ensure clean separation of concerns and high maintainability:

```text
Nao Assignment/
├── app.py                # Main Application Entry Point & Responsive UI
├── style.css             # Premium Healthcare Design System (Glassmorphism)
├── chat.db               # Transaction-safe SQLite Database (Auto-generated)
├── audio_files/          # Directory for clinical audio message storage
├── modules/              # Specialized Logic Modules
│   ├── db.py             # Database Abstraction Layer (WAL mode enabled)
│   ├── llm_service.py    # LLM Integration (Gemini 2.5 API & Prompt Engineering)
│   └── audio_utils.py    # Multimodal File Handling & Logic
├── .streamlit/           
│   └── secrets.toml      # Local Configuration & Security (Ignored by Git)
├── requirements.txt      # Project Dependency Manifest
└── README.md             # Technical Documentation & Project Summary
```

## 🛠️ Detailed Tech Stack
-   **Execution Framework**: [Streamlit v1.40+](https://streamlit.io/) - Selected for its reactive state management and low-latency UI rendering.
-   **Multimodal AI Logic**: [Google Gemini 2.5 Flash](https://ai.google.dev/) - Utilized for high-speed voice-to-text transcription and clinical translation.
-   **Clinical Intelligence**: [Google Gemini 2.5 Pro](https://ai.google.dev/) - Deployed for the "Medical Scribe" feature to perform high-reasoning summarization of symptoms and treatments.
-   **Data Architecture**: [SQLite3](https://www.sqlite.org/index.html) - Optimized with **Write-Ahead Logging (WAL)** for seamless concurrency in multi-user healthcare environments.
-   **Real-time Engine**: Polling-based orchestration via `streamlit-autorefresh` allowing for decoupled Doctor/Patient synchronization.
-   **Design Language**: Custom Pure CSS implementation of **Glassmorphism**, focused on accessibility, role-based visual cues, and mobile responsiveness.

## 🤖 AI Partnership & Development Process
This application was engineered in a collaborative pair-programming partnership with **Antigravity**, Google DeepMind's advanced coding agent. The development workflow included:
- **Architectural Design**: Designing a "processing lock" to handle high-frequency polling errors and audio duplication loops.
- **Prompt Engineering**: Crafting clinical-specific instructions to ensure Gemini models maintain professional medical terminology.
- **Cloud Optimization**: Hardening the application for Streamlit Community Cloud through absolute pathing and secure secret management.

## ✅ Features: Attempted & Completed
### Mandatory Requirements
- [x] **Real-Time Translation**: Near-instant translation between Doctor and Patient sessions.
- [x] **Two-Way Role Support**: Independent dashboards for Doctors and Patients.
- [x] **Text Chat Interface**: High-fidelity UI with clear message distinction.
- [x] **Audio Recording & Playback**: Integrated browser recording with manual submission control.
- [x] **Conversation Logging**: Reliable clinical logging in SQLite with timestamps.
- [x] **Contextual Search**: Optimized keyword search with case-insensitive highlights.
- [x] **AI Medical Summary**: Intelligent extraction of symptoms, medications, and plans.

### Advanced Enhancements
- [x] **Manual Submission Mode**: Added a "Send Voice 🎤" button to provide user control and eliminate infinite loops.
- [x] **De-duplication System**: Content hashing (MD5) to prevent redundant AI calls for audio data during UI refreshes.
- [x] **Cloud Persistence Stability**: Specialized absolute pathing logic for stable deployment.

## 🚧 Known Limitations & Technical Trade-offs
- **Persistence Strategy**: As per Requirement #4, conversation history persists across sessions. However, to maintain high performance on Streamlit Cloud's ephemeral storage, `chat.db` is managed as a server-side resource rather than a versioned artifact in Git.
- **Latency Balancing**: A 5-second polling interval was chosen as the optimal balance between real-time feeling and API rate-limit conservation.
- **Security Protocols**: All sensitive configurations are managed via Streamlit's secrets engine to ensure high security during public deployment.

## 📦 Local Setup Instructions
1. **Clone & Install**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure API Key**:
   Create `.streamlit/secrets.toml`:
   ```toml
   [general]
   GEMINI_API_KEY = "your_active_gemini_key"
   ```
3. **Run Application**:
   ```bash
   python -m streamlit run app.py
   ```

---
*Developed for the Nao Technical Assessment.*
