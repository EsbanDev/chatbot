import os
import tempfile
import streamlit as st
import whisper
from openai import OpenAI

# CONFIGURACIÓN
MODEL_NAME = "gemini-3.7-flash"

st.set_page_config(page_title="Chatbot Gemini", page_icon="💬")
st.title("CHATBOT PRO 😈")

# API KEY
api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))

if not api_key:
    st.error(
        "No se encontró la API key. Defínela en `.streamlit/secrets.toml` "
        "como `GEMINI_API_KEY` o como variable de entorno."
    )
    st.stop()

# CLIENTE 
client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=api_key,
)

# MODELO DE WHISPER 
WHISPER_MODEL_SIZE = "base"


@st.cache_resource(show_spinner="Cargando modelo de Whisper...")
def load_whisper_model():
    return whisper.load_model(WHISPER_MODEL_SIZE)


whisper_model = load_whisper_model()

# HISTORIAL DE CONVERSACIÓN
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Eres un asistente útil y conciso."}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# BOTÓN PARA REINICIAR CONVERSACIÓN
with st.sidebar:
    st.subheader("Opciones")
    if st.button("🗑️ Nueva conversación"):
        st.session_state.messages = [
            {"role": "system", "content": "Eres un asistente útil y conciso."}
        ]
        # Limpia cualquier audio grabado que no se haya enviado.
        st.session_state.audio_widget_counter = (
            st.session_state.get("audio_widget_counter", 0) + 1
        )
        st.session_state.pop("pending_audio_transcript", None)
        st.rerun()
    st.caption(f"Modelo: `{MODEL_NAME}`")

# ENTRADA DE AUDIO (Whisper)
# st.audio_input graba desde el micrófono del navegador y devuelve un
# archivo de audio en memoria 
#
if "audio_widget_counter" not in st.session_state:
    st.session_state.audio_widget_counter = 0

audio_key = f"audio_input_{st.session_state.audio_widget_counter}"
audio_value = st.audio_input("🎤 Envía un mensaje de voz", key=audio_key)

transcribed_text = None

# Si venimos de un rerun donde ya se transcribió el audio, recuperamos
# ese texto aquí (se guarda en session_state).
if "pending_audio_transcript" in st.session_state:
    transcribed_text = st.session_state.pop("pending_audio_transcript")

if audio_value is not None:
    col1, col2 = st.columns(2)
    with col1:
        send_audio = st.button(
            "✅ Transcribir y enviar", use_container_width=True
        )
    with col2:
        discard_audio = st.button(
            "🗑️ Descartar audio", use_container_width=True
        )

    if send_audio:
        audio_bytes = audio_value.getvalue()
        with st.spinner("Transcribiendo audio..."):
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp.write(audio_bytes)
                tmp_path = tmp.name

            try:
                result = whisper_model.transcribe(tmp_path, language="es")
                st.session_state.pending_audio_transcript = result["text"].strip()
            finally:
                os.remove(tmp_path)

        st.session_state.audio_widget_counter += 1
        st.rerun()

    elif discard_audio:
        st.session_state.audio_widget_counter += 1
        st.rerun()

# ENTRADA DEL USUARIO 
typed_input = st.chat_input("Escribe tu mensaje...")

user_input = transcribed_text or typed_input

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Llamar a la API y mostrar la respuesta 
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            stream = client.chat.completions.create(
                model=MODEL_NAME,
                messages=st.session_state.messages,
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    full_response += delta
                    placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)

        except Exception as e:
            full_response = f"⚠️ Ocurrió un error al llamar a la API: {e}"
            placeholder.error(full_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )