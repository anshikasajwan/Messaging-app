# Messaging-app
This app is a bimodal communication relay designed to facilitate seamless interaction between two users, even on a single device. Developed as part of a BTech project, it focuses on bridging language barriers through a structured English-to-English message exchange.
# Communicate Audio v2.0: VoIP Relay & Linguistic Data Tool 🎙️

## 📌 Project Overview
This application is a specialized **Audio Messaging System** built with Python and Streamlit. It serves two primary functions:
1. **Real-time Audio Relay**: Simulates a Voice-over-IP (VoIP) interaction between a 'Sender' and 'Receiver'.
2. **Dataset Collection**: Allows for the capture and export of raw audio bytes into `.wav` formats, supporting future research into the **multilingual translation of Indian text**.

## 🚀 Key Features
* **Bimodal Interface**: Separate tabs for Sender (Capture) and Receiver (Playback) roles.
* **Direct Browser Recording**: Integrates `streamlit-mic-recorder` for high-fidelity audio capture directly within the mobile or desktop browser.
* **Session State Memory**: Uses `st.session_state` to act as a temporary buffer, relaying audio data instantly across interfaces without a database.
* **Dataset Export**: Includes a one-click download feature to save recordings as `.wav` files for data preprocessing with **NumPy** or **Pandas**.

## 🏗️ Technical Architecture
The app follows a modular flow to handle binary audio data:
1. **Input**: Sender records audio → converted to `bytes`.
2. **Relay**: Bytes are stored in the shared `session_state` object.
3. **Output**: Receiver fetches bytes → renders a native HTML5 audio player for playback.



## 🛠️ Setup & Installation
1. Clone the repository to your Mac.
2. Install dependencies:
   ```bash
   pip install streamlit streamlit-mic-recorder