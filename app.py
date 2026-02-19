import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# --- 1. Configuración de la interfaz principal ---
st.set_page_config(
    page_title="Nano Car Configurator",
    page_icon="🚗",
    layout="wide"
)

# --- Definición de Opciones de Personalización ---
CAR_MODELS = {
    "Superdeportivo Clásico": "classic supercar, sleek lines",
    "SUV Futurista": "futuristic electric SUV, cyber truck style",
    "Sedán de Lujo": "luxury executive sedan",
    "Muscle Car Americano": "vintage American muscle car, aggressive stance",
    "Concepto de Carreras": "futuristic racing concept car, prototype"
}

CAR_COLORS = {
    "Rojo Carmesí Metalizado": "metallic crimson red paint",
    "Azul Eléctrico Mate": "matte electric blue finish",
    "Negro Fantasma": "glossy phantom black",
    "Blanco Perla": "pearlescent white",
    "Verde Lima Neón": "neon lime green",
    "Plata Titanio": "titanium silver"
}

ENVIRONMENTS = {
    "Ciudad Cyberpunk de Noche": "neon lit cyberpunk city street at night, wet asphalt reflecting lights",
    "Autopista Costera al Atardecer": "coastal highway during golden hour sunset, ocean view",
    "Sala de Exposición Minimalista": "minimalist high-end car showroom, white studio lighting",
    "Desierto Futurista": "futuristic desert landscape, sci-fi structures in background",
    "Pista de Carreras Mojada": "wet asphalt race track, dramatic clouds"
}

CAMERA_STYLES = {
    "Cinemático (Ángulo Bajo)": "cinematic low angle shot, dramatic lighting, shallow depth of field",
    "Fotografía de Estudio (Detallado)": "studio photography, highly detailed, neutral background, commercial look",
    "Vista Aérea (Dron)": "drone high angle view looking down",
    "Estilo Render 3D (Octane)": "3D render style, octane render, unreal engine 5, hyperrealistic"
}

# --- 3. Configuración de la función de llamada a la API ---
# AHORA RECIBE LA API KEY COMO PARÁMETRO
def call_nano_banana_api(constructed_prompt: str, api_key: str) -> Image.Image:
    """
    Envía el prompt y la clave del usuario al modelo 'Nano Banana'.
    """
    # Reemplaza esta URL por la de un servicio real (OpenAI, Stable Diffusion, etc.)
    api_url = "https://api.nanobanana.example.com/v1/generate" 

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": constructed_prompt,
        "negative_prompt": "ugly, deformed, bad blurry, poor quality",
        "resolution": "1024x768",
        "steps": 30,
        "guidance_scale": 7.5 
    }
    
    response = requests.post(api_url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    
    image_data = BytesIO(response.content)
    return Image.open(image_data)


# --- Función Principal de la App ---
def main():
    st.title("🏎️ Configurador de Coches - Nano Banana Engine")
    st.markdown("Diseña tu vehículo usando los controles y genera una visualización de alta calidad.")

    # --- Sidebar para Configuración ---
    with st.sidebar:
        st.header("🔑 Credenciales")
        # Nuevo campo para que el usuario introduzca su API Key de forma segura
        user_api_key = st.text_input(
            "Introduce tu API Key", 
            type="password", 
            help="Tu clave se usa solo para esta sesión y no se guarda."
        )
        
        st.divider()
        
        st.header("🛠️ Personalización")
        selected_model_key = st.selectbox("Modelo del Vehículo", list(CAR_MODELS.keys()))
        selected_color_key = st.selectbox("Color y Acabado", list(CAR_COLORS.keys()))
        
        st.divider()
        
        st.header("🌍 Entorno y Estilo")
        selected_env_key = st.selectbox("Escenario de Fondo", list(ENVIRONMENTS.keys()))
        selected_cam_key = st.selectbox("Estilo de Cámara/Render", list(CAMERA_STYLES.keys()))
        
        st.divider()
        
        # Botón de generación
        generate_btn = st.button("🚀 Generar Vehículo", type="primary", use_container_width=True)

    # --- Lógica de Generación ---
    if generate_btn:
        # Validación: Comprobar si el usuario ha introducido la API Key
        if not user_api_key.strip():
            st.warning("⚠️ Por favor, introduce tu API Key en el menú lateral antes de generar la imagen.")
            return # Detiene la ejecución aquí si no hay clave

        # Construcción del Prompt
        model_prompt = CAR_MODELS[selected_model_key]
        color_prompt = CAR_COLORS[selected_color_key]
        env_prompt = ENVIRONMENTS[selected_env_key]
        style_prompt = CAMERA_STYLES[selected_cam_key]

        full_prompt = (
            f"A high quality {style_prompt} of a {color_prompt} {model_prompt}, "
            f"situated in a {env_prompt}. Highly detailed, photorealistic, 8k resolution, automotive photography masterpiece."
        )

        with st.container():
            with st.spinner("⚙️ El motor Nano Banana está renderizando tu diseño..."):
                try:
                    # Llamada a la API PASANDO LA CLAVE DEL USUARIO
                    generated_image = call_nano_banana_api(full_prompt, user_api_key)
                    
                    st.success("¡Vehículo renderizado exitosamente!")
                    
                    col1, col2, col3 = st.columns([1, 8, 1])
                    with col2:
                         st.image(
                             generated_image,
                             caption=f"{selected_model_key} en {selected_color_key}",
                             use_container_width=True
                         )
                    
                except requests.exceptions.ConnectionError:
                    st.error("⛔ Error de conexión. Verifica que la URL de la API sea correcta y accesible.")
                except requests.exceptions.HTTPError as http_err:
                    if response.status_code == 401:
                        st.error("⛔ Error de Autenticación: Tu API Key parece ser incorrecta o no válida.")
                    else:
                        st.error(f"⛔ Error HTTP devuelto por la API: {http_err}")
                except Exception as e:
                    st.error(f"⛔ Se ha producido un error inesperado: {e}")

    else:
        st.info("👈 Introduce tu API Key, configura las opciones y pulsa 'Generar Vehículo'.")

if __name__ == "__main__":
    main()