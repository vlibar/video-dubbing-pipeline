
import logging
from moviepy.editor import VideoFileClip, AudioFileClip

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)

class VideoReplacer:
    def __init__(self, video_path):
        self.video_path = video_path

    def replace_audio_in_video(self, audio_path, output_video_path):
        try:
            logging.info("Replacing audio in the video.")
            video = VideoFileClip(self.video_path).without_audio()
            audio = AudioFileClip(audio_path)
            new_video = video.set_audio(audio)
            new_video.write_videofile(output_video_path, codec='libx264', audio_codec='aac', verbose=False)
            logging.info("Audio replaced successfully.")
        except Exception as e:
            logging.error(f"Failed to replace audio: {e}")
