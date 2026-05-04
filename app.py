import streamlit as st
import speech_recognition as sr

st.set_page_config(page_title="Laboratorio de Voz", layout="centered")

st.title("🎙️ Laboratorio de Voz: Transcripción Real")
st.write("Estado: Micrófono y Motor de Traducción conectados.")

# 1. Selección de idioma
idioma_opcion = st.radio("Idioma para capturar:", ["Español", "Inglés"], horizontal=True)
lang_code = "es-ES" if idioma_opcion == "Español" else "en-US"

st.divider()

# 2. El Micrófono (Captura la señal nítida)
audio_input = st.audio_input("Graba la palabra para convertirla a texto:")

if audio_input:
    st.audio(audio_input)
    
    # --- PROCESO DE CONVERSIÓN (El "Cerebro") ---
    r = sr.Recognizer()
    
    # Cargamos el audio capturado
    with sr.AudioFile(audio_input) as source:
        audio_data = r.record(source)
        
        try:
            # Enviamos el audio al motor de Google para convertirlo en texto
            texto_detectado = r.recognize_google(audio_data, language=lang_code)
            
            st.balloons()
            st.success(f"### ✅ Palabra detectada: **{texto_detectado}**")
            st.session_state['resultado'] = texto_detectado
            
        except sr.UnknownValueError:
            st.error("El motor no pudo entender la palabra. Intenta entonar más claro.")
        except sr.RequestError:
            st.error("Error de conexión con el motor de traducción.")

# 3. Interfaz de salida
st.divider()
st.text_input("Resultado escrito por el sistema:", value=st.session_state.get('resultado', ""))

if st.button("Limpiar laboratorio"):
    st.session_state['resultado'] = ""
    st.rerun()
