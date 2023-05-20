import json
import pathlib
import random

from chatgpt.image_download import image_get_pexels
from chatgpt.images2video import images2video, image2view2
from chatgpt.merge_av import merge_audio_video
from chatgpt.text2audio import text2audio, multilangTTS
from chatgpt.translator import google_translate_text
from chatgpt.upload_youtube import youtube_upload
from config import cfg, mkdir_p
import datetime
import dateutil.tz


class QuoteInfo:

    def __init__(self, quote, author, credit, source):
        self.quote = quote
        self.author = author
        self.credit = credit
        self.source = source


WORD_PER_MINUTE = 130


class ContentCreator:

    def __init__(self, project_name, project_loc):
        now = datetime.datetime.now(dateutil.tz.tzlocal())
        timestamp = str(now.strftime('%Y_%m_%d_%H_%M_%S'))
        self.output_dir = pathlib.Path(project_loc) / project_name
        self.temp_dir = pathlib.Path(self.output_dir / "temp")
        self.image_dir = self.temp_dir / "images"
        self.temp_audio_path = self.temp_dir / 'output_audio_{}.wav'.format(timestamp)
        self.temp_video_path = self.temp_dir / 'output_video_{}.mp4'.format(timestamp)
        mkdir_p(str(self.output_dir))
        mkdir_p(str(self.image_dir))

    @staticmethod
    def get_a_quote(quote_length=-1) -> str:
        """
        This function returns a random quote form a kaggle dataset available here:
        https://www.kaggle.com/datasets/akmittal/quotes-dataset
        """
        # Open the JSON file

        with open('data_and_config/quotes.json', encoding='utf-8') as file:
            # Read the contents of the file
            data = json.load(file)
            max_ = len(data)
            if quote_length == -1:
                quote_info = data[random.randint(0, max_)]
                return quote_info['Quote']
            else:
                quote = "\n\n\n"
                lent = 0
                while len(quote) - 3 < quote_length:
                    quote_info = data[random.randint(0, max_)]

                    quote = "{}{}\n\n\n".format(quote, quote_info['Quote'])
                    lent = len(quote) - 3
                return "{}\n\n\n".format(quote)

    @staticmethod
    def select_voice():
        return dict(male=0, female=1)[cfg.AUDIO.VOICE]

    @staticmethod
    def get_wpm():
        return WORD_PER_MINUTE * cfg.AUDIO.SPEED_X

    def generate_audio_from_text(self, text, language="en"):
        output = str(self.temp_audio_path)
        if language == "en":
            required_wpm = self.get_wpm()
            voice_idx = self.select_voice()
            text2audio(text, voice_idx, required_wpm, output)
        else:
            multilangTTS(text, lang=language, output=output)

    def download_images(self):
        image_get_pexels(cfg.VIDEO.IMAGE_QUERY, cfg.VIDEO.IMAGE_COUNT, str(self.image_dir))

    @staticmethod
    def get_dimension():
        """
        From aspect ratio and resolution we can calculate frame width and height.

        A 480p image has 480 columns of pixels.
        Actual Resolution	Resolution Conventional Name	Name with Respect to Quality
        720×480	             480p	                        SD
        1280×720	         720p	                        HD
        1920×1080	         1080p	                        Full HD (FHD)
        2560×1440	         1440p	                        Quad HD (QHD), WQHD
        3840×2160	         2160p	                        Ultra HD (UHD), 4K
        7680×4320	         4320p	                        8K UHD, 8K
        :return: 
        """
        aspect_ratio = dict(shorts=(9, 16), video=(16, 9))[cfg.TYPE]
        frame_height = {
            "480p": 480,
            "720p": 720,
            "1080p": 1080,
            "2K": 1440,
            "4K": 2160,
            "8K": 4320,
        }[cfg.RESOLUTION]
        w, h = aspect_ratio
        frame_width = (w / h) * frame_height
        return frame_width, frame_height

    def generate_video_form_images(self):
        duration_sec = cfg.LENGTH_IN_MINUTE
        frame_width, frame_height = self.get_dimension()
        image_directory = str(self.image_dir)
        output_file = str(self.temp_video_path)
        image2view2(image_directory, output_file, duration_sec=duration_sec, fps=30, frame_width=frame_width,
                    frame_height=frame_width)

    def merge_audio_video(self):
        video_path = str(self.temp_video_path)
        audio_path = str(self.temp_audio_path)
        merge_audio_video(video_path, audio_path, video_path)
        print("Collect video form:", str(self.temp_video_path))

    def get_quote_length(self):
        required_wpm = self.get_wpm()
        content_length_min = cfg.LENGTH_IN_MINUTE
        quote_length = content_length_min * required_wpm
        return quote_length

    def upload_youtube(self):
        video_path = str(self.temp_video_path)
        hash_tags = list(map(lambda x: x.strip(), cfg.VIDEO.HASH_TAGS.split(",")))
        youtube_upload(video_path, cfg.VIDEO.TITLE, cfg.VIDEO.DESCRIPTION, hash_tags)

    def generate_audio_from_quote(self):
        language = cfg.LANGUAGE
        quote_length = self.get_quote_length()
        quote = self.get_a_quote(quote_length)
        print("Quote:", quote)
        if language != "en":
            quote = google_translate_text(quote, target_language=language)
            print("Translated quote:", quote)
        self.generate_audio_from_text(quote, language=language)

