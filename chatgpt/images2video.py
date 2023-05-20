import pathlib

import cv2
import os


def images2video(image_directory, output_file, duration_sec, fps, frame_width, frame_height):
    # Get the list of image files in the directory
    image_files = sorted([os.path.join(image_directory, f) for f in os.listdir(image_directory) if f.endswith(".jpg")])

    # Create a VideoWriter object
    video_writer = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*"mp4v"), fps, (frame_width, frame_height))

    # Iterate over the image files and write frames to the video
    for i in range(1, duration_sec + 1):
        # select image
        idx = (i + 1) % len(image_files)
        image_path = image_files[idx]
        frame = cv2.imread(image_path)

        # Resize the frame to the desired dimensions
        frame = cv2.resize(frame, (frame_width, frame_height))
        for frame_idx in range(fps):
            # Write the frame to the video
            video_writer.write(frame)
    # Release the video writer and close the video file
    video_writer.release()

    print("Video generation complete.")


import cv2
import numpy as np


def fit_image_to_canvas(image, canvas_width, canvas_height, background=255):
    # Get the dimensions of the image
    image_height, image_width = image.shape[:2]

    # Calculate the aspect ratio of the image
    image_aspect_ratio = image_width / float(image_height)

    # Calculate the aspect ratio of the canvas
    canvas_aspect_ratio = canvas_width / float(canvas_height)

    # Calculate the new dimensions of the image to fit the canvas
    if canvas_aspect_ratio > image_aspect_ratio:
        new_width = canvas_height * image_aspect_ratio
        new_height = canvas_height
    else:
        new_width = canvas_width
        new_height = canvas_width / image_aspect_ratio

    # Resize the image to the new dimensions
    resized_image = cv2.resize(image, (int(new_width), int(new_height)))

    # Create a blank canvas of the specified size
    canvas = np.zeros((int(canvas_height), int(canvas_width), 3), dtype=np.uint8)
    canvas[:, :, :] = background

    # Calculate the position to paste the resized image on the canvas
    x = int((canvas_width - new_width) / 2)
    y = int((canvas_height - new_height) / 2)

    # Paste the resized image onto the canvas
    canvas[y:y + int(new_height), x:x + int(new_width)] = resized_image

    return canvas


def generate_resized_image(image_file, frame_width, frame_height):
    img = cv2.imread(image_file)
    img = fit_image_to_canvas(img, frame_width, frame_height, background=255)
    image_file_path = pathlib.Path(image_file)
    filename = str(image_file_path.name)
    parent_dir = image_file_path.parents[0]
    os.makedirs(parent_dir / "resize", exist_ok=True)
    newfile = str(parent_dir / "resize" / "resize{}".format(filename))
    cv2.imwrite(newfile, img)
    return newfile


def image2view2(image_directory, output_file, duration_sec, fps, frame_width, frame_height):
    from moviepy.editor import ImageSequenceClip

    # List of image file paths
    # Get the list of image files in the directory
    image_files = list(map(lambda file: generate_resized_image(file, frame_width, frame_height),
                           [os.path.join(
                               image_directory, f) for f in os.listdir(image_directory) if f.endswith(".jpg")]))

    # Create the image sequence clip
    durations_per_image = [duration_sec / len(image_files)] * len(image_files)
    video_clip = ImageSequenceClip(image_files, fps=fps, durations=durations_per_image)

    # Set the desired frame rate
    video_clip = video_clip.set_fps(fps)

    # Specify the output file name and codec
    codec = 'libx264'

    # Write the video to the output file
    video_clip.write_videofile(output_file, codec=codec)

    print(f"Video created and saved as '{output_file}'")
