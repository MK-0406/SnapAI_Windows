# 📷 SnapAI (Windows)

**SnapAI** is a lightweight floating panel app for **Windows** that monitors your screenshot folder, extracts text using OCR, and sends it to the **Gemini 2.5 Flash API** to generate intelligent answers.

Perfect for answering quizzes, fill-in-the-blanks, and MCQs from screenshots.

---

## ✨ Features

- 📸 Detects screenshots from both clipboard and folder
- 🧠 Extracts text using [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- 💬 Sends text to Google's **Gemini 2.5 Flash** model via API
- 🪟 Always-on-top transparent floating UI
- ✅ Start / Stop / Quit controls
- 📋 Logs saved to `~/snapai_log.txt`

---

## ⚙️ Setup Instructions (Windows)

### 1. Download the whole folder
Unzip the folder in your Downloads folder

### 2. Open Terminal
On Windows, you can use:

Command Prompt → Press Win + R, type cmd, press Enter

### 3. Navigate to the SnapAI folder

```bash
cd C:\Users\YourName\Downloads\SnapAI_Windows-main\SnapAI_Windows-main
```

### 4. Get a Gemini API Key
1. Go to https://aistudio.google.com/app/apikey
2. Sign up or log in with your Google account.
3. Click "Create API Key"
4. Copy the key 

### 5. Create a `.env` file with your API key:

```bash
echo GOOGLE_API_KEY=your_google_api_key_here > .env
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
- Python 3.13

---

## Install Tesseract OCR on Windows
  
### 1. Download the Windows installer:
https://github.com/UB-Mannheim/tesseract/wiki

### 2. Run the installer (.exe) and install it to the default path:
C:\Program Files\Tesseract-OCR\tesseract.exe

---

## 📘 User Manual

### 🖥️ Interface
A floating window will appear with:
- Welcome message
- Scrollable response area
- Start, Stop, and Quit buttons

### ▶️ Start Monitoring
Click Start to begin monitoring your Screenshots folder (Pictures\Screenshots). When a new screenshot is added:

1. The image is scanned with OCR.
2. Text is sent to the Gemini AI.
3. The panel displays the AI-generated response.
   
### ⏹️ Stop Monitoring
Click Stop to stop watching for new screenshots.

### ❌ Quit
Click Quit to close the app.

---
