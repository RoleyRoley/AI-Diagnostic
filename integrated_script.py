import psutil
import speech_recognition as sr
import pyttsx3
import random

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    memory_info = psutil.virtual_memory()
    return memory_info.percent

def get_disk_usage():
    disk_info = psutil.disk_usage('/')
    return disk_info.percent

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        return text.lower()
    except sr.RequestError:
        return "api unavailable"
    except sr.UnknownValueError:
        return "unable to recognize speech"

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

casual_responses = [
    "I'm just a computer program, but I'm here to help!",
    "Did you know I can monitor your system's performance?",
    "How can I assist you today?",
    "I'm always here if you need me.",
    "Feel free to ask me anything about your computer's health."
]

# Define keywords for different commands
cpu_keywords = ["cpu", "processor"]
memory_keywords = ["memory", "ram"]
disk_keywords = ["disk", "storage"]
shutdown_keywords = ["shutdown", "stop", "exit", "quit"]
greeting_keywords = ["hello", "hi"]
how_are_you_keywords = ["how are you", "what's up"]
thanks_keywords = ["thank you", "thanks"]

def process_command(command):
    if any(keyword in command for keyword in cpu_keywords):
        cpu_usage = get_cpu_usage()
        response = f"CPU Usage: {cpu_usage}%"
    elif any(keyword in command for keyword in memory_keywords):
        memory_usage = get_memory_usage()
        response = f"Memory Usage: {memory_usage}%"
    elif any(keyword in command for keyword in disk_keywords):
        disk_usage = get_disk_usage()
        response = f"Disk Usage: {disk_usage}%"
    elif any(keyword in command for keyword in shutdown_keywords):
        response = "Shutting down. Goodbye!"
        speak_text(response)
        return False  # Indicate that we should stop listening
    elif any(keyword in command for keyword in how_are_you_keywords):
        response = random.choice(casual_responses)
    elif any(keyword in command for keyword in greeting_keywords):
        response = "Hello! How can I assist you today?"
    elif any(keyword in command for keyword in thanks_keywords):
        response = "You're welcome!"
    else:
        response = "Sorry, I didn't understand that."
    
    print(response)
    speak_text(response)
    return True  # Indicate that we should continue listening

def main():
    while True:
        command = recognize_speech_from_mic()
        print("You said:", command)
        if not process_command(command):
            break

if __name__ == "__main__":
    main()
