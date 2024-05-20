
import logging
from moviepy.editor import VideoFileClip

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)

class AudioExtractor:
    def __init__(self, video_path, audio_output_path):
        self.video_path = video_path
        self.audio_output_path = audio_output_path

    def extract_audio_from_video(self):
        try:
            logging.info("Extracting audio from video.")
            video = VideoFileClip(self.video_path)
            audio = video.audio
            audio.write_audiofile(self.audio_output_path, codec='pcm_s16le')
            logging.info("Audio extracted successfully.")
        except Exception as e:
            logging.error(f"Failed to extract audio: {e}")
