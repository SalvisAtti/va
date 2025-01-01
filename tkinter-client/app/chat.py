import tkinter as tk
import requests
import json
import os
import speech_recognition as sr
import pyttsx3
from tkinter.scrolledtext import ScrolledText

# Load configuration from JSON file
config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path) as config_file:
    config = json.load(config_file)

API_URL = config['api_url']
THREAD_ID = config['thread_id']

listener = sr.Recognizer()
machine = pyttsx3.init()

# --- Helper Functions ---
def talk(text):
    """Speak out the provided text."""
    machine.say(text)
    machine.runAndWait()

def capture_voice_input():
    """Capture and process user voice input."""
    try:
        with sr.Microphone() as source:
            print("Listening...")
            talk("I'm listening.")
            audio = listener.listen(source)
            instruction = listener.recognize_google(audio)
            print(f"Voice input: {instruction}")
            return instruction
    except sr.UnknownValueError:
        talk("Sorry, I did not catch that. Please try again.")
    except sr.RequestError:
        talk("Sorry, I'm having trouble connecting to the speech recognition service.")
    return ""

# --- Main Chat Application ---
class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ManVA Chat")

        self.messages_frame = tk.Frame(self.root)
        self.messages_frame.pack()

        self.messages_text = ScrolledText(self.messages_frame, state='disabled', width=60, height=20, wrap=tk.WORD)
        self.messages_text.pack()

        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack()

        self.input_field = tk.Entry(self.input_frame, width=50)
        self.input_field.pack(side=tk.LEFT, padx=5)
        self.input_field.bind("<Return>", self.send_message_with_event)

        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=5)

        self.voice_button = tk.Button(self.input_frame, text="🎤", command=self.voice_input)
        self.voice_button.pack(side=tk.LEFT, padx=5)

        self.populate_chat()

    def populate_chat(self):
        """Fetches the conversation history and displays it."""
        response = requests.get(f"{API_URL}/conversation-history/?thread_id={THREAD_ID}")
        if response.status_code == 200:
            data = response.json()
            self.messages_text.config(state='normal')
            for message in data['conversation_history']:
                self.messages_text.insert(tk.END, f"{message['sender']}: {message['content']}\n")
            self.messages_text.config(state='disabled')
            self.messages_text.yview(tk.END)

    def send_message(self):
        """Sends a new message and updates the chat."""
        user_message = self.input_field.get()
        if user_message:
            self.display_message("You", user_message)
            self.input_field.delete(0, tk.END)
            self.handle_response(user_message)

    def send_message_with_event(self, event):
        """Wrapper to handle sending a message when 'Enter' key is pressed."""
        self.send_message()

    def voice_input(self):
        """Handles voice input from the user."""
        instruction = capture_voice_input()
        if instruction:
            self.display_message("You (Voice)", instruction)
            self.handle_response(instruction)

    def handle_response(self, message):
        """Processes the user message and updates the chat."""
        response = requests.post(f"{API_URL}/send-message/", json={"thread_id": THREAD_ID, "message": message})
        if response.status_code == 200:
            assistant_response = response.json().get("response", "")
            self.display_message("Assistant", assistant_response)
            talk(assistant_response)

    def display_message(self, sender, message):
        """Displays a message in the chat window."""
        self.messages_text.config(state='normal')
        self.messages_text.insert(tk.END, f"{sender}: {message}\n")
        self.messages_text.config(state='disabled')
        self.messages_text.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    chat_app = ChatApp(root)
    root.mainloop()
