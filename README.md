Here’s a **GitHub-ready, professional README** (with badges, clean formatting, and project polish 👇):

---

# 🎙️ Swar Connect

### Multilingual Audio Messaging System for Seamless Communication

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![Status](https://img.shields.io/badge/Project-Active-success)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🌐 Overview

**Swar Connect** is an AI-powered multimodal communication system designed to enable seamless voice-based interaction across different languages.

Built as a **BTech project**, the application bridges communication gaps by converting spoken input into **text, translating it into multiple Indian languages, and generating corresponding audio output** — all in real time.

---

## 🚀 Features

### 🎙️ Audio Messaging

* Record voice messages directly in-browser
* Simulates real-time **VoIP-style communication**

### 🧠 AI-Powered Processing

* 🔊 **Speech-to-Text (ASR)** using SpeechRecognition
* 🌍 **Multilingual Translation** across Indian languages
* 🔁 **Text-to-Speech (TTS)** for translated audio playback

### 📱 User Experience

* Mobile-style interface
* Separate **Sender** and **Receiver** tabs
* Real-time inbox simulation

### 🌏 Supported Languages

Hindi • English • Bengali • Marathi • Tamil • Gujarati • Malayalam • Punjabi • Assamese • Odia • Rajasthani

### ⚡ Backend Pipeline

```
Audio → Speech Recognition → Translation → Text-to-Speech → Output
```

---

## 🏗️ Architecture

### 🔄 Data Flow

1. **Audio Input**

   * Captured via `streamlit-mic-recorder`

2. **Speech Recognition**

   * Converts audio → text

3. **Translation Engine**

   * Uses `googletrans` for multilingual conversion

4. **Voice Generation**

   * Uses `gTTS` for translated speech output

5. **Relay Mechanism**

   * Data stored in shared memory (`global_vault`)

6. **Output**

   * Receiver selects preferred language → gets translated audio + transcript

---

## 🛠️ Tech Stack

| Layer          | Technology             |
| -------------- | ---------------------- |
| Frontend       | Streamlit              |
| Audio Input    | streamlit-mic-recorder |
| Speech-to-Text | SpeechRecognition      |
| Translation    | googletrans            |
| Text-to-Speech | gTTS                   |
| Backend Logic  | Python                 |

---

## 📦 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/Messaging-app.git
cd Messaging-app
```

### 2️⃣ Install dependencies

```bash
pip install streamlit streamlit-mic-recorder googletrans==4.0.0-rc1 gTTS SpeechRecognition httpx
```

### 3️⃣ Run the app

```bash
streamlit run new.py
```

---

## 📸 Demo (Add Screenshots Here)

> 💡 Tip: Add screenshots or a demo GIF here for better GitHub impact

```
/assets/demo.gif
/assets/ui-preview.png
```

---

## ⚠️ Important Notes

* Requires **active internet connection** (Google APIs used)
* Minor latency may occur during translation
* Timeout handling implemented for stability

---

## 🎯 Future Improvements

* 🔄 Replace APIs with **offline models (Whisper + IndicTrans2)**
* 🌐 Real-time streaming using WebRTC
* 💾 Database integration for message storage
* 🔐 User authentication system
* 🤖 Improved translation accuracy via fine-tuning

---

## 🤝 Contributing

Contributions are welcome!
Feel free to fork the repo and submit a pull request 🚀

---

## 📄 License

This project is licensed under the **MIT License**

---

## 👩‍💻 Author

**Anshika Sajwan**

---


