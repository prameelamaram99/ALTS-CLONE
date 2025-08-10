### Prerequisites
Python 3.10+ (3.11 works fine, avoid 3.12+ if using Whisper or Coqui TTS)
Pip (latest version)
Git installed
FFmpeg installed and available in PATH (Whisper & TTS need it)
Ollama installed locally (for running LLaMA 3.2)

Windows: choco install git ffmpeg
Download Ollama from https://ollama.com/download
ollama pull llama3.2


--------------------------------------------------------------------------------------------------------
# Clone Your Project
git clone https://github.com/yourusername/your-repo.git
cd your-repo

# Create Virtual Environment
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows

# Install Python Dependencies
pip install git+https://github.com/alxpez/keyboard.git
pip install git+https://github.com/alxpez/alts-notify.git
pip install litellm openai-whisper pystray python-dotenv simpleaudio sounddevice soundfile psutil
pip install TTS pyyaml pillow

# Download Models
python -m whisper --model base.en

# Run the Program
python alts.py

