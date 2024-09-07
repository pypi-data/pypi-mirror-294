import json
import os
import shutil
import filemac
import pyaudio
from vosk import KaldiRecognizer, Model

# Load the Vosk model
# Replace with the path to your Vosk model
model_path = "../src/vosk-model-en-us-0.22-lgraph"
model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)

# Set up the audio stream
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1,
                    rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

os.system("clear")  # Clear the screen also print("\033[H\033[J")
print("\033[1;30mSpeak into the microphone...\033[0m")

text = ""
# Get the width of the terminal
terminal_width = shutil.get_terminal_size().columns


def wrap_text(text, width):
    """Wrap the text to fit within the specified width."""
    wrapped_lines = []
    words = text.split()
    current_line = ""

    for word in words:
        # Check if adding the next word exceeds the width
        if len(current_line) + len(word) + 1 > width:
            wrapped_lines.append(current_line)
            current_line = word  # Start a new line with the current word
        else:
            if current_line:
                current_line += " "  # Add a space before the next word
            current_line += word

    if current_line:
        wrapped_lines.append(current_line)  # Add any remaining text

    return "\n".join(wrapped_lines)


try:
    while True:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text += " " + result['text']

            # Wrap the text and print it
            wrapped_text = wrap_text(text.strip(), terminal_width)
            print("\033[H\033[J")  # Clear the screen
            print("\033[1;30mSpeak into the microphone...\033[0m")
            print(f"\033[1;32m{wrapped_text}\033[0m", end='\r')
        else:
            partial_result = json.loads(recognizer.PartialResult())
            partial_text = partial_result['partial']
            # Wrap the partial text and print it
            wrapped_partial = wrap_text(
                text.strip() + " " + partial_text, terminal_width)
            print("\033[H\033[J")  # Clear the screen
            print("\033[1;30mSpeak into the microphone...\033[0m")
            print(f"\033[1;36m{wrapped_partial}\033[0m", end="\r")

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
