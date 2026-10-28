import base64
import os
import random
import time
import pandas as pd
import streamlit as st

# 1. Configuración de página DEBE SER el primer comando de Streamlit
st.set_page_config(page_title="Krautrock Roulette Studio", layout="centered")

# ==============================================================================
# FUNCIONES AUXILIARES PARA CARGAR ARCHIVOS LOCALES EN BASE64
# ==============================================================================
def obtener_base64_archivo(ruta_archivo):
    """Convierte cualquier archivo local a cadena Base64."""
    with open(ruta_archivo, "rb") as f:
        datos = f.read()
    return base64.b64encode(datos).decode()

# ==============================================================================
# CARGA DE RECURSOS LOCALES (IMÁGENES Y FUENTES)
# ==============================================================================

# 1. Fondo de la Pantalla Principal
ruta_fondo_principal = "mi_fondo_krautrock.jpg"
css_fondo_principal = ""
try:
    base64_img_main = obtener_base64_archivo(ruta_fondo_principal)
    css_fondo_principal = f"""
        [data-testid="stMain"] {{
            background-image: url("data:image/jpg;base64,{base64_img_main}") !important;
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
        }}
    """
except FileNotFoundError:
    css_fondo_principal = """
        [data-testid="stMain"] {
            background-color: #0f1115 !important;
        }
    """

# 2. Tipografía Personalizada
ruta_fuente_local = "Basenji-SemiBold.otf"
css_fuente_custom = ""
try:
    base64_font = obtener_base64_archivo(ruta_fuente_local)
    css_fuente_custom = f"""
        @font-face {{
            font-family: 'MiFuentePersonalizada';
            src: url("data:font/otf;charset=utf-8;base64,{base64_font}") format('opentype');
        }}

        h1, .stApp h1 {{
            font-family: 'MiFuentePersonalizada', sans-serif !important;
            font-size: 70px !important;
            color: #FF4757 !important;
            text-shadow: 3px 3px 12px rgba(0, 0, 0, 0.8), 0 0 20px rgba(255, 71, 87, 0.4) !important;
        }}
    """
except FileNotFoundError:
    pass

# ==============================================================================
# INYECCIÓN UNIFICADA DE ESTILOS CSS
# ==============================================================================
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');

    /* Ocultar barra lateral completamente */
    [data-testid="stSidebar"] {{
        display: none !important;
    }}

    /* Estilos dinámicos inyectados */
    {css_fuente_custom}
    {css_fondo_principal}

    html, body, [class*="css"], .stMarkdown {{
        font-family: 'Space Grotesk', sans-serif;
    }}

    .stApp {{
        color: #f1f5f9;
    }}

    /* Estilo de la sombra del subtítulo */
    .hero-subtitle {{
        text-align: center;
        color: #ffffff;
        font-size: 18px;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.9);
        margin-bottom: 25px;
    }}

    /* Tarjeta de resultado */
    .kraut-card {{
        background-image:
            linear-gradient(
                135deg,
                rgba(30, 34, 43, 0.85),
                rgba(17, 19, 24, 0.85)
            );
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        border-radius: 16px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8),
                    0 0 15px rgba(255, 71, 87, 0.2);
        border: 1px solid #ff4757;
        margin-top: 20px;
    }}

    .artist-title {{
        color: #ff4757;
        font-size: 32px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 10px;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.7);
    }}

    .album-sub {{
        color: #ffa502;
        font-size: 20px;
        font-weight: 600;
        font-style: italic;
    }}

    /* Contenedor estandarizado para las portadas con espacio inferior añadido */
    .cover-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 15px;
        margin-bottom: 30px; /* Espacio perfecto antes del botón */
    }}
    
    .cover-container img {{
        width: 100% !important;
        max-width: 320px !important;
        height: 320px !important;
        object-fit: cover !important;
        border-radius: 12px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.7), 0 0 10px rgba(255, 165, 2, 0.3);
        border: 2px solid rgba(255, 255, 255, 0.15);
    }}

    /* Forzar centrado absoluto del contenedor del botón en Streamlit */
    div.stButton {{
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }}

    div.stButton > button {{
        background: linear-gradient(135deg, #ff4757 0%, #ff6b81 100%);
        color: white;
        font-size: 20px;
        font-weight: bold;
        border-radius: 50px;
        padding: 15px 40px;
        border: none;
        width: 100%;
        max-width: 400px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.6),
                    0 4px 15px rgba(255, 71, 87, 0.6);
        transition: all 0.3s ease;
        display: block;
        margin: 0 auto;
    }}

    div.stButton > button:hover {{
        background: linear-gradient(135deg, #ff6b81 0%, #ff4757 100%);
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.8),
                    0 6px 20px rgba(255, 71, 87, 0.8);
    }}

    /* Texto encima de la barra de búsqueda (Centrado, Blanco y con Sombra) */
    div[data-testid="stSelectbox"] > label {{
        display: block !important;
        width: 100% !important;
        text-align: center !important;
    }}

    div[data-testid="stSelectbox"] > label p {{
        width: 100% !important;
        text-align: center !important;
        margin: 0 auto !important;

        color: #ffffff !important;
        font-size: 18px !important;
        font-weight: 700 !important;

        text-shadow:
            2px 2px 6px rgba(0, 0, 0, 0.95),
            0 0 10px rgba(0, 0, 0, 0.75) !important;
    }}
    </style>
""", unsafe_allow_html=True)

PORTADA_DEFAULT = "https://images.unsplash.com/photo-1539375665275-f9de415ef9ac?w=500"
RUTA_EXCEL_LOCAL = "German_Progressive_Rock_Bands_and_Albums.xlsx"

# ==============================================================================
# 2. FUNCIÓN DE CARGA Y PARSEO DEL EXCEL
# ==============================================================================
def cargar_catalogo(fuente):
    try:
        if isinstance(fuente, str):
            df = pd.read_excel(fuente)
        else:
            if fuente.name.endswith('.csv'):
                df = pd.read_csv(fuente)
            else:
                df = pd.read_excel(fuente)

        if df.empty:
            return []

        col_artista = df.columns[0]
        col_disco = df.columns[1] if len(df.columns) > 1 else df.columns[0]
        
        for col in df.columns:
            nombre_col = str(col).lower()
            if "banda" in nombre_col or "artista" in nombre_col or "nombre" in nombre_col:
                col_artista = col
            if "disco" in nombre_col or "álbum" in nombre_col or "album" in nombre_col or "título" in nombre_col:
                col_disco = col

        col_cover = next((col for col in df.columns if "cover" in str(col).lower() or "imagen" in str(col).lower() or "portada" in str(col).lower()), None)

        catalogo = []
        for _, row in df.iterrows():
            artista = str(row[col_artista]).strip() if pd.notna(row[col_artista]) else ""
            if not artista or artista.lower() == 'nan':
                continue

            disco = str(row[col_disco]).strip() if col_disco and pd.notna(row[col_disco]) else "Selección Krautrock"
            
            cover = PORTADA_DEFAULT
            if col_cover and col_cover in df.columns and pd.notna(row[col_cover]):
                val_cover = str(row[col_cover]).strip()
                if val_cover and val_cover.lower() != 'nan':
                    cover = val_cover

            catalogo.append({
                "artista": artista,
                "disco": disco,
                "cover": cover
            })

        return catalogo
    except Exception as e:
        return []

# Inicializar estado del catálogo con respaldo de seguridad
if "catalogo" not in st.session_state or not st.session_state.catalogo:
    catalogo_cargado = []
    if os.path.exists(RUTA_EXCEL_LOCAL):
        catalogo_cargado = cargar_catalogo(RUTA_EXCEL_LOCAL)
    
    if not catalogo_cargado:
        catalogo_cargado = [
            {"artista": "Amon Düül II", "disco": "Yeti", "cover": PORTADA_DEFAULT},
            {"artista": "Can", "disco": "Tago Mago", "cover": PORTADA_DEFAULT},
            {"artista": "Neu!", "disco": "Neu!", "cover": PORTADA_DEFAULT},
            {"artista": "Tangerine Dream", "disco": "Phaedra", "cover": PORTADA_DEFAULT}
        ]
    st.session_state.catalogo = catalogo_cargado

lista_artistas = sorted(list(set(item['artista'] for item in st.session_state.catalogo)))

# ==============================================================================
# 3. INTERFAZ PRINCIPAL & RULETA
# ==============================================================================
st.markdown("<h1 style='text-align: center;'> Krautrock Roulette</h1>", unsafe_allow_html=True)
st.markdown("<p class='hero-subtitle'>Explora el universo del rock experimental alemán de los años setenta.</p>", unsafe_allow_html=True)

# 1. Zona de resultados
zona_resultado = st.empty()

# 2. Botón centrado garantizado mediante columnas simétricas
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    presionado = st.button("🔀 ¡SELECCIONAR BANDA ALEATORIA!")

st.write("")

# 3. Buscador Desplegable debajo del botón
opcion_seleccionada = st.selectbox(
    "🔍 O selecciona un artista del catálogo:",
    ["-- Elegir de la lista --"] + lista_artistas
)

elegido = None

if presionado:
    for _ in range(15):
        muestra = random.choice(st.session_state.catalogo)
        zona_resultado.markdown(f"""
            <div class="kraut-card" style="opacity: 0.7;">
                <p style="font-size: 30px; margin: 0;">🎛️</p>
                <div class="artist-title">{muestra['artista']}</div>
                <div class="album-sub">{muestra['disco']}</div>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(0.08)

    elegido = random.choice(st.session_state.catalogo)

elif opcion_seleccionada != "-- Elegir de la lista --":
    discos_artista = [item for item in st.session_state.catalogo if item['artista'] == opcion_seleccionada]
    if discos_artista:
        elegido = random.choice(discos_artista)

if elegido:
    with zona_resultado.container():
        st.markdown(f"""
            <div class="kraut-card">
                <p style="font-size: 14px; color: #ffa502; font-weight: bold;">🔊 BANDA SELECCIONADA PARA ESCUCHAR:</p>
                <div class="artist-title">{elegido['artista']}</div>
                <div class="album-sub">"{elegido['disco']}"</div>
            </div>
        """, unsafe_allow_html=True)
        st.write("")
        
        st.markdown(f"""
            <div class="cover-container">
                <img src="{elegido['cover']}" alt="Portada del disco">
            </div>
        """, unsafe_allow_html=True)