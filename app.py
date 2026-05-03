import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Laboratorio de Voz", layout="centered")

st.title("🎤 ¡Conexión Exitosa!")
st.write("Estado: Micrófono habilitado y seguro.")

idioma = st.radio("Idioma:", ["en-US", "es-ES"], horizontal=True)

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
        
        btn.onmousedown = () => {{
            rec.start();
            btn.style.background = '#FF5252';
            msg.innerText = "Escuchando...";
        }};

        btn.onmouseup = () => {{
            rec.stop();
            btn.style.background = '#FFD600';
            msg.innerText = "Enviando...";
        }};

        btn.ontouchstart = (e) => {{ e.preventDefault(); btn.onmousedown(); }};
        btn.ontouchend = (e) => {{ e.preventDefault(); btn.onmouseup(); }};

        rec.onresult = (event) => {{
            const texto = event.results[0][0].transcript;
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: texto
            }}, '*');
            msg.innerText = "¡Capturado!";
        }};
    }}
    </script>
    """
    return components.html(html_code, height=160)

# --- CAPTURA CON FILTRO ---
captura_cruda = mi_microfono(idioma)

st.divider()

# Este es el FILTRO que elimina el error de DeltaGenerator
if isinstance(captura_cruda, str) and len(captura_cruda) > 0:
    st.balloons()
    st.success(f"### ✅ Palabra detectada: {captura_cruda}")
    st.session_state["ultima_voz"] = captura_cruda
else:
    # Si lo que recibe no es texto (como el DeltaGenerator), lo ignoramos visualmente
    st.info("Esperando tu voz... (Mantén pulsado el botón amarillo)")

# Mostramos el resultado limpio
resultado_final = st.text_input("Confirmación de texto:", value=st.session_state.get("ultima_voz", ""))

if st.button("Limpiar"):
    st.session_state["ultima_voz"] = ""
    st.rerun()
