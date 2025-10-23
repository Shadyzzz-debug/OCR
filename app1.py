import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image

# --- 1. Configuración de la Página y Estilo Gótico (CSS Injection) ---
st.set_page_config(
    page_title="El Rastreador de Runas",
    page_icon="👁️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Paleta Gótica (Estilo Bloodborne):
# Fondo: #0A0A0A (Negro profundo)
# Texto Principal: #F5F5DC (Hueso/Papiro)
# Acento/Sangre: #8B0000 (Rojo intenso)
# Metal/Piedra: #6B5B3E (Bronce oscuro/Caoba)

gothic_css = """
<style>
/* Fondo general y fuente serif dramática */
body {
    background-color: #0A0A0A;
    color: #F5F5DC;
    font-family: 'Georgia', serif;
}
.stApp {
    background-color: #0A0A0A;
    color: #F5F5DC;
}

/* Título Principal: Cincelado y Dramático */
h1 {
    color: #8B0000; /* Rojo sangre */
    text-shadow: 2px 2px 5px #000000;
    font-size: 2.8em;
    border-bottom: 5px double #6B5B3E; /* Borde doble color bronce */
    padding-bottom: 10px;
    margin-bottom: 30px;
    text-align: center;
    letter-spacing: 2px;
}

/* Subtítulos: Menos prominentes, color de metal */
h2, h3 {
    color: #D4D4D4;
    font-family: 'Georgia', serif;
}

/* Sidebar: Fondo de cámara oscura con bordes intrincados */
[data-testid="stSidebar"] {
    background-color: #1A1A1A;
    color: #F5F5DC;
    border-right: 3px solid #6B5B3E;
    box-shadow: 0 0 15px rgba(107, 91, 62, 0.5), inset 0 0 5px rgba(0, 0, 0, 0.8);
}

/* Elementos de entrada (Runas): Fondo oscuro, borde metálico */
.stTextInput > div > div > input, .stTextArea > div > textarea, .stSelectbox > div > div {
    background-color: #1A1A1A;
    color: #F5F5DC;
    border: 2px solid #6B5B3E;
    border-radius: 4px;
    box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.5);
}

/* Botones genéricos (no aplicables directamente al OCR, pero mantenidos por si acaso) */
.stButton > button {
    background-color: #444444; /* Base metálica */
    color: #F5F5DC;
    border: 3px solid #8B0000; /* Borde rojo sangre */
    border-radius: 8px;
    padding: 12px 25px;
    font-weight: bold;
    box-shadow: 6px 6px 10px #000000, inset 0 0 10px rgba(255, 255, 255, 0.1);
    transition: background-color 0.3s, box-shadow 0.3s, transform 0.1s;
}

.stButton > button:hover {
    background-color: #8B0000; /* Hover a rojo intenso */
    color: white;
    box-shadow: 8px 8px 15px #000000;
    transform: translateY(-2px);
}

/* Estilo para las alertas de Streamlit */
.stAlert {
    background-color: #1A1A1A !important;
    border: 2px solid #8B0000 !important;
    color: #F5F5DC !important;
}

</style>
"""
st.markdown(gothic_css, unsafe_allow_html=True)

st.title("El Rastreador de Runas")
st.subheader("Invoca la Visión Ocular para Leer el Olvido")

# --- 2. Imagen Gótica (Placeholder de un Sello) ---
image_url = "https://placehold.co/650x250/1A1A1A/6B5B3E?text=Sello+de+la+Revelación+Prohibida"
st.image(image_url, caption="Una visión que corta la oscuridad.", use_column_width=True)

# --- 3. Sidebar y Protocolo de Visión ---
with st.sidebar:
    st.subheader("Protocolo de la Visión")
    st.write(
        "Utiliza la cámara para capturar el texto. El Oráculo descifrará las Runas ocultas. "
        "Elige el **Ritual de Inversión** para textos difíciles."
    )
    st.markdown("---")
    
    # Filtro con nombres góticos
    filtro = st.radio("Ritual de Inversión (Filtro)",
        ('Con el Ritual (Invertir)', 'Sin el Ritual (Normal)'))

# --- 4. Funcionalidad de OCR ---

img_file_buffer = st.camera_input("👁️ Ojo de la Revelación: Captura el Sello Prohibido")


if img_file_buffer is not None:
    st.markdown("---")
    # Para leer el buffer de la imagen con OpenCV:
    bytes_data = img_file_buffer.getvalue()
    
    # Manejo de errores de CV2/Numpy
    try:
        np_arr = np.frombuffer(bytes_data, np.uint8)
        cv2_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        if cv2_img is None:
            st.error("Error al decodificar la imagen. Asegúrate de que el archivo es válido.")
        else:
            # Aplicar filtro de inversión (bitwise_not)
            if filtro == 'Con el Ritual (Invertir)':
                cv2_img = cv2.bitwise_not(cv2_img)
            
            # Convertir a RGB para Tesseract
            img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
            
            # Reconocimiento de texto
            with st.spinner('Descifrando las Runas en el éter...'):
                text = pytesseract.image_to_string(img_rgb)
            
            st.markdown(f"## 📜 Manuscrito Descifrado:")
            
            if text.strip():
                st.info(text)
            else:
                st.warning("El Oráculo no pudo discernir Runas claras en la imagen.")
            
    except Exception as e:
        st.error(f"Un fallo ocurrió durante el ritual de la Visión: {e}")


    


