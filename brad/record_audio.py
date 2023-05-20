import sounddevice as sd
import wave


def record_audio():
    # Define the sample rate
    sample_rate = 44100

    # Define the number of channels
    channels = 2

    # Define the duration of the recording
    duration = 5

    # Create a new wav file
    wav_file = wave.open("recording.wav", "wb")

    # Set the sample rate and number of channels
    wav_file.setparams((2, channels, sample_rate, 'NONE', 'not compressed'))

    # Start recording
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels)

    # Wait for the recording to finish
    sd.wait()

    # Write the recording to the wav file
    wav_file.writeframes(recording)

    # Close the wav file
    wav_file.close()
