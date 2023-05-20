import cv2
import os

"Don't let fear hold you back. Take risks, step outside of your comfort zone, and go after your dreams. " \
           "You are capable of anything you set your mind to. So go out there and make it happen!"
def images2video():
    # Set the directory containing the input images
    image_directory = "images"

    # Set the output video file name and parameters
    output_file = "output_video.mp4"
    fps = 30
    frame_width = 640
    frame_height = 480
    duration = 10  # sec

    # Get the list of image files in the directory
    image_files = sorted([f for f in os.listdir(image_directory) if f.endswith(".jpg")])

    # Create a VideoWriter object
    video_writer = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*"mp4v"), fps, (frame_width, frame_height))

    # Iterate over the image files and write frames to the video
    for i in range(duration):
        # select image
        image_file = image_files[i % len(image_files)]
        for frame in range(fps):
            # Read the image
            image_path = os.path.join(image_directory, image_file)
            frame = cv2.imread(image_path)

            # Resize the frame to the desired dimensions
            frame = cv2.resize(frame, (frame_width, frame_height))

            # Write the frame to the video
            video_writer.write(frame)
        print(i)
    # Release the video writer and close the video file
    video_writer.release()

    print("Video generation complete.")
