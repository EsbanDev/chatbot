# 💬 Chatbot con Gemini + Whisper

Chatbot construido con [Streamlit](https://streamlit.io/) que se conecta a la API de **Gemini** (usando la capa de compatibilidad con el SDK de OpenAI) y permite enviar mensajes por texto o por voz, transcribiendo el audio localmente con **Whisper**.

## ✨ Características

- Interfaz de chat con historial persistente durante la sesión.
- Streaming de respuestas (el texto aparece progresivamente, no de golpe).
- Entrada por voz: graba un mensaje desde el micrófono y transcríbelo con Whisper antes de enviarlo.
- Opción de descartar una grabación de audio sin transcribirla.
- Botón para reiniciar la conversación (limpia también cualquier audio pendiente).

## 📋 Requisitos previos

- Python 3.9 o superior.
- Una API key de Gemini, obtenida en [Google AI Studio](https://aistudio.google.com/).
- **ffmpeg** instalado en el sistema (requerido por Whisper para procesar audio). No se instala con `pip`, es un programa aparte.
  - Windows: descarga desde [gyan.dev](https://www.gyan.dev/ffmpeg/builds/), descomprime, y agrega la carpeta `bin` al `PATH` del sistema.
  - macOS: `brew install ffmpeg`
  - Linux (Debian/Ubuntu): `sudo apt install ffmpeg`

## 🚀 Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/EsbanDev/chatbot.git
   cd chatbot
   ```

2. (Opcional pero recomendado) Crea un entorno virtual:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura tu API key. Crea la carpeta `.streamlit/` en la raíz del proyecto (si no existe) y dentro un archivo `secrets.toml`:
   ```toml
   GEMINI_API_KEY = "tu-api-key-aqui"
   ```
   > ⚠️ Este archivo **no** se sube al repositorio (está en `.gitignore`). Nunca compartas tu API key públicamente.

## ▶️ Uso

```bash
streamlit run app.py
```

Esto abrirá la app en tu navegador. Desde ahí puedes:
- Escribir un mensaje y presionar Enter.
- O grabar un mensaje de voz con el botón de micrófono, y elegir "Transcribir y enviar" o "Descartar audio".

## ⚙️ Configuración adicional

- **Modelo de Gemini**: se define en la variable `MODEL_NAME` al inicio de `app.py`.
- **Tamaño del modelo de Whisper**: se define en `WHISPER_MODEL_SIZE` (opciones: `tiny`, `base`, `small`, `medium`, `large`). Modelos más grandes son más precisos pero más lentos, especialmente en CPU.

## 🧯 Problemas comunes

- **`FP16 is not supported on CPU; using FP32 instead`**: advertencia inofensiva de Whisper al correr en CPU en vez de GPU. No afecta el resultado de la transcripción.
- **Respuestas lentas**: puede deberse a carga del servidor de Gemini, o a que Whisper corre en CPU (una GPU NVIDIA con CUDA acelera bastante la transcripción).
- **Error al leer `secrets.toml`**: confirma que el archivo tenga contenido válido en formato TOML y que la carpeta se llame exactamente `.streamlit`.

## 📄 Licencia

Este proyecto no tiene licencia definida aún. Agrega un archivo `LICENSE` si planeas distribuirlo públicamente.
