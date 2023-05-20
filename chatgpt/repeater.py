from moviepy.editor import VideoFileClip, concatenate
from pydub import AudioSegment


def repeat_content(video_path, audio_path, repetitions):
    # Load the video clip
    video_clip = VideoFileClip(video_path)

    # Load the audio clip
    audio_clip = AudioSegment.from_file(audio_path)

    # Repeat the audio clip
    repeated_audio = audio_clip * repetitions

    # Set the audio of the video clip
    video_clip = video_clip.set_audio(repeated_audio)

    # Concatenate video clips
    final_video = concatenate([video_clip] * repetitions)

    # Export the final video
    final_video.write_videofile('output.mp4', codec='libx264')

    print("Content created successfully.")


# Example usage
video_path = 'input.mp4'
audio_path = 'audio.mp3'
repetitions = 5

# Create content by repeating audio and video
repeat_content(video_path, audio_path, repetitions)
