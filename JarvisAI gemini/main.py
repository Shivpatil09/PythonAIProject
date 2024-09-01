import datetime
import webbrowser
import speech_recognition as sr
import win32com.client
import os
from config import apikey
import google.generativeai as genai

# Initialize the text-to-speech engine
speaker = win32com.client.Dispatch("SAPI.SpVoice")

# Initialize chat history
chatstr = ""

# Function to generate AI response and save to a file
def generate_ai_response(prompt):
    try:
        genai.configure(api_key=apikey)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash")
        response = model.generate_content([prompt])

        response_text = response.text
        print(response_text)

        # Prepare the filename based on the prompt
        prompt_summary = prompt.replace(' ', '_')[
                         :50]  # Replace spaces and limit length
        filename = f"Openai/{prompt_summary}.txt"

        # Create directory if it doesn't exist
        os.makedirs("Openai", exist_ok=True)

        with open(filename, "w") as file:
            file.write(
                f"GenAi response for prompt: {prompt}\n")
            file.write("**********************\n\n")
            file.write(response_text)
    except Exception as e:
        print(f"Error generating AI response: {e}")


# Function to convert text to speech
def say(text):
    speaker.Speak(text)


# Function to capture voice command and convert to text
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio,
                                       language="en-in")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            say("Sorry, I didn't catch that. Could you please repeat?")
            return None
        except sr.RequestError as e:
            say("Sorry, I'm having trouble connecting to the speech recognition service.")
            return None


# Main function to handle commands
def handle_command(query):
    if query is None:
        return

    query = query.lower()

    # List of sites to open
    sites = {
        "youtube": "https://youtube.com",
        "google": "https://google.com",
        "wikipedia": "https://wikipedia.com",
        "zoro": "https://zorotv.com",
        "hd1": "https://hd1.to",
    }

    # List of music files to play
    musics = {
        "arms around you": "C:/A-xe-12/shiv/BRAND/XXXTENTACION & Lil Pump - Arms Around You.mp3",
        "way down we go": "C:/A-xe-12/shiv/BRAND/KALEO-Way-Down-We-Go-Official-Music-Video_0-7IHOXkiV8.mp3",
    }

    # Open websites
    for site in sites:
        if site in query:
            say(f"Opening {site}")
            webbrowser.open(sites[site])
            return

    # Play music
    if "open music" in query:
        for music in musics:
            if music in query:
                say(f"Playing {music}")
                os.startfile(musics[music])
                return

    # Provide current time
    if "the time" in query:
        current_time = datetime.datetime.now().strftime(
            "%H:%M:%S")
        say(f"Sir, the time is {current_time}")
        return

    # Generate AI response
    if "using artificial intelligence" in query:
        generate_ai_response(prompt=query)
        return

    # Stop listening
    if "stop listening" in query:
        say("Ok sir. I have stopped listening. In case you need me, you know where to find me. Jarvis out.")
        exit()

    # Reset chat
    if "reset chat" in query:
        global chatstr
        chatstr = ""
        say("Chat history has been reset.")
        return

    # Default case: handle unknown command
    say("I'm not sure how to help with that.")


# Main loop
if __name__ == "__main__":
    while True:
        print("Listening...")
        user_query = take_command()
        handle_command(user_query)
