import streamlit as st
import speech_recognition as sr
import os

# Pour gestion d'état entre runs Streamlit
if "listening" not in st.session_state:
    st.session_state.listening = False
if "transcribed_text" not in st.session_state:
    st.session_state.transcribed_text = ""

def transcribe_speech(api_choice, language):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        st.info("🎤 Parlez maintenant...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        if api_choice == "Google":
            text = recognizer.recognize_google(audio, language=language)
        elif api_choice == "PocketSphinx":
            text = recognizer.recognize_sphinx(audio, language=language)
        else:
            text = "API inconnue."
        return text
    except sr.UnknownValueError:
        return "⚠️ Impossible de comprendre le message vocal."
    except sr.RequestError as e:
        return f"⚠️ Erreur du service de reconnaissance vocale : {e}"
    except Exception as e:
        return f"⚠️ Erreur inattendue : {e}"

def main():
    st.title("🎙️ Application de Reconnaissance Vocale Améliorée")

    # Choix API
    api_choice = st.selectbox("Choisissez l'API de reconnaissance vocale :", ["Google", "PocketSphinx"])

    # Choix langue
    language = st.selectbox(
        "Choisissez la langue parlée :",
        {
            "Français": "fr-FR",
            "Anglais": "en-US",
            "Arabe": "ar-SA",
            "Espagnol": "es-ES",
            "Allemand": "de-DE"
        }.keys()
    )
    lang_code = {
        "Français": "fr-FR",
        "Anglais": "en-US",
        "Arabe": "ar-SA",
        "Espagnol": "es-ES",
        "Allemand": "de-DE"
    }[language]

    # Boutons de contrôle
    col1, col2, col3 = st.columns(3)
    with col1:
        start = st.button("▶️ Démarrer")
    with col2:
        pause = st.button("⏸️ Pause")
    with col3:
        resume = st.button("▶️ Reprendre")

    if start:
        st.session_state.listening = True
        st.session_state.transcribed_text = ""

    if pause:
        st.session_state.listening = False
        st.info("🛑 Reconnaissance vocale mise en pause.")

    if resume:
        st.session_state.listening = True
        st.info("▶️ Reprise de la reconnaissance vocale.")

    # Reconnaissance vocale simulée en mode start + listening
    if st.session_state.listening:
        # La vraie reconnaissance est bloquante, pour simuler :
        with st.spinner("Écoute en cours..."):
            text = transcribe_speech(api_choice, lang_code)
            if text.startswith("⚠️"):
                st.error(text)
            else:
                st.success("✅ Texte reconnu !")
                st.session_state.transcribed_text += " " + text

    # Afficher la transcription courante
    st.text_area("Texte transcrit :", value=st.session_state.transcribed_text.strip(), height=200)

    # Sauvegarder la transcription dans un fichier
    if st.button("💾 Sauvegarder la transcription dans un fichier"):
        filename = "transcription.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(st.session_state.transcribed_text.strip())
        st.success(f"Transcription sauvegardée dans `{filename}`")

if __name__ == "__main__":
    main()
