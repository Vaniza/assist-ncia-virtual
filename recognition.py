import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
import requests
import json
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


def init_speech():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Voz em português
    return engine

# Módulo Text to Speech
def speak(engine, text):
    engine.say(text)
    engine.runAndWait()

# Módulo Speech to Text
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ouvindo...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language='pt-BR')
            print(f"Você disse: {text}")
            return text.lower()
        except:
            print("Não entendi o comando.")
            return ""

# Função para pesquisar no Wikipedia
def search_wikipedia(query):
    wikipedia.set_lang("pt")
    try:
        result = wikipedia.summary(query, sentences=2)
        return result
    except:
        return "Não foi possível encontrar informações sobre isso."

# Função para abrir YouTube
def open_youtube():
    webbrowser.open("https://www.youtube.com")

# Função para encontrar farmácia mais próxima
def find_nearest_pharmacy(latitude, longitude):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{latitude},{longitude}",
        "radius": "5000",
        "type": "pharmacy",
        "key": "SUA_CHAVE_API_AQUI"  # Substitua pela sua chave API do Google Places
    }
    
    try:
        response = requests.get(url, params=params)
        results = response.json()
        if results["status"] == "OK":
            nearest = results["results"][0]
            return f"A farmácia mais próxima é {nearest['name']}"
        return "Não foi possível encontrar farmácias próximas."
    except:
        return "Erro ao buscar farmácias."

def main():
    engine = init_speech()
    speak(engine, "Olá! Como posso ajudar?")
    
    while True:
        command = listen()
        
        if "pesquisar" in command:
            query = command.replace("pesquisar", "").strip()
            result = search_wikipedia(query)
            speak(engine, result)
            
        elif "youtube" in command:
            speak(engine, "Abrindo YouTube")
            open_youtube()
            
        elif "farmácia" in command:
            # Usando uma localização fixa para exemplo
            # Em uma implementação real, você pode usar a localização atual do usuário
            latitude = -23.550520
            longitude = -46.633308
            result = find_nearest_pharmacy(latitude, longitude)
            speak(engine, result)
            
        elif "sair" in command:
            speak(engine, "Até logo!")
            break

if __name__ == "__main__":
    main()
