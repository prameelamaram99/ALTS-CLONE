import os
import sys
import json
import queue
import sounddevice as sd
import vosk
import wave

# === Configuration ===

# Set the model path here (change based on your language)
# For example:
# English: "model-en"
# Spanish: "model-es"
MODEL_PATH = "C:/Users/Hp/Downloads/vosk-model-en-us-librispeech-0.2/vosk-model-en-us-librispeech-0.2"

# Sample rate (depends on model, most are 16000 Hz)
SAMPLE_RATE = 16000


# === Helper: Load Vosk Model ===
def load_model():
    if not os.path.exists(MODEL_PATH):
        print(f"Model not found at '{MODEL_PATH}'.")
        print("Please download a model from https://alphacephei.com/vosk/models")
        sys.exit(1)
    return vosk.Model(MODEL_PATH)


# === Microphone Mode ===
def recognize_from_microphone():
    print("🎙️ Starting microphone recognition... Speak into the mic (Ctrl+C to stop)")

    q = queue.Queue()

    # Callback to store incoming audio data
    def callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        q.put(bytes(indata))

    model = load_model()
    recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)

    try:
        with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16',
                               channels=1, callback=callback):
            while True:
                data = q.get()
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    print("You said:", result.get("text", ""))
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")
    except Exception as e:
        print("Error:", e)


# === WAV File Mode ===
def recognize_from_microphone():
    print("🎙️ Starting microphone recognition... Speak into the mic.")
    print("🗣️ Say 'stop listening' to return to the menu.\n")

    q = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        q.put(bytes(indata))

    model = load_model()
    recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)

    try:
        with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16',
                               channels=1, callback=callback):
            while True:
                data = q.get()
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "").strip()
                    if text:
                        print("You said:", text)
                        if "stop listening" in text.lower():
                            print("👂 Stopping mic mode, returning to menu.")
                            break
    except Exception as e:
        print("Error:", e)



# === Main Program ===
def main():
    while True:
        print("\n=== Vosk Speech-to-Text ===")
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
