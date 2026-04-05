<div align="center">
  <h1>🛡️ PhishGuard</h1>
  <p><strong>An AI-Powered Phishing Email Detector with Gmail Integration</strong></p>
  
  <p>
    <img alt="Python" src="https://img.shields.io/badge/Python-3.11+-blue.svg" />
    <img alt="Flask" src="https://img.shields.io/badge/Flask-Backend-green.svg" />
    <img alt="Machine Learning" src="https://img.shields.io/badge/ML-Random%20Forest-orange.svg" />
    <img alt="Chrome Extension" src="https://img.shields.io/badge/Extension-Chrome-yellow.svg" />
  </p>
</div>

---

## 🌟 What is PhishGuard?

**PhishGuard** is a complete cybersecurity tool designed to help you catch malicious, scam, and phishing emails before they do harm. 

It acts as your personal email bodyguard by using **Machine Learning** to read and analyze email content, links, and attachments behind the scenes. If something looks suspicious, PhishGuard warns you immediately!

### ✨ Key Features:
* 🧠 **Smart AI Engine:** Uses a Machine Learning model (Random Forest + TF-IDF) to understand email text and identify hidden phishing traits.
* 🌐 **Real-Time Web Dashboard:** A beautiful dashboard that receives live alerts via WebSockets when suspicious emails are scanned.
* 🧩 **Gmail Chrome Extension:** Seamlessly integrates a "Scan with PhishGuard" button directly into your Gmail inbox!
* 🔍 **Manual Scanning:** Don't use Gmail? No problem. You can copy and paste raw emails (`.eml` source) directly into the dashboard for an instant security check.

---

## 🚀 How to Get Started (Beginner Friendly!)

Setting up PhishGuard is simple. Just follow these steps in your terminal.

### 1. Install Requirements
First, make sure you have Python installed. Then, set up your environment and install the required packages:

```bash
# Move into the project folder
cd phishguard

# Create and activate a Virtual Environment
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install all the necessary packages
pip install -r requirements.txt

# Download required natural language processing data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

### 2. Generate Data & Train the AI Model
Before the engine can detect phishing, it needs to be trained on data! We've included a script to automatically generate synthetic data and train the AI for you.

```bash
# 1. Generate 5,000 realistic synthetic emails
python dataset/download_data.py

# 2. Train the Machine Learning Model
PYTHONPATH=.. python backend/models/train_model.py
```
*(The trained AI models will automatically save to the `models/` directory!)*

### 3. Start the Backend Server
Now that your AI is smart and ready, start the Flask Web Server!

```bash
# Start the server and dashboard
PYTHONPATH=.. python backend/app.py
```
🎉 **Success!** You can now open your browser and go to `http://localhost:5000/` to see your dashboard!

---

## 🧩 Installing the Chrome Extension

To get the magic Gmail button, you need to load the extension into Chrome:

1. Open Google Chrome and type `chrome://extensions/` in your URL bar.
2. Turn on **Developer mode** (toggle switch in the top right corner).
3. Click the **Load unpacked** button in the top left.
4. Select the `phishguard/extension/` folder from this project.
5. **Done!** Open Gmail, click on any email, and you'll see the shiny new **Scan with PhishGuard** button next to the email header!

---

## 🧪 Testing the System
Want to make sure everything is working perfectly under the hood? Run our automated tests:
```bash
PYTHONPATH=.. pytest tests/
```

## 🛠️ Built With
* **Backend:** Python, Flask, Flask-SocketIO
* **Machine Learning:** Scikit-Learn (Random Forest Engine), Pandas, NLTK
* **Frontend/Extension:** HTML, CSS, JavaScript (Chrome Manifest V3)
