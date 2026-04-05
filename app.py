import streamlit as st
from streamlit_mic_recorder import mic_recorder
from googletrans import Translator
from gtts import gTTS
import speech_recognition as sr
import io
import datetime
import time

# --- 1. SHARED GLOBAL ENGINE (Cloud Relay) ---
@st.cache_resource
def get_global_vault():
    return {}

global_vault = get_global_vault()

# --- 2. BACKEND AI ENGINE (Corrected Logic) ---
from httpx import Timeout # Add this at the very top with your imports

def backend_process_all_langs(audio_bytes):
    iso_map = {
        "Hindi": "hi", "English": "en", "Bengali": "bn", "Malayalam": "ml",
        "Odia": "or", "Assamese": "as", "Marathi": "mr", "Tamil": "ta",
        "Gujarati": "gu", "Punjabi": "pa", "Rajasthani": "hi"
    }
    
    results = {}
    try:
        recognizer = sr.Recognizer()
        audio_file = io.BytesIO(audio_bytes)
        with sr.AudioFile(audio_file) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = recognizer.record(source)
        
        # 1. ASR (Speech to Text)
        source_text = recognizer.recognize_google(audio_data, language="en-IN")
        
        if not source_text:
            return "Error: No speech detected.", None

        # 2. Setup Translator with a longer timeout (20 seconds)
        # This prevents the "Read operation timed out" error
        translator = Translator(timeout=Timeout(20.0))
        
        for lang_name, lang_code in iso_map.items():
            try:
                # Translate Text
                translation = translator.translate(source_text, dest=lang_code)
                translated_text = str(translation.text)
                
                # Generate Audio
                tts = gTTS(text=translated_text, lang=lang_code)
                tts_buffer = io.BytesIO()
                tts.write_to_fp(tts_buffer)
                
                results[lang_name] = {
                    "transcript": translated_text,
                    "audio": tts_buffer.getvalue()
                }
                
                # 💡 Crucial: Small pause so Google doesn't time us out
                time.sleep(0.2) 
                
            except Exception as lang_err:
                print(f"Skipping {lang_name}: {lang_err}")
                continue
        
        return source_text, results
    except Exception as e:
        return f"Connection Error: {str(e)}", None

# --- 3. UI STYLING (The "Anshika" Smartphone Theme) ---
BRIGHT_STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&display=swap');
    html, body, [class*="st-"] { font-family: 'Outfit', sans-serif; }
    h1, h2, h3, p, label, .stMarkdown p { color: #000000 !important; font-weight: 800 !important; }

    .stApp {
        max-width: 340px !important; height: 720px !important; 
        margin: 10px auto !important; border: 10px solid #1e1e2e !important; 
        border-radius: 40px !important; background: #ffffff !important;
        overflow-y: auto !important; overflow-x: hidden !important;
    }

    .stButton>button {
        border-radius: 25px !important;
        background: linear-gradient(45deg, #00AD5F, #00FF95) !important;
        color: white !important; font-weight: 700 !important; border: none !important;
    }
    
    .mobile-status-bar {
        position: absolute; top: -35px; right: 10px; z-index: 10000;
        font-size: 11px; font-weight: 900; color: #000;
    }
    .header-box { margin-top: 5px; display: flex; justify-content: space-between; align-items: center; width: 100%; }
    header, footer { visibility: hidden; }
</style>
"""

st.set_page_config(page_title="Indian lingual", layout="centered")
st.markdown(BRIGHT_STYLE, unsafe_allow_html=True)

# --- 4. RENDER STATUS BAR & HEADER ---
st.markdown(f'<div class="mobile-status-bar">{datetime.datetime.now().strftime("%I:%M %p")} 📶 🔋 100%</div>', unsafe_allow_html=True)

st.markdown('<div class="header-box">', unsafe_allow_html=True)
col_text, col_img = st.columns([3, 1])
with col_text:
    st.markdown("<h2 style='color:#000; margin:0; line-height:1.1;'>SWAR<br>CONNECT</h2>", unsafe_allow_html=True)
with col_img:
    st.image("WhatsApp Image 2026-04-02 at 23.41.07.jpeg", width=80)
st.markdown('</div>', unsafe_allow_html=True)

tab_send, tab_receive = st.tabs(["🚀 SEND", "📥 RECEIVE"])

# ---------------------------------------------------------
# TAB 1: SENDER (FIXED CALL NAME)
# ---------------------------------------------------------
with tab_send:
    st.image("https://img.icons8.com/fluency/96/rocket.png", width=60)
    target_user = st.text_input("RECEIVER'S ID:", placeholder="e.g. User_2")
    
    with st.container(border=True):
        st.write("🎙️ **RECORDING BOOTH**")
        audio = mic_recorder(start_prompt="⏺️ RECORD", stop_prompt="⏹️ STOP", key='v60_mic', format="wav")
        
        if audio:
            st.audio(audio['bytes'])
            if st.button("🚀 BLAST MESSAGE!", use_container_width=True):
                if target_user:
                    with st.spinner("Backend AI Translating..."):
                        # SYNCED NAME: backend_process_all_langs
                        orig_text, translations = backend_process_all_langs(audio['bytes'])
                        
                        if translations:
                            global_vault[target_user.strip()] = {
                                "original_audio": audio['bytes'],
                                "original_text": orig_text,
                                "translations": translations,
                                "sender": "Anshika",
                                "time": datetime.datetime.now().strftime("%I:%M %p")
                            }
                            st.balloons() 
                            st.toast("Transmission Verified! 🎈")
                        else:
                            st.error(orig_text)
                else:
                    st.error("Missing Target ID!")

# ---------------------------------------------------------
# TAB 2: RECEIVER (Instant Translation)
# ---------------------------------------------------------
with tab_receive:
    st.image("https://img.icons8.com/fluency/96/mailbox-closed-flag-up.png", width=60)
    my_id = st.text_input("MY ACCOUNT ID:", placeholder="e.g. User_2")
    
    lang_list = ["Hindi", "English", "Bengali", "Malayalam", "Odia", "Assamese", "Marathi", "Tamil", "Gujarati", "Punjabi", "Rajasthani"]
    chosen_lang = st.selectbox("PREFERED LANGUAGE:", lang_list)
    
    msg = global_vault.get(my_id.strip())

    if msg:
        with st.container(border=True):
            st.write(f"📥 **FROM: {msg['sender']}**")
            
            # Retrieve the pre-translated data from the vault
            lang_data = msg['translations'].get(chosen_lang)
            
            if lang_data:
                st.write(f"🗣️ **Translated Voice ({chosen_lang}):**")
                st.audio(lang_data['audio'])
                
                # Visual Transcript Card
                st.markdown(f"""
                    <div style="background:#f0fff4; border-left:6px solid #00AD5F; padding:12px; border-radius:10px; margin-top:10px;">
                        <p style="color:#666; font-size:11px; margin:0;">Input: "{msg['original_text']}"</p>
                        <p style="color:#000; font-size:15px; margin:5px 0;"><b>{chosen_lang}: "{lang_data['transcript']}"</b></p>
                    </div>
                """, unsafe_allow_html=True)

        if st.button("🗑️ CLEAR INBOX", use_container_width=True):
            global_vault.pop(my_id.strip(), None)
            st.rerun()
    else:
        st.info("📡 SCANNING NETWORK...")
        time.sleep(4)
        st.rerun()
