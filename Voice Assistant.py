import streamlit as st
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import threading  # <-- Import threading here

# Initialize speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)

# Vibrant CSS with Animations
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Pacifico&display=swap');

        body {
            background: linear-gradient(120deg, #ff9a9e, #fad0c4, #fad0c4);
            font-family: 'Orbitron', sans-serif;
            color: white;
            animation: backgroundShift 15s ease infinite;
        }
            
        .stApp {
            background: url('https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExczg3cHM4ZGk3cjcyb3Vzc3l2dmtpOGx0OW51M3FlOGE5M3FranNxYSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/usm8WOpsYdzb9yguxj/giphy.gif') no-repeat center center fixed;
            background-size: cover;
        }


        @keyframes backgroundShift {
            0% {background-position: 0%;}
            50% {background-position: 100%;}
            100% {background-position: 0%;}
        }

        .main {
            background: linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0.05));
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 0 30px rgba(255,255,255,0.3);
            animation: pulse 4s infinite;
        }

        @keyframes pulse {
            0% {box-shadow: 0 0 15px #00f2fe;}
            50% {box-shadow: 0 0 30px #ff6a00;}
            100% {box-shadow: 0 0 15px #00f2fe;}
        }

        .title {
            font-family: 'Pacifico', cursive;
            font-size: 3rem;
            text-align: center;
            background: linear-gradient(90deg, #ff6a00, #ee0979, #00f2fe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradient 5s ease infinite;
        }

        @keyframes gradient {
            0% {background-position: 0%;}
            50% {background-position: 100%;}
            100% {background-position: 0%;}
        }

        .button {
            background: linear-gradient(90deg, #00c6ff, #0072ff);
            border: none;
            color: white;
            padding: 0.9rem 1.8rem;
            font-size: 1.2rem;
            font-weight: bold;
            border-radius: 10px;
            text-align: center;
            cursor: pointer;
            margin: 1rem auto;
            display: block;
            box-shadow: 0 0 20px #00f2fe;
            transition: all 0.4s ease;
            animation: float 3s ease-in-out infinite;
        }

        .button:hover {
            background: linear-gradient(90deg, #f7971e, #ffd200);
            box-shadow: 0 0 30px #ffd200;
            transform: scale(1.1);
        }

        @keyframes float {
            0% {transform: translateY(0px);}
            50% {transform: translateY(-5px);}
            100% {transform: translateY(0px);}
        }

        .response {
            background: rgba(0,0,0,0.4);
            padding: 1rem;
            border-radius: 15px;
            margin-top: 1rem;
            font-size: 1.1rem;
            color: #fff;
            text-shadow: 1px 1px 3px #000;
            animation: fadeIn 2s ease;
        }

        @keyframes fadeIn {
            from {opacity: 0;}
            to {opacity: 1;}
        }

        .footer {
            text-align: center;
            color: #fff;
            font-size: 0.9rem;
            margin-top: 2rem;
            font-style: italic;
            animation: fadeIn 4s ease;
        }
    </style>
""", unsafe_allow_html=True)

# Function to speak text asynchronously
def engine_talk(text):
    def speak():
        engine.say(text)
        engine.runAndWait()
    t = threading.Thread(target=speak)
    t.start()
    return text

# Function to capture voice command
def get_command():
    listener = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.info("🎙️ Listening...")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            command = listener.recognize_google(voice).lower()
            return command.strip()
    except Exception as e:
        st.error(f"Error: {e}")
        return ""


# Streamlit UI
st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown('<h1 class="title">🌟 AuraTalk </h1>', unsafe_allow_html=True)

if st.button("🎙️ Start Listening", key="listen_button", use_container_width=True):
    command = get_command()
    if command:
        st.success(f"✅ You said: **{command}**")
        if 'play' in command:
            song = command.replace('play', '').strip()
            response = f"🎵 Playing {song}"
            pywhatkit.playonyt(song)
        elif 'time' in command:
            response = '🕰️ The current time is ' + datetime.datetime.now().strftime('%I:%M %p')
        elif 'who is' in command:
            name = command.replace('who is', '').strip()
            try:
               response = wikipedia.summary(name, sentences=2)
            except wikipedia.exceptions.DisambiguationError as e:
               options = e.options[:5]  # Show top 5 options
               response = f"⚠️ Multiple results found for '{name}': {', '.join(options)}. Please be more specific."
            except wikipedia.exceptions.PageError:
               response = f"❌ Could not find information about '{name}'."
            except Exception as e:
               response = f"❌ Error: {str(e)}"
        elif 'joke' in command:
            response = pyjokes.get_joke()
        elif 'stop' in command:
            response = "👋 Goodbye!"
            engine_talk(response)
            st.stop()
        else:
            response = "🤷‍♂️ I could not understand you properly."
    else:
        response = "⚠️ I did not catch that. Please speak again."

    st.markdown(f'<div class="response">{response}</div>', unsafe_allow_html=True)
    engine_talk(response)

st.markdown('<p class="footer">✨ Made with 💙 in Python + Streamlit 🚀</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
