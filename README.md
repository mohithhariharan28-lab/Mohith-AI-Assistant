# Mohith AI Assistant

Mohith AI Assistant is a complete, production-ready ChatGPT-like AI workspace built using **Python**, **Streamlit**, and the **OpenAI API**. It features a modern Navy Blue theme, persistent session chats, prompt engineering styles (Concise, Medium, and Detailed), response metrics, clipboard utilities, session archiving, and user feedback collection.

---

## 🚀 Key Features

1. **Intelligent Chat Workspace**: Interactive interface supporting real-time streaming, conversation states, and direct prompt engineering style switches.
2. **Modular AI Tools**:
   - **Answer Questions**: Delivers customized answers with selectable depth.
   - **Text Summarizer**: Summarizes content into sentences, bullet points, or executive reports.
   - **Business Idea Generator**: Generates lean startup proposals or comprehensive business models.
   - **Story Generator**: Compiles short stories ranging from flash fiction to rich, detailed narrative chapters.
   - **Email Writer**: Drafts professional business communication from short snippets to corporate memos.
   - **Resume Helper**: Rewrites bullet points, summarizes experience, and suggests ATS keywords.
   - **Study Assistant**: Creates revision cards, quiz questions, and study explanations.
3. **Response Features**:
   - Word count and response time metrics.
   - Fast raw code / text copying.
   - Download response directly as `.txt`.
   - Response regeneration.
4. **Persistent History Manager**: Start new chats, clear current sessions, and retrieve or restore past conversations during the session.
5. **CSV Feedback Logging**: Evaluate model helpfulness and save responses alongside user remarks in `feedback.csv` for analysis.
6. **Customizable settings**: Easily adjust GPT Models (`gpt-4o`, `gpt-4o-mini`, `gpt-3.5-turbo`), generation temperature (0.0 to 2.0), and max token limits.

---

## 📁 Repository Structure

```
Mohith AI Project/
├── app.py                  # Main Streamlit application and layout routing
├── ai_client.py            # OpenAI API wrapper and error handling routines
├── prompts.py              # System prompts & structures for all styles/features
├── utils.py                # Visual styling, word count calculations, CSV database helpers
├── config.py               # Global settings, model profiles, and environment config
├── requirements.txt        # Package dependencies
├── .env.example            # Environment variables template
├── README.md               # Project overview
├── INSTALLATION_GUIDE.md   # Setup and configuration manual
└── USER_GUIDE.md           # User manual and Prompt Engineering features guide
```

---

## 🛠️ Tech Stack

- **Frontend/Application Framework:** Streamlit (v1.30.0+)
- **API Client:** OpenAI Python SDK (v1.0.0+)
- **Environment Management:** python-dotenv
- **Data logging/analytics:** pandas & CSV

---

## 📜 Guides & Documentation

To set up and utilize this application, please refer to the following documentation:
- [Installation Guide](file:///c:/Users/aparn/OneDrive/Documents/Pictures/Mohith%20AI%20Project/INSTALLATION_GUIDE.md): Step-by-step tutorial on python installation, virtual environment setup, package installer instructions, and environment configuration.
- [User Guide](file:///c:/Users/aparn/OneDrive/Documents/Pictures/Mohith%20AI%20Project/USER_GUIDE.md): Description of the interface, prompt library patterns, settings optimization, and feedback review options.
