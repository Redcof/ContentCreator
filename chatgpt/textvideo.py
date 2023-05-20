from moviepy.editor import VideoClip
from moviepy.video.VideoClip import TextClip
from moviepy.video.io.ffmpeg_writer import FFMPEG_VideoWriter

# Define the duration and frames per second (FPS) of the video
duration = 5  # Duration in seconds
fps = 30  # Frames per second


# Create a function that generates frames for the video
def generate_frame(t):
    # Example: Create a frame with a moving text
    txt = f"This is frame {int(t * fps)}"
    return TextClip(txt, fontsize=30, color='white').set_duration(1 / fps)


# Create the video clip
video_clip = VideoClip(generate_frame, duration=duration)

# Specify the output file name and codec
output_file = 'output.mp4'
codec = 'libx264'

# Write the video to the output file
video_clip.write_videofile(output_file, fps=fps, codec=codec)

print(f"Video created and saved as '{output_file}'")
