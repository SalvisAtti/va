# Refactored MainVA.py
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia

listener = sr.Recognizer()
machine = pyttsx3.init()

def talk(text):
    """Speak out the provided text."""
    machine.say(text)
    machine.runAndWait()

def play_on_youtube(query):
    """Play a video on YouTube based on the query."""
    try:
        pywhatkit.playonyt(query)
        return f"Playing {query} on YouTube."
    except Exception as e:
        return f"Error searching YouTube: {e}"

def tell_time():
    """Provide the current time."""
    return datetime.datetime.now().strftime('%I:%M %p')

def tell_date():
    """Provide the current date."""
    return datetime.datetime.now().strftime('%d/%m/%Y')

def provide_greeting():
    """Respond to a greeting."""
    return "Thanks! I'm fine. How about you?"

def tell_name():
    """Introduce the assistant's name."""
    return "I am Tom. What can I do for you?"

def search_wikipedia(query):
    """Search Wikipedia for information about the query."""
    try:
        info = wikipedia.summary(query, sentences=1)
        return info
    except wikipedia.exceptions.PageError:
        search_results = wikipedia.search(query)
        if search_results:
            closest_match = search_results[0]
            try:
                info = wikipedia.summary(closest_match, sentences=1)
                return f"Couldn't find an exact match, but here's information on {closest_match}: {info}"
            except Exception:
                return "Sorry, I couldn't find any information."
        return "Sorry, I couldn't find any information."

def calculate(expression):
    """Evaluate and return the result of a mathematical expression."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Calculation error: {e}"
