
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Laboratorio Web de Voz", page_icon="🎤")

st.title("🎤 Laboratorio de Voz: ¡Conexión Exitosa!")
st.write("Esta versión tiene seguridad HTTPS activa.")

# Selector de idioma
idioma = st.radio("Idioma para la prueba:", ["en-US", "es-ES"], horizontal=True)

def mic_web_cloud(lang):
    # JavaScript optimizado para Streamlit Cloud
    js_code = f"""
    <div style="text-align:center;">
        <button id="btn" style="
            width:100%; height:100px; font-weight:900; 
            background-color:#FFD600; border:4px solid #000; 
            border-radius:20px; cursor:pointer; font-size:22px;
            box-shadow: 0px 5px 0px #000;
        ">MANTÉN PULSADO Y HABLA</button>
        <p id="info" style="font-family:sans-serif; font-size:14px; margin-top:10px; color:#555;">Listo</p>
    </div>

    <script>
    const btn = document.getElementById('btn');
    const info = document.getElementById('info');
    const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!Recognition) {{
        info.innerText = "Error: Navegador no compatible";
    }} else {{
        const rec = new Recognition();
        rec.lang = '{lang}';
        rec.continuous = false;
        rec.interimResults = false;

        btn.onmousedown = () => {{
            try {{
                rec.start();
                btn.style.backgroundColor = '#FF5252';
                btn.innerText = '🔴 ESCUCHANDO...';
                info.innerText = "Suelte el botón al terminar de hablar";
            }} catch(e) {{ info.innerText = "Error: " + e.message; }}
        }};

        btn.onmouseup = () => {{
            rec.stop();
            btn.style.backgroundColor = '#FFD600';
            btn.innerText = 'MANTÉN PULSADO Y HABLA';
            info.innerText = "Procesando audio...";
        }};

        // Soporte para móviles
        btn.ontouchstart = (e) => {{ e.preventDefault(); btn.onmousedown(); }};
        btn.ontouchend = (e) => {{ e.preventDefault(); btn.onmouseup(); }};

        rec.onresult = (event) => {{
            const result = event.results[0][0].transcript;
            info.innerText = "¡Capturado!";
            // Enviamos el resultado a Streamlit
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: result
            }}, '*');
        }};

        rec.onerror = (e) => {{
            info.innerText = "Error: " + e.error;
            btn.style.backgroundColor = '#FFD600';
            btn.innerText = 'MANTÉN PULSADO Y HABLA';
        }};
    }}
    </script>
    """
    return components.html(js_code, height=180)

# --- CAPTURA DE RESULTADO ---

# Llamamos al componente y guardamos el resultado
resultado_voz = mic_web_cloud(idioma)

st.markdown("---")

# Usamos un contenedor vacío para que el resultado aparezca de inmediato
placeholder = st.empty()

if isinstance(resultado_voz, str) and resultado_voz.strip() != "":
    # Mostramos globos para celebrar que funcionó
    st.balloons()
    placeholder.success(f"### 🎯 Dijiste: **{resultado_voz}**")
    st.session_state['ultima_palabra'] = resultado_voz
else:
    placeholder.info("La palabra aparecerá aquí en cuanto termines de hablar.")

# Cuadro de confirmación
st.text_input("Palabra capturada por el sistema:", value=st.session_state.get('ultima_palabra', ""))

if st.button("Limpiar pantalla"):
    st.session_state['ultima_palabra'] = ""
    st.rerun()
¿Por qué se quedaba en "Procesando"?
En la web, a veces el componente HTML envía la palabra pero Streamlit no se entera de que tiene que volver a dibujar la pantalla. En este nuevo código:

He simplificado la lógica de envío.

He añadido un st.empty() que ayuda a que el mensaje de éxito aparezca con más fuerza.

He añadido st.balloons() para que, en cuanto el servidor reciba la palabra, veas globos volando en tu pantalla. ¡Será la señal de victoria!

Prueba esto:
Actualiza el archivo en GitHub, espera a que Streamlit Cloud diga que terminó de cargar (el círculo de abajo a la derecha dejará de girar) y haz la prueba.

Si hablas fuerte y claro, y el navegador ya te dio permiso, ¡deberías ver los globos y tu palabra en negrita! Cuéntame si por fin lograste ver el resultado.
