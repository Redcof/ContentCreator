from moviepy.editor import VideoFileClip, AudioFileClip


def merge_audio_video(video_path, audio_path, output_path):
    # Load the video and audio clips
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    # Set the audio of the video clip to the loaded audio clip
    video_clip = video_clip.set_audio(audio_clip)

    # Write the merged video clip to the output file
    video_clip.write_videofile(output_path, codec="libx264")

    print("Video merging complete.")
