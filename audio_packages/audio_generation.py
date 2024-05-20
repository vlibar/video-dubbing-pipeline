
import logging
import torch
from melo.api import TTS
from pydub import AudioSegment
from openvoice import se_extractor
from openvoice.api import ToneColorConverter

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)

class AudioGenerator:
    def __init__(self, tts_model_name, tts_checkpoint_dir):
        self.tts_model_name = tts_model_name
        self.tts_checkpoint_dir = tts_checkpoint_dir
        self.tts = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def load_tts_model(self):
        logging.info("Loading TTS model.")
        self.tts = TTS(language=self.tts_model_name, device=self.device)
        logging.info("TTS model loaded successfully.")
    
    def load_tone_converter(self):
        logging.info("Loading tone converter.")
        checkpoints_dir = self.tts_checkpoint_dir
        tone_color_converter = ToneColorConverter(f'{checkpoints_dir}/converter/config.json', device=self.device)
        tone_color_converter.load_ckpt(f'{checkpoints_dir}/converter/checkpoint.pth')
        source_se = torch.load(f'{checkpoints_dir}/base_speakers/ses/en-newest.pth').to(self.device)
        return tone_color_converter, source_se
      
    def tone_convertion(self, tone_color_converter, source_se, speaker_wav_path, output_audio_path):
        vad_flg = False if torch.cuda.is_available() else True
        target_se, audio_name = se_extractor.get_se(speaker_wav_path,
                                                    tone_color_converter,
                                                    vad=vad_flg)
        tone_color_converter.convert(audio_src_path='tmp.wav',
                                     src_se=source_se,
                                     tgt_se=target_se,
                                     output_path=output_audio_path)

    def generate_audio_from_text(self, text, speaker_wav_path, output_audio_path, speed=0.9):
        if not self.tts:
            logging.error("TTS model is not loaded.")
            return
        logging.info("Generating audio from text.")
        self.tts.tts_to_file(text, 0, 'tmp.wav', speed=speed)

        tone_color_converter, source_se = self.load_tone_converter()
        self.tone_convertion(tone_color_converter, source_se, speaker_wav_path, output_audio_path)
        logging.info(f"Audio generated and saved to {output_audio_path}")
