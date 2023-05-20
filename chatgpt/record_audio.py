import time

import sounddevice as sd
import scipy.io.wavfile as wav


def record_audio():
    # Set the desired audio parameters
    sample_rate = 44100  # Sample rate in Hz
    duration = 21  # Duration of the recording in seconds

    print("Prepare for recording in 5 seconds")
    time.sleep(5.)
    # Record audio
    print("Recording audio for {} seconds...".format(duration))
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()  # Wait until recording is finished

    # Save the recorded audio as a WAV file
    output_file = "recorded_audio_{}sec.wav".format(duration)
    wav.write(output_file, sample_rate, audio)

    print("Audio saved as", output_file)
