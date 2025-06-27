# 📷 SnapAI (Windows)

**SnapAI** is a lightweight floating panel app for **Windows** that monitors your screenshot folder, extracts text using OCR, and sends it to the **Groq LLaMA 3 API** to generate intelligent answers.

Perfect for answering quizzes, fill-in-the-blanks, and MCQs from screenshots.

---

## ✨ Features

- 📸 Monitors `Screenshots` folder for new screenshots
- 🧠 Extracts text using [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- 💬 Sends text to Groq’s **LLaMA 3** model via API
- 🪟 Always-on-top transparent floating UI
- ✅ Start / Stop / Quit controls
- 📋 Logs saved to `~/snapai_log.txt`

---

## ⚙️ Setup Instructions (Windows)

### 1. Open Terminal
On Windows, you can use:

Command Prompt → Press Win + R, type cmd, press Enter

### 2. Navigate to the folder you want
Example: You want to put the SnapAI project in your Documents folder:

```bash
cd C:\Users\YourName\Documents
```

### 3. Clone this Repository

```bash
git clone https://github.com/yourusername/SnapAI_Windows.git
cd SnapAI_Windows
```
Refer to the steps below to download git.

#### 1. Download Git for Windows

Visit: https://git-scm.com/download/win
It should start downloading automatically.

#### 2. Install Git

Run the installer.
On the setup screen, keep all default settings.
Most importantly:
✅ Ensure "Git from the command line and also from 3rd-party software" is selected (this adds Git to your PATH).

#### 3. Restart Command Prompt

After installing, close and reopen Command Prompt to reload the environment.

### 4. Get a Groq API Key
1. Go to https://console.groq.com/keys
2. Sign up or log in with your account.
3. Click "Create API Key"
4. Copy the key (starts with gsk_...)

### 5. Create a `.env` file with your API key:

```bash
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

### 6. Install dependencies:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 7. Run the app:

```bash
python SnapAI.py
```

---

## Requirements

- Windows OS
- Tesseract OCR
- Python 3.8 or later

## Install Tesseract OCR on Windows
  
### 1. Download the Windows installer:
https://github.com/UB-Mannheim/tesseract/wiki

### 2. Install it to the default path:
C:\Program Files\Tesseract-OCR\tesseract.exe

