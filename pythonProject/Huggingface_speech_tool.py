import torch
import torchaudio
import sounddevice as sd
from scipy.io.wavfile import write
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

# Load Hugging Face model and tokenizer (cached after first use)
print("🔄 Loading model... (may take a moment on first run)")
tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

# Transcribe from WAV file
def recognize_from_wav_file(filename):
    try:
        print(f"📁 Loading audio from: {filename}")
        waveform, sample_rate = torchaudio.load(filename)

        if sample_rate != 16000:
            print("🔁 Resampling audio to 16kHz")
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
            waveform = resampler(waveform)

        input_values = tokenizer(waveform.squeeze().numpy(), return_tensors="pt").input_values

        with torch.no_grad():
            logits = model(input_values).logits

        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = tokenizer.decode(predicted_ids[0])

        print("\n🗣️ Transcription:")
        print(transcription)
    except Exception as e:
        print(f"❌ Error processing file: {e}")

# Transcribe from microphone
def recognize_from_microphone():
    try:
        print("🎤 Recording from microphone (say something)...")
        duration = 5  # seconds
        sample_rate = 16000
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()
        write("mic_input.wav", sample_rate, recording)  # Save to WAV

        recognize_from_wav_file("mic_input.wav")
    except Exception as e:
        print(f"❌ Error recording: {e}")

# === MAIN MENU ===
def main():
    while True:
        print("\n=== Hugging Face Offline Speech-to-Text ===")
        print("1. Use microphone")
        print("2. Transcribe WAV file")
        print("3. Exit")
        choice = input("Enter choice (1/2/3): ").strip()

        if choice == '1':
            recognize_from_microphone()
        elif choice == '2':
            filename = input("Enter path to .wav file: ").strip()
            recognize_from_wav_file(filename)
        elif choice == '3':
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
