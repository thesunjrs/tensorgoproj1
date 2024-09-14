import os
import pyttsx3
import speech_recognition as sr
import webbrowser
import google.generativeai as genai

print(f"GOOGLE_API_KEY from environment: {os.getenv('GOOGLE_API_KEY')}")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("No GOOGLE_API_KEY found. Please set the environment variable or pass the key directly.")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def Reply(question):
    prompt = f"Chando: {question}\nJarvis:"
    try:
        chat = model.start_chat(history=[])
        response = chat.send_message(prompt)
        answer = response.text.strip()
        return answer
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I'm sorry, I couldn't process that."

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print("Say that again please...")
            return "None"
        return query

if __name__ == "__main__":
    while True:
        query = takeCommand().lower()
        if 'exit' in query:
            break
        response = Reply(query)
        speak(response)
