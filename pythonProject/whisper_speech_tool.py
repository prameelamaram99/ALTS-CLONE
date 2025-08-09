import whisper  # Import OpenAI Whisper speech-to-text model library
import torch  # Import PyTorch for tensor operations
import torchaudio  # Audio utilities in PyTorch for loading & processing audio
import sounddevice as sd  # Library to record audio from microphone
import scipy.io.wavfile as wav  # For saving recorded audio as WAV file
import os  # For operating system file management


def record_audio(output_file="user_input.wav", duration=5, sample_rate=16000):
    """
    Records audio from the microphone and saves it as a WAV file.
    """
    print(f"🎙️ Recording for {duration} seconds... Speak now!")

    # Start recording audio from default microphone
    # Parameters:
    #   - number of frames = duration (seconds) * sample_rate (samples/sec)
    #   - samplerate = 16000 Hz (standard for speech recognition)
    #   - mono audio (channels=1)
    #   - 16-bit integer samples (dtype="int16")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")

    sd.wait()  # Wait until recording is finished

    # Save recorded audio data as WAV file with the given sample rate
    wav.write(output_file, sample_rate, recording)

    print(f"✅ Recording saved to {output_file}")

    # Return the path of saved WAV file
    return output_file


def load_audio_correctly(file_path):
    """
    Loads an audio file using torchaudio, converts to mono, and resamples to 16000 Hz.
    """
    # Load audio file from disk into a tensor (waveform) and get its sample rate
    waveform, sample_rate = torchaudio.load(file_path)

    # If audio has more than one channel (e.g. stereo), average them to get mono audio
    if waveform.shape[0] > 1:
        waveform = torch.mean(waveform, dim=0, keepdim=True)

    # If audio sample rate is not 16000 Hz, resample it to 16000 Hz for Whisper compatibility
    if sample_rate != 16000:
        resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
        waveform = resampler(waveform)

    # Remove the first dimension (channel) and return 1D tensor of audio samples
    return waveform.squeeze(0)


def transcribe_audio(file_path):
    """
    Transcribes audio using OpenAI Whisper.
    """
    # Load the Whisper model into memory; "base" is a good balance of speed and accuracy
    model = whisper.load_model("base")  # Other options: "tiny", "small", "medium", "large"

    # Load the audio file correctly and preprocess it
    audio = load_audio_correctly(file_path)

    # Trim or pad audio tensor to the expected length for Whisper
    audio = whisper.pad_or_trim(audio)

    # Convert audio samples to log-Mel spectrogram (input format for Whisper)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # Set decoding options:
    # fp16=False means use 32-bit floating point (needed for CPU)
    # language="te" forces transcription to Telugu language (use language codes)
    options = whisper.DecodingOptions(fp16=False, language="te")

    # Perform the actual transcription decoding step on the model with given options
    result = whisper.decode(model, mel, options)

    # Print the transcribed text result
    print("\n📝 Transcription:")
    print(result.text)


def main():
    print("🎧 Whisper Speech-to-Text Tool")
    print("-----------------------------")

    # Ask user how many seconds to record audio for
    duration = int(input("How many seconds do you want to record? (e.g., 5): "))

    # Record audio from microphone and save as WAV file
    file_path = record_audio(duration=duration)

    # Transcribe the saved audio file with Whisper
    transcribe_audio(file_path)

    # Optional: delete the recorded audio file after transcription to keep things clean
    if os.path.exists(file_path):
        os.remove(file_path)


# Python standard boilerplate to run main() when this script is executed directly
if __name__ == "__main__":
    main()
