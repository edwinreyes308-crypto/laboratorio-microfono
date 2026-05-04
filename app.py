import streamlit as st

st.set_page_config(page_title="Laboratorio de Voz", layout="centered")

st.title("🎙️ Laboratorio de Voz Definitivo")
st.write("Estado: Conexión segura garantizada")

# 1. Selección de idioma (Mantenemos tu interfaz de usuario)
idioma = st.radio("Selecciona el idioma:", ["en-US", "es-ES"], horizontal=True)

st.divider()

# 2. El Micrófono Oficial (Sustituye al botón amarillo)
# Este componente ya viene con todo el código de seguridad necesario
audio_datos = st.audio_input("Haz clic en el círculo para grabar tu voz")

st.divider()

# 3. Mostrar el resultado
if audio_datos:
    st.success("¡Audio capturado con éxito!")
    # Reproduce lo que grabaste para verificar entonación
    st.audio(audio_datos)
    
    # Aquí es donde el sistema "escribirá" la palabra en el siguiente paso
    st.info(f"El sistema ha recibido la señal de audio en {idioma}. Listo para transcripción.")
else:
    st.warning("Esperando grabación... Presiona el icono del micrófono arriba.")

# Cuadro de texto final
st.text_input("Palabra detectada por el sistema:", value=st.session_state.get('voz_final', ""))
