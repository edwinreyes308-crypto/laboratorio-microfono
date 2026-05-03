import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Laboratorio Web de Voz", page_icon="🎤")

st.title("🎤 Prueba de Voz: Conexión Final")
st.write("Estado: Conexión segura HTTPS activa.")

idioma = st.radio("Selecciona idioma:", ["en-US", "es-ES"], horizontal=True)

def mic_componente(lang):
    # JavaScript con envío forzado de datos
    js_code = f"""
    <div style="text-align:center;">
        <button id="btn" style="
            width:100%; height:90px; font-weight:900; 
            background-color:#FFD600; border:4px solid #000; 
            border-radius:20px; cursor:pointer; font-size:20px;
        ">MANTÉN PULSADO Y HABLA</button>
        <p id="info" style="font-family:sans-serif; font-size:14px; margin-top:10px; color:blue;">Listo</p>
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
            rec.start();
            btn.style.backgroundColor = '#FF5252';
            info.innerText = "Escuchando...";
        }};

        btn.onmouseup = () => {{
            rec.stop();
            btn.style.backgroundColor = '#FFD600';
            info.innerText = "Enviando datos...";
        }};

        rec.onresult = (event) => {{
            const result = event.results[0][0].transcript;
            info.innerText = "¡Enviado!";
            
            // EL TRUCO: Enviamos el valor y notificamos a Streamlit que hubo un cambio
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: result
            }}, '*');
        }};
        
        rec.onerror = (e) => {{ info.innerText = "Error: " + e.error; }};
    }}
    </script>
    """
    # Usamos una key única para que Streamlit refresque el componente
    return components.html(js_code, height=170, key="micro_web")

# Captura del resultado
resultado = mic_componente(idioma)

st.markdown("---")

# Lógica de visualización inmediata
if resultado:
    st.balloons()
    st.success(f"### ✅ Se detectó la palabra: **{resultado}**")
    st.session_state['voz_capturada'] = resultado
else:
    st.info("Mantén presionado el botón, habla claro y suéltalo para ver el resultado.")

# Caja de confirmación
st.text_input("Texto recibido en Python:", value=st.session_state.get('voz_capturada', ""))   
