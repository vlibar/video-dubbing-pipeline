
import logging
import torch
import whisperx

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)

class TranscriptionModel:
    def __init__(self, model_size):
        self.model_size = model_size
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def load_model(self):
        logging.info("Loading ASR model.")
        compute_type = 'float16' if self.device == 'cuda' else 'int8'
        try:
            self.model = whisperx.load_model(self.model_size, device=self.device, compute_type=compute_type)
            logging.info("Model loaded successfully.")
        except Exception as e:
            logging.error("Error loading Whisper model: %s", e)
    
    def align_transcription(self, audio_path, result):
        if not result:
            logging.error("No transcription result to align.")
            return {}
        try:
            model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=self.device)
            result_aligned = whisperx.align(result["segments"], model_a, metadata, audio_path, device=self.device)
            return result_aligned
        except Exception as e:
            logging.error("Error aligning transcription: %s", e)
            return {}

    def transcribe_audio(self, audio_path, batch_size=16):
        if not self.model:
            logging.error("Model is not loaded.")
            return {}
        try:
            logging.info(f"Transcribing audio file {audio_path}")
            result = self.model.transcribe(audio_path, batch_size=batch_size)
            result = self.align_transcription(audio_path, result)

            logging.info("Transcription completed successfully")
            return result
        except Exception as e:
            logging.error("Error transcribing audio: %s", e)
            return {}
