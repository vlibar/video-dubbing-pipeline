
import os
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)

class VideoDownloader:
    def __init__(self, video_url, video_path):
        self.video_url = video_url
        self.video_path = video_path

    def download_video(self):
        if not os.path.exists(self.video_path):
            logging.info(f"Downloading video from {self.video_url}")
            os.system(f"gdown {self.video_url} -O {self.video_path}")
        else:
            logging.info(f"File {self.video_path} already exists.")
