# Installation & Setup Guide - Mohith AI Assistant

Follow these steps to set up, configure, and launch the Mohith AI Assistant on your local development machine.

---

## 📋 Prerequisites

Before starting, ensure you have the following installed:
1. **Python 3.9 or higher**: [Download Python](https://www.python.org/downloads/) (Make sure to check "Add Python to PATH" during installation on Windows).
2. **OpenAI API Key**: Obtain a secret key from the [OpenAI Developer Portal](https://platform.openai.com/).

---

## ⚙️ Step-by-Step Installation

### Step 1: Clone or Copy the Workspace
Navigate to the directory containing your workspace files:
```bash
cd "c:\Users\aparn\OneDrive\Documents\Pictures\Mohith AI Project"
```

### Step 2: Set Up a Virtual Environment (Recommended)
Creating a virtual environment ensures that the packages do not conflict with your global Python environment:

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Packages
Install the required packages using `pip`:
```bash
pip install -r requirements.txt
```

This installs:
- `streamlit` - The application framework.
- `openai` - Standard OpenAI API client library.
- `python-dotenv` - Environment variable loader.
- `pandas` - Analytics loader for feedback.

### Step 4: Configure API Credentials
Create your environment variables file to store your OpenAI API Key securely:

1. Copy the `.env.example` template:
   ```bash
   copy .env.example .env
   ```
2. Open the newly created `.env` file in your text editor.
3. Replace the placeholder text with your actual API key:
   ```env
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

*Note: You can also choose to leave the API key blank in `.env` and configure it dynamically under the **Settings** menu page in the running web app.*

---

## 🚀 Running the Application

Launch the Streamlit developer web server:
```bash
streamlit run app.py
```

Upon executing this command:
1. Streamlit compiles and launches the application container.
2. A new browser tab should automatically open at `http://localhost:8501`.
3. If it does not open automatically, copy and paste the network link displayed in your terminal.

---

## 🛠️ Verification & Testing

To confirm the setup has completed successfully:
1. Navigate to the **Settings** tab in the sidebar menu.
2. Check the model configurations or type your API key (if not loaded from `.env`).
3. Click **Validate API Key**. A green banner saying *"API Key is VALID and working!"* confirms successful communication.
4. Navigate to the **Chat** tab, select a feature, and submit a query to start chatting.
