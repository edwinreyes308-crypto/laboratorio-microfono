import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Laboratorio de Micrófono", layout="centered")

st.title("🎙️ Laboratorio de Entonación")
st.write("Prueba de captura de voz con seguridad HTTPS")

# --- INTERFAZ ORIGINAL ---
idioma = st.radio("Selecciona el idioma para la prueba:", ["en-US", "es-ES"], horizontal=True)

def componente_microfono(lang):
    # HTML y JS que ya conoces, optimizado para enviar el texto correctamente
    html_code = f"""
    <div style="text-align:center;">
        <button id="btn" style="
            width:100%; height:100px; font-weight:900; 
            background-color:#FFD600; border:4px solid #000; 
            border-radius:20px; cursor:pointer; font-size:22px;
            box-shadow: 0px 6px 0px #000;
        ">MANTÉN PULSADO Y HABLA</button>
        <p id="info" style="font-family:sans-serif; font-size:14px; margin-top:10px; color:#555;">Listo</p>
    </div>

    <script>
    const btn = document.getElementById('btn');
    const info = document.getElementById('info');
    const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (Recognition) {{
        const rec = new Recognition();
        rec.lang = '{lang}';
        rec.continuous = false;
        rec.interimResults = false;

        btn.onmousedown = () => {{
            try {{
                rec.start();
                btn.style.backgroundColor = '#FF5252';
                btn.style.boxShadow = '0px 2px 0px #000';
                btn.style.transform = 'translateY(4px)';
                info.innerText = "Escuchando...";
            }} catch(e) {{ info.innerText = "Error: " + e.message; }}
        }};

        btn.onmouseup = () => {{
            rec.stop();
            btn.style.backgroundColor = '#FFD600';
            btn.style.boxShadow = '0px 6px 0px #000';
            btn.style.transform = 'translateY(0px)';
            info.innerText = "Procesando...";
        }};

        // Soporte para móviles (Motorola/Android)
        btn.ontouchstart = (e) => {{ e.preventDefault(); btn.onmousedown(); }};
        btn.ontouchend = (e) => {{ e.preventDefault(); btn.onmouseup(); }};

        rec.onresult = (event) => {{
            const result = event.results[0][0].transcript;
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: result
            }}, '*');
            info.innerText = "¡Capturado!";
        }};
    }}
    </script>
    """
    # Usamos una key estática para evitar el TypeError
    return components.html(html_code, height=180, key="laboratorio_v1")

# --- LÓGICA DE CAPTURA ---
captura = componente_microfono(idioma)

st.divider()

# Filtro para que solo muestre el texto cuando sea una cadena real
if isinstance(captura, str) and len(captura) > 0:
    st.balloons()
    st.success(f"### Palabra escuchada: **{captura}**")
    st.session_state['texto_escuchado'] = captura
else:
    st.info("El resultado aparecerá aquí abajo cuando hables.")

# El cuadro final que querías para ver la palabra escrita
st.text_input("Resultado en el sistema:", value=st.session_state.get('texto_escuchado', ""))

if st.button("Limpiar laboratorio"):
    st.session_state['texto_escuchado'] = ""
    st.rerun()
