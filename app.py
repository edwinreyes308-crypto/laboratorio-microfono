import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Laboratorio de Voz", layout="centered")

st.title("🎤 Prueba de Voz: Paso Final")
st.write("Estado: Conexión HTTPS segura.")

# 1. Selección de idioma
idioma = st.radio("Idioma:", ["en-US", "es-ES"], horizontal=True)

# 2. El Componente con "Notificador de Cambio"
def mi_microfono(lang):
    html_code = f"""
    <div style="text-align:center;">
        <button id="btn" style="
            width:100%; height:90px; font-weight:bold; 
            background-color:#FFD600; border:3px solid black; 
            border-radius:20px; cursor:pointer; font-size:20px;
        ">MANTÉN PULSADO Y HABLA</button>
        <p id="msg" style="font-family:sans-serif; font-size:12px; color:gray; margin-top:5px;">Listo</p>
    </div>

    <script>
    const btn = document.getElementById('btn');
    const msg = document.getElementById('msg');
    const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (Recognition) {{
        const rec = new Recognition();
        rec.lang = '{lang}';
        rec.continuous = false;
        rec.interimResults = false;
        
        btn.onmousedown = () => {{
            try {{
                rec.start();
                btn.style.background = '#FF5252';
                msg.innerText = "Escuchando...";
            }} catch(e) {{ console.log(e); }}
        }};

        btn.onmouseup = () => {{
            rec.stop();
            btn.style.background = '#FFD600';
            msg.innerText = "Enviando...";
        }};

        // Soporte para móviles
        btn.ontouchstart = (e) => {{ e.preventDefault(); btn.onmousedown(); }};
        btn.ontouchend = (e) => {{ e.preventDefault(); btn.onmouseup(); }};

        rec.onresult = (event) => {{
            const texto = event.results[0][0].transcript;
            msg.innerText = "¡Capturado!";
            
            // Enviamos el valor a Python
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: texto
            }}, '*');
        }};
    }}
    </script>
    """
    # Usamos una key dinámica basada en el idioma para forzar el refresco
    return components.html(html_code, height=160, key=f"micro_{lang}")

# --- CAPTURA ---
captura_voz = mi_microfono(idioma)

st.divider()

# TRUCO: Si la captura es un objeto DeltaGenerator, la ignoramos.
# Solo actuamos si es un String (texto).
if isinstance(captura_voz, str) and len(captura_voz) > 0:
    st.balloons()
    st.success(f"### ✅ Palabra detectada: **{captura_voz}**")
    st.session_state["texto_final"] = captura_voz
else:
    st.info("Mantén pulsado, habla claro y suelta para ver el resultado.")

# Cuadro donde aparecerá la palabra grabada
st.text_input("Texto recibido en el sistema:", value=st.session_state.get("texto_final", ""))

if st.button("Limpiar todo"):
    st.session_state["texto_final"] = ""
    st.rerun()
