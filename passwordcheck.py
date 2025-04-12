import streamlit as st
import re

st.title("Password Check")
st.markdown("---")
st.write("Enter Your Password")
password = st.text_input("Password", type="password")
st.markdown("---")

def check_password(password):
    score = 0
    error = []
    
    if len(password) < 8:
        error.append("Password must be at least 8 characters long (12+ recommended)")
    elif len(password) >= 12:
        score += 1
    
    has_upper = re.search("[A-Z]", password)
    has_lower = re.search("[a-z]", password)
    if has_upper and has_lower:
        score += 1
    else:
        error.append("Password must contain both upper and lower case letters")
    
    if re.search(r"\d", password):
        score += 1
    else:
        error.append("Password must contain at least one number")
    
    if re.search(r"[!@#$%^&()?*]", password):
        score += 1
    else:
        error.append("Password must contain at least one special character")
    
    common_passwords = ["password", "123456", "qwerty"]
    if password.lower() in common_passwords:
        score = 0
        error.append("Password is too common")
    
    if re.search(r"(.)\1{2,}", password):
        score -= 1
        error.append("Avoid repeating characters")
    
    if score >= 5:
        strength = "Excellent"
    elif score >= 4:
        strength = "Strong"
    elif score >= 3:
        strength = "Moderate"
    elif score >= 2:
        strength = "Weak"
    else:
        strength = "Very Weak"
    
    return score, error, strength

if password:
    score, error, strength = check_password(password)
    st.write(f"Password Strength: {strength}")
    
    cols = st.columns(5)
    colors = ["#FF0000", "#FFA500", "#FFFF00", "#00FF00", "#0000FF"]
    
    for i in range(5):
        with cols[i]:
            st.color_picker(label="", value=colors[i] if i < score else "#808080", key=f"color_{i}", disabled=True)
    
    st.subheader(f"Strength: {strength}")
    st.progress(min(score/5, 1.0))
    
    if error:
        st.subheader("Improvements needed:")
        for item in error:
            st.error(item)