# 🛡️ PhishGuard | AI-Driven Threat Intelligence

**PhishGuard** is a high-performance, professional-grade cybersecurity platform designed to detect and neutralize sophisticated phishing attempts using a hybrid approach of **Heuristic Triage** and **Machine Learning Analysis**. 

![Status](https://img.shields.io/badge/Status-v3.0_Stable-orange?style=for-the-badge)
![ML Engine](https://img.shields.io/badge/Engine-Random_Forest_%2B_NLP-success?style=for-the-badge)
![UI](https://img.shields.io/badge/UI-Premium_Glassmorphism-blueviolet?style=for-the-badge)

---

## 📖 Complete User Manual

Welcome to **PhishGuard**! This section is designed to walk you step-by-step through setting up, configuring, and effectively using the platform.

### System Requirements & Dependencies
Before installing, ensure you have the following installed on your machine:
*   **Python 3.10 or higher**: Required for core execution.
*   **pip**: Python package manager for installing dependencies.

**Major Libraries Used**:
*   `Flask==3.0.0`: Powers the backend server and REST APIs.
*   `flask-cors`: Handles Cross-Origin Resource Sharing.
*   `flask-socketio`: Enables real-time communication for the dashboard.
*   `scikit-learn==1.3.2` & `joblib==1.3.2`: Forms the core of the Machine Learning Engine (Random Forest).
*   `nltk==3.8.1`: Natural Language Toolkit used for text preprocessing (Tokenization, Lemmatization, Stop-words removal).
*   `dnspython` & `email-validator`: Ensures emails and headers are properly structurally evaluated.

---

### Step 1: Installation & Setup
1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/your-repo/phishguard.git
    cd phishguard
    ```
2.  **Create a Virtual Environment**:
    This isolates dependencies so they do not conflict with your system.
    ```bash
    python -m venv venv
    ```
    *Activate it:*
    - **Windows**: `venv\Scripts\activate`
    - **Linux/Mac**: `source venv/bin/activate`
3.  **Install the Required Tooling**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Initialize the Massive ML Dataset (Optional but Recommended)**:
    PhishGuard includes a procedural data engine that can generate thousands of diverse training samples to maximize the Random Forest accuracy.
    ```bash
    python dataset/generate_dataset.py
    ```
    This auto-creates `phishing_data.csv` with 15,000 highly-varied email structures. You can then train the model accurately!

### Step 2: Running the Project
1.  **Start the Server**:
    ```bash
    python app.py
    ```
2.  **Access the Dashboard**:
    Open a modern web browser and navigate to `http://localhost:5000`. You will see the PhishGuard application interface.

> **Note on NLTK Downloads**: The first time you execute a scan or start the app, PhishGuard might automatically download `stopwords` and `wordnet` corpora from NLTK. This is normal and takes only a few seconds.

---

### Step 3: How to Use the Email Scanner
PhishGuard's scanner accepts **two main formats** of inputs in the "Email Analyzer" tab:

#### Mode A: Pasting Raw EML (With Headers) - Recommended 
If you have access to the raw email source (including `Subject:`, `From:`, `To:`, etc.):
1.  Copy the entire raw text block.
2.  Paste it into the terminal box on the **Email Analyzer** page.
3.  Click `RUN AI DIAGNOSTICS`. 
4.  *Benefit: This allows the engine to check for Authentication anomalies (SPF/DKIM/DMARC) as well as Behavioral Text features.*

#### Mode B: Pasting Plain Text (Email Body Only)
If you only want to quickly check the body of an email or random suspicious text:
1.  Just copy the text content.
2.  Paste it into the terminal box.
3.  Click `RUN AI DIAGNOSTICS`.
4.  *Benefit: The system is perfectly adapted for this. It will safely ignore missing SMTP headers so it won't wrongly penalize your score, and relies entirely on Deep Text NLP patterns and URL heuristics.*

---

### Step 4: Understanding The UI and Dashboards
*   **The Dashboard Tab**: Shows your total scanned emails, threats blocked, and safe artifacts verified.
*   **ML Engine Indicator**: In the bottom left corner, you will see `ML Engine: ACTIVE`. If for any reason your `.pkl` model files (Random Forest models) go missing or fail to load, the system degrades safely to `OFFLINE (Heuristic)`, using fallback rules to keep you safe.
*   **Risk Meter**: 
    *   `0-30%`: Likely Safe.
    *   `31-60%`: Proceed with Caution.
    *   `60-100%`: Action Blocked (Phishing Detected).

---

### 💡 Pro Tip: How to Export .eml from Gmail
To test the scanner with a real email from your Gmail inbox:
1.  Open the email you want to analyze.
2.  Click the **three vertical dots** (More) next to the "Reply" button.
3.  Select **"Download message"**.
4.  This will save a `.eml` file to your computer.
5.  In PhishGuard, click **UPLOAD .EML** and select that file to run an automatic AI diagnostic!

---

## 🛠️ Troubleshooting & Solutions

*   **Error: "ML ENGINE DEGRADED" / "idf vector not fitted"**
    *   **Solution**: This happens if the `tfidf_vectorizer.pkl` lacks vocabulary or the model files are corrupted. Thanks to PhishGuard's Interactive Fallback UI, you don't even need to touch the terminal! When this error appears on your dashboard, simply click **Retrain ML Model** to automatically fix the corrupted models, or click **Use Rule-Based Fallback** to skip ML and use the heuristic engine.
*   **Error: "ANALYSIS FAILED" in GUI**
    *   **Solution**: Ensure you actually pasted text into the analyzer. Empty inputs are caught and rejected.
*   **Error: NLTK Resource Not Found**
    *   **Solution**: Since version 3.0, the script (`nlp_processor.py`) attempts to safely auto-download missing models. If it fails, run python and execute: `import nltk; nltk.download('stopwords'); nltk.download('wordnet')`.
*   **Warning: "Model files not found" in Server Console**
    *   **Solution**: You are missing the pretrained `rf_model.pkl` and `tfidf_vectorizer.pkl` files inside the `models/` directory. Use `dataset/generate_dataset.py` followed by `backend/models/train_model.py` to generate them. The application will continue functioning by dynamically switching to a Rule-Based Heuristic engine.
*   **Port 5000 Already in Use**
    *   **Solution**: Change `port=5000` to `port=8080` in `app.py`.

---

## 📂 Project Architecture

```text
phishguard/
├── backend/                # Core Application Logic
│   ├── models/             # ML Integration (Feature mapping & the Random Forest bridge)
│   ├── routes/             # RESTful APIs (Handles JSON communication to the frontend)
│   ├── static/             # Frontend Assets (Glass UI, Advanced JS, Style Tooling)
│   ├── templates/          # HTML5 User Interfaces
│   └── utils/              # NLP & Text Utilities (Parsing & Safety fallbacks)
├── dataset/                # Training Data for the AI Engine
├── models/                 # Pre-trained ML weights (.pkl)
├── tests/                  # Unit & Integration Tests
└── app.py                  # Server/Application Entry Point
```

## 🔮 Future Roadmap
1.  **Transformer Integration**: Upgrading to **BERT** for contextual embeddings.
2.  **Automated Quarantine**: Plug into live IMAP/SMTP nodes to push directly to junk.
3.  **Browser Addon Sync**: On-the-fly DOM scanning in browser interfaces.

---
<div align="center">
    <i>Developed by - Kushal Soni </i>
</div>
