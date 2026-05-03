import streamlit as st
import streamlit.components.v1 as components

# 1. Configuración inicial (Debe ser lo primero)
st.set_page_config(page_title="Laboratorio de Voz", layout="centered")

st.title("🎤 Probador de Voz Profesional")
st.write("Estado: Conexión segura HTTPS")

# 2. Selección de idioma
idioma = st.radio("Idioma:", ["en-US", "es-ES"], horizontal=True)

# 3. El componente (Simplificado al máximo para evitar el TypeError)
def mi_microfono(lang):
    html_code = f"""
    <div style="text-align:center;">
        <button id="btn" style="
            width:100%; height:80px; font-weight:bold; 
            background-color:#FFD600; border:3px solid black; 
            border-radius:15px; cursor:pointer; font-size:18px;
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

        // Soporte táctil
        btn.ontouchstart = (e) => {{ e.preventDefault(); btn.onmousedown(); }};
        btn.ontouchend = (e) => {{ e.preventDefault(); btn.onmouseup(); }};

        rec.onresult = (event) => {{
            const texto = event.results[0][0].transcript;
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: texto
            }}, '*');
            msg.innerText = "¡Enviado!";
        }};
    }}
    </script>
    """
    # Quitamos la 'key' problemática y dejamos solo lo esencial
    return components.html(html_code, height=150)

# 4. Captura y visualización (Lógica robusta)
valor_capturado = mi_microfono(idioma)

st.divider()

if valor_capturado:
    st.balloons()
    st.success(f"### ✅ Palabra detectada: {valor_capturado}")
    st.session_state["texto_voz"] = valor_capturado
else:
    st.info("La palabra aparecerá aquí después de que hables.")

# Caja de confirmación (solo texto plano)
confirmacion = st.text_input("Resultado capturado:", value=st.session_state.get("texto_voz", ""))

if st.button("Limpiar"):
    st.session_state["texto_voz"] = ""
    st.rerun()
