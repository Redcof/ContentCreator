import gc
import os.path
import pathlib

from moviepy.audio.AudioClip import concatenate_audioclips
from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from pydub import AudioSegment


def prepare_paths(path):
    """This is split multiple paths and automatically filter out wrong paths"""
    if os.path.isfile(path) and path.endswith(".txt"):
        with open(path, "r") as fp:
            paths = fp.readlines()
    else:
        paths = path.split(",")
    path = list(filter(lambda x: os.path.isfile(x), map(lambda x: x.strip(), paths)))
    print("Path collected: {}".format(len(path)))
    return path


def read_videos(video_paths: [str]) -> [VideoFileClip]:
    print("Video loaded {}".format(len(video_paths)))
    return [VideoFileClip(path) for path in video_paths]


def merge_videos(videos: [VideoFileClip]) -> VideoFileClip:
    print("Video concatenated {}".format(len(videos)))
    return concatenate_videoclips(videos)


def read_audios(audio_paths: [str]) -> [AudioFileClip]:
    print("Audio loaded {}".format(len(audio_paths)))
    return [AudioFileClip(path) for path in audio_paths]


def merge_audios(audios: [AudioFileClip]) -> AudioFileClip:
    print("Audio concatenated {}".format(len(audios)))
    return concatenate_audioclips(audios)


def repeat_content(workspace, video_path, audio_path, audio_repetitions, output_video):
    gc.collect()
    # Load the video clip
    video_clip = merge_videos(read_videos(prepare_paths(video_path)))

    # Load the audio clip
    audio_clip = merge_audios(read_audios(prepare_paths(audio_path)))
    # save the repeated audio to a temp file
    new_audio_path = pathlib.Path(workspace)
    new_audio_path = str(new_audio_path / "temp_audio.mp3")
    audio_clip.write_audiofile(new_audio_path)
    print("Temp audio is saved at {}".format(new_audio_path))
    del audio_clip
    gc.collect()

    # Load the audio clip
    audio_segment = AudioSegment.from_file(new_audio_path)
    print("Initial Audio duration(sec): {} to be repeated by {}".format(round(audio_segment.duration_seconds, 0),
                                                                        audio_repetitions))
    # Repeat the audio clip
    if audio_repetitions > 0:
        print("Repeat Audio {} Times".format(audio_repetitions), end="...")
        repeated_audio = audio_segment * (audio_repetitions + 1)
        repeated_audio.export(new_audio_path)
        # collect
        del repeated_audio
        gc.collect()
        # load audio as compatible audio clip
        final_audio_clip = AudioFileClip(new_audio_path)
        print("Done")
    else:
        # load audio as compatible audio clip
        final_audio_clip = AudioFileClip(new_audio_path)

    # read file as audio clip
    audio_duration_sec = final_audio_clip.duration
    video_duration_sec = video_clip.duration
    # video repeat
    vid_repeat = int(audio_duration_sec // video_duration_sec) + 1
    print("Video Duration(sec): {}".format(round(video_duration_sec, 0)))
    print("Audio Duration(sec): {}".format(round(audio_duration_sec, 0)))
    print("Video Repeat Count: {}".format(vid_repeat))
    # Concatenate video clips
    if vid_repeat == (0, 1):
        repeated_vid = video_clip
    else:
        print("Repeat Video {} Times".format(vid_repeat), end="...")
        repeated_vid = concatenate_videoclips([video_clip] * vid_repeat)
        print("Done")
    print("Repeated Video Duration(sec): {}".format(round(repeated_vid.duration, 0)))

    print("Merging video and audio", end="...")
    # Set the audio of the video clip
    final_video = repeated_vid.set_audio(final_audio_clip)
    print("Done")
    fps = 15
    approx_data_kb_per_sec = 45
    approx_frame_writing_rate = 25  # frames/sec
    print("Expected content size: {}GB".format(
        round(((fps * approx_data_kb_per_sec * repeated_vid.duration) / 1024) / 1024), 2)
    )
    print("Expected content length: {}min".format(round(repeated_vid.duration / 60.), 2))
    print("Expected time to create: {}min".format(
        round((fps * repeated_vid.duration / approx_frame_writing_rate) / 60.), 2)
    )
    print("Exporting content...")
    # Export the final video
    final_video.write_videofile(output_video, fps=fps, codec='libx264')

    if os.path.isfile(new_audio_path):
        print("Cleanup...")
        os.remove(new_audio_path)
    print("Content created successfully: '{}'.".format(output_video))

# # Example usage
# video_path = 'input.mp4'
# audio_path = 'audio.mp3'
# repetitions = 5
#
# # Create content by repeating audio and video
# repeat_content(video_path, audio_path, repetitions)
