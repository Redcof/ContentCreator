import pyttsx3
import librosa


def text2audio():
    # Define the text to be converted to audio
    text = "Don't let fear hold you back. Take risks, step outside of your comfort zone, and go after your dreams. " \
           "You are capable of anything you set your mind to. So go out there and make it happen!"

    # Load the voice sample
    voice_sample = librosa.load("recorded_audio_21sec.wav")

    # Create a new Text-to-Speech engine
    engine = pyttsx3.init()

    # Set the voice of the engine
    engine.setProperty('voice', 'english-us')

    # Set the rate of the engine
    engine.setProperty('rate', 150)

    # Convert the text to audio using the voice sample
    engine.say(text, voice_sample=voice_sample)

    # Play the audio
    engine.runAndWait()

    # Close the engine
    engine.stop()
