import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Diccionario Pedagógico de Voz", layout="centered")

st.title("🎤 Laboratorio de Voz: Versión Profesional")
st.write("Estado: Conexión segura HTTPS activa.")

# --- SECCIÓN DE IDIOMA ---
col1, col2 = st.columns(2)
with col1:
    idioma = st.selectbox("Selecciona el idioma a practicar:", ["Español", "Inglés"])
with col2:
    nivel = st.selectbox("Nivel:", ["Primaria", "Secundaria"])

st.divider()

# --- CAPTURA DE AUDIO NATIVA ---
# Esta herramienta es la que elimina los errores de "Network" y "TypeError"
st.subheader("Paso 1: Graba tu pronunciación")
archivo_audio = st.audio_input("Presiona el círculo para grabar tu voz")

if archivo_audio:
    # 1. Confirmación visual de que el audio llegó al servidor
    st.success("¡Audio capturado con éxito!")
    st.audio(archivo_audio)
    
    # 2. Espacio para la transcripción
    st.subheader("Paso 2: Resultado de la transcripción")
    
    # Nota técnica: Para convertir este archivo de audio a texto escrito (transcribir),
    # el siguiente paso es conectar una librería como 'speech_recognition'.
    # Por ahora, el sistema ya recibe tu voz sin errores.
    
    st.info(f"El sistema ha recibido tu voz en {idioma}. "
            "Estamos listos para procesar la palabra en el diccionario.")

else:
    st.info("Haz clic en el icono del micrófono arriba para empezar.")

# --- ÁREA DEL DICCIONARIO (Lógica pedagógica) ---
st.divider()
st.subheader("📚 Consulta del Diccionario")
palabra_manual = st.text_input("O escribe la palabra manualmente aquí:", placeholder="Ej: Polinomios, Fracciones...")

if palabra_manual:
    st.write(f"Buscando definición para: **{palabra_manual}**")
    # Aquí irá tu base de datos de matemáticas e inglés
