# # from brad.record_audio import record_audio
# # from brad.text2audio import text2audio
# from chatgpt.text2audio import text2audio
# from chatgpt.record_audio import record_audio
# from chatgpt.audio2video import audio2video
# from chatgpt.image_download import image_get_pexels
# from chatgpt.images2video import images2video
# from chatgpt.merge_av import merge_audio_video
from config import cfg_from_file, cfg
from content_creator import ContentCreator


# 512gb SSD, M2, 16RAM, Air
# 149900 - 97910 - Store Discount 10%, Cashback 5000 Cashback, debit card 6month emi.

def main():
    cfg_from_file('data_and_config/config.yml')
    # record_audio()
    # text2audio()
    # audio_path = 'output.wav'
    # output_path = 'output.mp4'
    # generate_anim()
    # image_get_pexels()
    # images2video()
    # merge_audio_video()
    cc = ContentCreator(cfg.TOPIC, ".")
    cc.download_images()
    cc.generate_audio_from_quote()
    cc.generate_video_form_images()
    cc.merge_audio_video()
    cc.upload_youtube()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
