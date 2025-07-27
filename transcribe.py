import speech_recognition as sr
import time

# Initialize recognizer
recognizer = sr.Recognizer()
# timeout time after user query completion
recognizer.pause_threshold = 1.2

# Function to recognize speech
def transcribe_audio():
    try:
        # Use the microphone as the audio source
        with sr.Microphone() as source:
            # Adjust for ambient noise
            # recognizer.adjust_for_ambient_noise(source, duration=0.2)
            # Listen to the audio from the microphone
            print("Please say something...")
            audio = recognizer.listen(source, timeout=2)

        # Use the Google Web Speech API to transcribe the audio
        print("Transcribing...")
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    except sr.WaitTimeoutError:
        print("WaitTimeoutError")
    except Exception as e:
        print("Something went wrong!!!")
        
    return None

if __name__=="__main__":
    # Call the function to transcribe audio
    transcribe_audio()
