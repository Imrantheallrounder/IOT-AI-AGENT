import pvporcupine
import pyaudio
import struct
import os

from dotenv import load_dotenv
load_dotenv()

WAKEWORD_API_KEY = os.getenv("WAKEWORD_API_KEY")

async def listen_for_wake_word(
    keywords=None,
    on_detected=None,
    max_duration=None
):
    """
    Listens for wake words using Porcupine.
    
    Args:
        keywords (list): List of wake words to detect.
        on_detected (callable): Function to call when a wake word is detected. Gets passed the keyword string.
        max_duration (float): Optional duration in seconds to run before exiting.

    Raises:
        KeyboardInterrupt: If user interrupts with Ctrl+C.
    """
    if keywords is None:
        keywords = ["bumblebee", "picovoice", "jarvis", "alexa", "hey google", "hey siri", "porcupine"]

    porcupine = None
    audio_stream = None
    pa = None

    try:
        porcupine = pvporcupine.create(access_key=WAKEWORD_API_KEY, keywords=keywords)

        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length,
        )

        print(f"[WakeWord] Listening for: {', '.join(keywords)}")

        import time
        start_time = time.time()

        while True:
            if max_duration and (time.time() - start_time > max_duration):
                print("[WakeWord] Max duration reached, exiting...")
                break

            pcm_bytes = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm_ints = struct.unpack_from("h" * porcupine.frame_length, pcm_bytes)
            keyword_index = porcupine.process(pcm_ints)

            if keyword_index >= 0:
                keyword = keywords[keyword_index]
                # print(f"[WakeWord] Detected: {keyword}")
                if on_detected:
                    await on_detected(keyword)
                break

    except KeyboardInterrupt:
        print("[WakeWord] Interrupted by user.")
    finally:
        if audio_stream:
            audio_stream.stop_stream()
            audio_stream.close()
        if porcupine:
            porcupine.delete()
        if pa:
            pa.terminate()
        print("[WakeWord] Cleaned up.")


# Example usage (can be removed if used as a module):
if __name__ == "__main__":
    import asyncio
    # def handle_detection(keyword):
    #     print(f">>> Wake word '{keyword}' triggered an action!")
    def handle_detection(tmp):
        print(f">>>>>>>> Custom <<<<<<<<<<")

    # listen_for_wake_word(on_detected=handle_detection)
    asyncio.run(listen_for_wake_word(on_detected=handle_detection))