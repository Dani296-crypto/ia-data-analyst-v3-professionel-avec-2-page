import streamlit as st

st.set_page_config(page_title="Login IA", layout="centered")

st.title("🔐 Connexion")

password = st.text_input("Mot de passe", type="password")

if st.button("Se connecter"):

    if password == st.secrets["APP_PASSWORD"]:
        st.session_state["auth"] = True
        st.success("Accès autorisé")
        st.switch_page("pages/ia.py")

    else:
        st.error("Mot de passe incorrect")
