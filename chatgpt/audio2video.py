from moviepy.editor import AudioFileClip, VideoClip


def audio2video(audio_path, output_path):
    # Load the audio clip
    audio = AudioFileClip(audio_path)

    # Create a blank video clip with the same duration as the audio
    video = VideoClip(duration=audio.duration)

    # Set the audio as the audio track of the video clip
    video = video.set_audio(audio)

    # Set the video codec and write the video file
    video.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=24)

# # Specify the path to your audio clip and the desired output path for the video
# audio_path = 'path/to/audio.wav'
# output_path = 'path/to/output.mp4'
#
# # Generate the video
# generate_video(audio_path, output_path)
