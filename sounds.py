from kokoro import KPipeline
import sounddevice as sd
import numpy as np

import os
import sys

# Initialize pipeline
pipeline = KPipeline(lang_code='a')

def play_chime(sound_path: str = "/Users/startus/Downloads/wakeup_sound.mp3"):
    """
    Plays a short chime sound to indicate the assistant is listening.
    
    Parameters:
        sound_path (str): Full path to the chime file. Must be an .mp3 or .wav depending on OS.
    """
    if not sound_path:
        # Default fallback path (you can customize this)
        sound_path = os.path.expanduser("~/sounds/assistant_chime.mp3")

    if not os.path.exists(sound_path):
        print(f"Chime file not found: {sound_path}")
        return

    if sys.platform == "darwin":  # macOS
        os.system(f'afplay "{sound_path}"')
    elif sys.platform.startswith("linux"):  # Raspberry Pi / Linux
        # Choose aplay for WAV or mpg123 for MP3
        if sound_path.endswith(".wav"):
            os.system(f'aplay "{sound_path}"')
        elif sound_path.endswith(".mp3"):
            os.system(f'mpg123 "{sound_path}"')  # You need: sudo apt install mpg123
    else:
        print("Platform not supported for chime playback.")

    
def play_sound(text):
    SAMPLE_RATE = 24000
    print("Starting playback...")
    # Iterate through the chunks
    for gs, ps, audio in pipeline(text, voice='am_adam', speed=1):
        if audio is not None:
            # Play the audio chunk immediately
            # blocking=True ensures one chunk finishes before the next starts
            sd.play(audio, SAMPLE_RATE)
            sd.wait() 
    print("Playback finished.")


if __name__ == "__main__":
    play_chime()  # Play the default chime sound
    play_sound("This is a test!")