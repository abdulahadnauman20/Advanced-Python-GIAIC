import streamlit as st
import hashlib
from cryptography.fernet import Fernet
import json
import os
from datetime import datetime, timedelta
import time

def load_or_generate_key():
    KEY_FILE = "encryption_key.key"
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as key_file:
            key_file.write(key)
        return key

KEY = load_or_generate_key()  
cipher = Fernet(KEY)

# Data Persistence
def load_data():
    DATA_FILE = "storeddata.json"
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as data_file:
                return json.load(data_file)
    except (json.JSONDecodeError, IOError):
        return {}
    return {}

def save_data(data):
    DATA_FILE = "storeddata.json"
    with open(DATA_FILE, 'w') as data_file:
        json.dump(data, data_file)

stored_data = load_data()

def hash_passkey(passkey):
    salt = os.urandom(16).hex()  
    hashed = hashlib.pbkdf2_hmac('sha256', passkey.encode(), salt.encode(), 100000)
    return f"{salt}${hashed.hex()}"

def verify_passkey(passkey, stored_hash):
    try: 
        salt, hashed_value = stored_hash.split('$')
        new_hash = hashlib.pbkdf2_hmac('sha256', passkey.encode(), salt.encode(), 100000).hex()
        return new_hash == hashed_value
    except ValueError:
        return False

def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

def decrypt_data(encrypted_text):
    return cipher.decrypt(encrypted_text.encode()).decode()

if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0
if 'lockout_until' not in st.session_state:
    st.session_state.lockout_until = None

st.set_page_config(page_title="Secure Data Encryption System", layout="wide")

st.markdown("""
    <style>
    .main {padding: 2rem;}
    .sidebar .sidebar-content {padding: 1rem;}
    .stTextArea textarea {min-height: 150px;}
    .stAlert {border-left: 4px solid #ff4b4b;}
    .stSuccess {border-left: 4px solid #00cc00;}
    </style>
    """, unsafe_allow_html=True)

menu = ["Home", "Store Data", "Retrieve Data", "Login", "Data Management"]
choice = st.sidebar.selectbox("Navigation", menu)

st.sidebar.markdown("---")
st.sidebar.subheader("System Status")
st.sidebar.write(f"Stored entries: {len(stored_data)}")
st.sidebar.write(f"Failed attempts: {st.session_state.failed_attempts}/3")

if st.session_state.lockout_until and datetime.now() < st.session_state.lockout_until:
    remaining = (st.session_state.lockout_until - datetime.now()).seconds
    st.sidebar.error(f"🔒 Locked for {remaining//60}m {remaining%60}s")
else:
    st.sidebar.success("🟢 System ready")

if choice == "Home":
    st.title(" Secure Data Encryption System")
    st.subheader(" Welcome to the Secure Data System")
    st.write("""
    Use this app to securely store and retrieve data using unique passkeys.
    
    ### Features:
    - AES-128
    - Secure passkey hashing with PBKDF2
    - Account lockout after multiple failed attempts
    - Data persistence across sessions
    
    ### How to use:
    1. Store Data: Enter your sensitive data and a strong passkey
    2. Retrieve Data: Provide your encrypted data and passkey
    3. Security: After 3 failed attempts, you'll be locked out for 5 minutes
    """)

elif choice == "Store Data":
    st.title(" Store Data Securely")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("New Entry")
        user_id = st.text_input("Unique Identifier (username/email):")
        user_data = st.text_area("Data to Encrypt:")
        
    with col2:
        st.subheader("Security")
        passkey = st.text_input("Passkey:", type="password", help="Minimum 8 characters")
        passkey_confirm = st.text_input("Confirm Passkey:", type="password")
        show_strength = st.checkbox("Show passkey strength")
        
        if show_strength and passkey:
            strength = 0
            if len(passkey) >= 8: strength += 1
            if any(c.isupper() for c in passkey): strength += 1
            if any(c.isdigit() for c in passkey): strength += 1
            if any(not c.isalnum() for c in passkey): strength += 1
            
            strength_labels = {
                0: ("Very Weak", "warning"),
                1: ("Weak", "error"),
                2: ("Moderate", "warning"),
                3: ("Strong", "info"),
                4: ("Very Strong", "success")
            }
            label, method = strength_labels.get(strength, ("Unknown", "info"))
            getattr(st, method)(label)

    if st.button("Encrypt & Save"):
        if not all([user_id, user_data, passkey, passkey_confirm]):
            st.error("All fields are required!")
        elif passkey != passkey_confirm:
            st.error("Passkeys do not match!")
        elif len(passkey) < 8:
            st.error("Passkey must be at least 8 characters!")
        else:
            hashed_passkey = hash_passkey(passkey)
            encrypted_text = encrypt_data(user_data)
            
            stored_data[user_id] = {
                "encrypted_text": encrypted_text,
                "passkey": hashed_passkey,
                "timestamp": datetime.now().isoformat()
            }
            
            save_data(stored_data)
            st.success("Data stored securely!")
            with st.expander("View Encrypted Data"):
                st.code(encrypted_text)

elif choice == "Retrieve Data":
    st.title(" Retrieve Your Data")
    
    if st.session_state.lockout_until and datetime.now() < st.session_state.lockout_until:
        remaining = (st.session_state.lockout_until - datetime.now()).seconds
        st.error(f"Account locked! Please try again in {remaining//60}m {remaining%60}s")
        st.stop()
    
    user_id = st.text_input("Enter your unique identifier:")
    passkey = st.text_input("Enter your passkey:", type="password")
    
    if st.button("Decrypt Data"):
        if not user_id or not passkey:
            st.error("Both fields are required!")
        elif user_id not in stored_data:
            st.error("Identifier not found!")
        else:
            data = stored_data[user_id]
            
            if verify_passkey(passkey, data["passkey"]):
                try:
                    decrypted_text = decrypt_data(data["encrypted_text"])
                    st.session_state.failed_attempts = 0
                    
                    st.success("Data decrypted successfully!")
                    st.text_area("Decrypted Data:", value=decrypted_text, height=200)
                    
                    with st.expander("View Details"):
                        st.json({
                            "Identifier": user_id,
                            "Storage Time": data["timestamp"],
                            "Retrieval Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                except Exception as e:
                    st.error(f"Decryption failed: {str(e)}")
            else:
                st.session_state.failed_attempts += 1
                remaining_attempts = 3 - st.session_state.failed_attempts
                
                if remaining_attempts > 0:
                    st.error(f"Incorrect passkey! Attempts remaining: {remaining_attempts}")
                else:
                    st.session_state.lockout_until = datetime.now() + timedelta(minutes=5)
                    st.error("Too many failed attempts! Account locked for 5 minutes.")
                    time.sleep(1)
                    st.experimental_rerun()

elif choice == "Login":
    st.title("🔑 Reauthorization Required")
    
    if st.session_state.lockout_until and datetime.now() < st.session_state.lockout_until:
        remaining = (st.session_state.lockout_until - datetime.now()).seconds
        st.error(f"Account locked! Please try again in {remaining//60}m {remaining%60}s")
        st.stop()
    
    login_pass = st.text_input("Enter Master Password:", type="password")
    
    if st.button("Login"):
        if login_pass == "admin123": 
            st.session_state.failed_attempts = 0
            st.session_state.lockout_until = None
            st.success("Reauthorized successfully! Redirecting...")
            time.sleep(1)
            st.rerun()
        else:
            st.session_state.failed_attempts += 1
            remaining_attempts = 3 - st.session_state.failed_attempts
            
            if remaining_attempts > 0:
                st.error(f"Incorrect password! Attempts remaining: {remaining_attempts}")
            else:
                st.session_state.lockout_until = datetime.now() + timedelta(minutes=5)
                st.error("Too many failed attempts! Account locked for 5 minutes.")
                time.sleep(1)
                st.experimental_rerun()

elif choice == "Data Management":
    st.title("📊 Data Management")
    
    if not stored_data:
        st.info("No data stored yet")
    else:
        st.write(f"Total entries: {len(stored_data)}")
        
        with st.expander("View All Entries (Metadata Only)"):
            for user_id, data in stored_data.items():
                st.write(f"**{user_id}** - Stored on {data['timestamp']}")
        
        st.subheader("Entry Operations")
        selected_id = st.selectbox("Select entry to manage:", list(stored_data.keys()))
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("View Entry Details"):
                st.json(stored_data[selected_id])
        
        with col2:
            if st.button("Delete Entry"):
                del stored_data[selected_id]
                save_data(stored_data)
                st.success("Entry deleted!")
                time.sleep(1)
                st.experimental_rerun()