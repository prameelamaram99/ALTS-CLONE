import subprocess

# Function to speak text using eSpeak and save as a WAV file
def speak_with_espeak(text, voice="en-us", speed=140, pitch=70, output_file="output.wav"):
    """
    Speaks the given text using eSpeak and saves the output as a .wav file.

    Parameters:
    - text (str): The text to be spoken
    - voice (str): The voice/language code (default is 'en-us')
    - speed (int): Speaking speed in words per minute (default is 140)
    - pitch (int): Pitch level (0 to 99, default is 70)
    - output_file (str): The filename to save the audio (default is 'output.wav')
    """

    print("\n🔊 Speaking your text now...\n")

    # Speak the text out loud
    subprocess.run(["espeak", "-v", voice, "-s", str(speed), "-p", str(pitch), text])

    # Save the speech to a .wav file
    subprocess.run(["espeak", "-v", voice, "-s", str(speed), "-p", str(pitch), "-w", output_file, text])

    print(f"✅ Audio has been saved to '{output_file}'\n")

# --------- Main program starts here ---------

# Ask the user to enter some text
user_input = input("📝 Enter the text you want to convert to speech: ")

# Call the function to speak and save the audio
speak_with_espeak(user_input)
