import streamlit as st

st.set_page_config(page_title="Login")

if "auth" not in st.session_state:
    st.session_state["auth"] = False

st.title("🔐 Login")

password = st.text_input("Mot de passe", type="password")

if st.button("Se connecter"):

    if password == st.secrets["APP_PASSWORD"]:
        st.session_state["auth"] = True
        st.success("Connexion réussie ✔️")
        st.rerun()

    else:
        st.error("Mot de passe incorrect")

# 👉 aucune redirection forcée ici
if st.session_state["auth"]:
    st.info("Connexion OK ✔️ → ouvre IA dans le menu à gauche")
