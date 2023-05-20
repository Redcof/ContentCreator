import pyttsx3
from gtts import gTTS
from playsound import playsound


def text2audio(text, voice_idx, word_per_minute, output, hear=False):
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()

    # Set the voice
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_idx].id)  # Use the first available voice

    # set custom voice
    engine.setProperty('volume', 1.)
    engine.setProperty('rate', word_per_minute)

    # Convert text to speech
    if hear:
        engine.say(text)

    # Save the speech as an audio file
    engine.save_to_file(text, output)

    # Run the engine and wait for speech generation
    engine.runAndWait()

    print("Audio file generated")


def multilangTTS(text, lang, output, slow_speed=False, hear=False):
    # Create a gTTS object and specify the language (Bengali in this case)
    tts = gTTS(text, lang=lang, slow=slow_speed)
    # Save the speech output to an audio file
    tts.save(output)
    if hear:
        playsound(output)
    print("Audio file generated")


if __name__ == '__main__':
    text = "আমি পাইথনে বাংলায় টেক্সট টু স্পিচ প্রোগ্রাম তৈরি করছি।"
    output_file = "output_ben.mp3"
    multilangTTS(text, output=output_file, lang="bn", hear=True)
