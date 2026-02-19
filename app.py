import streamlit as st
from PIL import Image
from io import BytesIO
from google import genai
from google.genai import errors

# --- 1. Configuración de la interfaz principal ---
st.set_page_config(
    page_title="Gemini Car Configurator",
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

# --- 3. Configuración de la llamada a la API de Google Gemini ---
def generate_car_image_gemini(prompt: str, api_key: str) -> Image.Image:
    """
    Envía el prompt al modelo de generación de imágenes de Google (Imagen 3).
    """
    # Inicializar el cliente de Gemini con la clave del usuario
    client = genai.Client(api_key=api_key)
    
    # Llamar al modelo Imagen 3
    result = client.models.generate_images(
        model='imagen-3.0-fast-generate-001',
        prompt=prompt,
        config=dict(
            number_of_images=1,
            aspect_ratio="4:3", # Formato horizontal ideal para coches
            output_mime_type="image/jpeg",
        )
    )
    
    # Extraer los bytes de la primera imagen generada y convertirla a un objeto PIL Image
    if result.generated_images:
        image_bytes = result.generated_images[0].image.image_bytes
        return Image.open(BytesIO(image_bytes))
    else:
        raise ValueError("La API no devolvió ninguna imagen.")

# --- Función Principal de la App ---
def main():
    st.title("🏎️ Configurador de Coches - Google Imagen 3")
    st.markdown("Diseña tu vehículo usando los controles y genera una visualización de alta calidad con la API de Gemini.")

    # --- Sidebar para Configuración ---
    with st.sidebar:
        st.header("🔑 Credenciales")
        # Campo para la API Key de Google Gemini
        user_api_key = st.text_input(
            "Introduce tu Gemini API Key", 
            type="password", 
            help="Consigue tu API key gratis en Google AI Studio."
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
        if not user_api_key.strip():
            st.warning("⚠️ Por favor, introduce tu Gemini API Key en el menú lateral.")
            return

        # Construcción del Prompt
        model_prompt = CAR_MODELS[selected_model_key]
        color_prompt = CAR_COLORS[selected_color_key]
        env_prompt = ENVIRONMENTS[selected_env_key]
        style_prompt = CAMERA_STYLES[selected_cam_key]

        full_prompt = (
            f"A high quality {style_prompt} of a {color_prompt} {model_prompt}, "
            f"situated in a {env_prompt}. Highly detailed, photorealistic, automotive photography masterpiece."
        )

        with st.container():
            with st.spinner("⚙️ El motor de Google está renderizando tu diseño... (Puede tardar unos segundos)"):
                try:
                    # Llamada a la API de Gemini
                    generated_image = generate_car_image_gemini(full_prompt, user_api_key)
                    
                    st.success("¡Vehículo renderizado exitosamente!")
                    
                    col1, col2, col3 = st.columns([1, 8, 1])
                    with col2:
                         st.image(
                             generated_image,
                             caption=f"{selected_model_key} en {selected_color_key}",
                             use_container_width=True
                         )
                    
                except errors.APIError as api_err:
                    st.error(f"⛔ Error de la API de Google: Verifica que tu API Key sea correcta. Detalle: {api_err}")
                except Exception as e:
                    st.error(f"⛔ Se ha producido un error inesperado: {e}")

    else:
        st.info("👈 Introduce tu API Key, configura las opciones y pulsa 'Generar Vehículo'.")

if __name__ == "__main__":
    main()