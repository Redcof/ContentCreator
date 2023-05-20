import librosa
import ffmpeg


def audio2video(audiofile, output):
    # Load the audio clip.
    audio_clip = librosa.load(audiofile)

    # Extract the audio features.
    features = librosa.feature.extract_mfcc(audio_clip, n_mfcc=128)

    # Create a video file.
    video_file = ffmpeg.create_video_file(output)

    # Add the audio features to the video file.
    for feature in features:
        video_file.add_audio_feature(feature)

    # Save the video file.
    video_file.save()
