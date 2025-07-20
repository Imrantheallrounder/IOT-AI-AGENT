import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Function to recognize speech
def transcribe_audio():
    # Use the microphone as the audio source
    with sr.Microphone() as source:
        print("Please say something...")
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)
        # Listen to the audio from the microphone
        audio = recognizer.listen(source)

    try:
        # Use the Google Web Speech API to transcribe the audio
        print("Transcribing...")
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        
    return None

if __name__=="__main__":
    # Call the function to transcribe audio
    transcribe_audio()
