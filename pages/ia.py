import streamlit as st
import pandas as pd
from openai import OpenAI
import json
import os

# ======================
# 🔒 PROTECTION
# ======================
if not st.session_state.get("auth", False):
    st.warning("Accès refusé")
    st.stop()

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="IA Data Analyst PRO",
    layout="wide"
)

st.title("📊 IA Data Analyst PRO")

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# ======================
# MEMORY FILE
# ======================
MEMORY_FILE = "memory/chat_memory.json"

# ======================
# MEMORY FUNCTIONS
# ======================

def load_memory():

    if os.path.exists(MEMORY_FILE):

        with open(MEMORY_FILE, "r") as file:
            return json.load(file)

    return []


def save_memory(memory):

    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)

# ======================
# INIT SESSION STATE
# ======================

if "history" not in st.session_state:
    st.session_state.history = load_memory()

if "df_loaded" not in st.session_state:
    st.session_state.df_loaded = None

# ======================
# FILE UPLOAD
# ======================

file = st.file_uploader(
    "📂 Upload Excel",
    type=["xlsx"]
)

if file:

    df = pd.read_excel(file)

    st.session_state.df_loaded = df

# ======================
# SI DONNÉES DISPONIBLES
# ======================

if st.session_state.df_loaded is not None:

    df = st.session_state.df_loaded

    st.subheader("🔍 Aperçu des données")

    st.dataframe(df)

    # ======================
    # IA FUNCTION
    # ======================

    def generate_result(question):

        prompt = f"""
Tu es un data analyst expert universel.

MISSION :
Analyser un fichier Excel et répondre aux questions.

RÈGLES :
- Utilise uniquement les données fournies
- Fais les calculs directement
- Si info absente → "non disponible"

DONNÉES :
{df.to_string(index=False)}

COLONNES :
{df.columns.tolist()}

QUESTION :
{question}

RÉPONSE :
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Data analyst précis et business"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    # ======================
    # UI QUESTION
    # ======================

    st.subheader("🧠 Pose ta question")

    question = st.text_input(
        "Ex: Quel produit vend le plus ?"
    )

    # ======================
    # BOUTON ANALYSE
    # ======================

    if st.button("Analyser"):

        # Vérification question vide
        if question.strip() == "":
            st.warning("Pose une question")
            st.stop()

        # Analyse IA
        with st.spinner("Analyse en cours..."):

            result = generate_result(question)

        # ======================
        # AJOUT HISTORIQUE
        # ======================

        st.session_state.history.append({
            "question": question,
            "answer": result
        })

        # ======================
        # SAUVEGARDE JSON
        # ======================

        save_memory(st.session_state.history)

        # ======================
        # AFFICHAGE RÉSULTAT
        # ======================

        st.subheader("📌 Résultat")

        st.write(result)

    # ======================
    # HISTORIQUE
    # ======================

    if st.session_state.history:

        st.subheader("🕘 Historique")

        for chat in reversed(st.session_state.history):

            with st.container():

                st.write(
                    "🧑 Question :",
                    chat["question"]
                )

                st.write(
                    "🤖 Réponse :",
                    chat["answer"]
                )

                st.markdown("---")
