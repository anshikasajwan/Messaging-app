import streamlit as st
from streamlit_mic_recorder import mic_recorder
import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Communicate Pro v3", layout="centered")

# --- DATABASE SIMULATION ---
if "message_vault" not in st.session_state:
    st.session_state.message_vault = {} 
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None
if "user_lang" not in st.session_state:
    st.session_state.user_lang = "English" # Default Language
if "current_view" not in st.session_state:
    st.session_state.current_view = "login"

# --- 1. LOGIN INTERFACE ---
if st.session_state.current_view == "login":
    st.title("🎙️ Communicate Audio")
    name_input = st.text_input("Please enter your full name:")
    
    # Pre-setting the language selection for the Sender/Receiver
    selected_lang = st.selectbox("Select your preferred language:", ["English"])
    
    if st.button("Enter System"):
        if name_input:
            st.session_state.logged_in_user = name_input.strip()
            st.session_state.user_lang = selected_lang
            st.session_state.current_view = "dashboard"
            if st.session_state.logged_in_user not in st.session_state.message_vault:
                st.session_state.message_vault[st.session_state.logged_in_user] = None
            st.rerun()

# --- 2. PERSONALIZED DASHBOARD ---
elif st.session_state.current_view == "dashboard":
    user = st.session_state.logged_in_user
    lang = st.session_state.user_lang
    st.title(f"👋 Hello, {user}!")
    st.write(f"Your Language: **{lang}**")
    
    incoming = st.session_state.message_vault.get(user)
    if incoming:
        st.warning(f"🔔 Notification: 1 unheard message from {incoming['sender']} (Language: {incoming['lang']})")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📤 Send a Message", use_container_width=True):
            st.session_state.current_view = "sender"
            st.rerun()
    with col2:
        if st.button("📥 Receive Messages", use_container_width=True):
            st.session_state.current_view = "receiver"
            st.rerun()
            
    if st.button("Logout", type="primary"):
        st.session_state.logged_in_user = None
        st.session_state.current_view = "login"
        st.rerun()

# --- 3. SENDER INTERFACE ---
elif st.session_state.current_view == "sender":
    st.header("📤 Outgoing Message")
    recipient = st.text_input("Enter Recipient Name:")
    
    # Metadata for the message
    st.write(f"Source Language: **{st.session_state.user_lang}**")
    
    audio_data = mic_recorder(start_prompt="Record", stop_prompt="Stop & Preview", key='send_rec')
    
    if audio_data:
        st.audio(audio_data['bytes'])
        if recipient and st.button("Confirm & Send"):
            st.session_state.message_vault[recipient] = {
                "bytes": audio_data["bytes"],
                "sender": st.session_state.logged_in_user,
                "lang": st.session_state.user_lang, # Attaching language data
                "time": datetime.datetime.now().strftime("%H:%M")
            }
            st.success(f"Sent to {recipient}!")
            
    if st.button("⬅️ Back"):
        st.session_state.current_view = "dashboard"
        st.rerun()

# --- 4. RECEIVER INTERFACE ---
elif st.session_state.current_view == "receiver":
    st.header(f"📥 {st.session_state.logged_in_user}'s Inbox")
    
    # NEW: Receiver sets their listening preference
    st.subheader("Listening Settings")
    listen_lang = st.selectbox(
        "I want to listen to my messages in:", 
        ["English", "Hindi", "Marathi", "Tamil"], 
        key="receiver_lang_pref"
    )
    
    st.divider()

    msg = st.session_state.message_vault.get(st.session_state.logged_in_user)
    
    if msg:
        st.write(f"📩 **New Message from {msg['sender']}**")
        st.write(f"Original Language: **{msg['lang']}**")
        st.write(f"Target Playback: **{listen_lang}**")
        
        # LOGIC: If languages don't match, we show a "Translation Needed" indicator
        if msg['lang'] != listen_lang:
            st.warning(f"🔄 Translation Required: {msg['lang']} ➔ {listen_lang}")
            st.info("System Note: In Phase 2, the NMT model will process this audio.")
        
        st.audio(msg['bytes'])
        
        if st.button("Mark as Heard & Delete", type="primary"):
            st.session_state.message_vault[st.session_state.logged_in_user] = None
            st.rerun()
    else:
        st.info("Your inbox is empty.")
        
    if st.button("⬅️ Back to Dashboard"):
        st.session_state.current_view = "dashboard"
        st.rerun()