import cv2
import numpy as np


def generate_anim():
    # Set the dimensions of the animation
    width = 640
    height = 480

    # Set the duration and frames per second (FPS)
    duration = 5  # in seconds
    fps = 30

    # Create a VideoWriter object to save the animation
    output_file = 'color_diffusion_animation.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    # Generate each frame of the animation
    num_frames = duration * fps
    for frame_idx in range(num_frames):
        # Create a blank frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        # Compute the color for the frame based on the frame index
        r = int(255 * (frame_idx / num_frames))
        g = int(255 * (1 - frame_idx / num_frames))
        b = int(255 * (frame_idx / num_frames))

        # Fill the frame with the computed color
        frame[:, :] = (b, g, r)

        # Write the frame to the video file
        video_writer.write(frame)

    # Release the VideoWriter object
    video_writer.release()
