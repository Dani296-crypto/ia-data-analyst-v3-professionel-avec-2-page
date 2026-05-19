import streamlit as st

st.set_page_config(page_title="Login")

st.title("🔐 Login")

if "auth" not in st.session_state:
    st.session_state["auth"] = False

password = st.text_input("Mot de passe", type="password")

if st.button("Se connecter"):

    if password == st.secrets["APP_PASSWORD"]:
        st.session_state["auth"] = True
        st.success("Accès autorisé")

    else:
        st.error("Mot de passe incorrect")

# 👉 IMPORTANT : redirection logique
if st.session_state["auth"]:
    st.switch_page("pages/ia")
