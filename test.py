import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Use default microphone as audio source
with sr.Microphone() as source:
    print("🎙️ Speak something...")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

    try:
        print("🔍 Recognizing...")
        text = recognizer.recognize_google(audio)
        print("📝 You said: " + text)
    except sr.UnknownValueError:
        print("❌ Sorry, could not understand audio.")
    except sr.RequestError as e:
        print("⚠️ Could not request results; {0}".format(e))
