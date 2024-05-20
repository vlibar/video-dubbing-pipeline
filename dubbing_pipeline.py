
from video_packages.video_download import VideoDownloader
from video_packages.video_replacer import VideoReplacer
from text_packages.segment_matcher import TextSegmenter
from text_packages.transcription_model import TranscriptionModel
from text_packages.text_translator import TextTranslator
from audio_packages.audio_processor_utils import AudioProcessorUtils
from audio_packages.audio_generation import AudioGenerator
from audio_packages.audio_extractor import AudioExtractor
from pydub import AudioSegment

class DubbingPipeline:
    def __init__(self, video_url, video_path, audio_output_path, new_audio_path, output_video_path, checkpoints_dir, translation_model, tts_model_name, transcription_model_size):
        self.video_downloader = VideoDownloader(video_url, video_path)
        self.audio_extractor = AudioExtractor(video_path, audio_output_path)
        self.transcription_model = TranscriptionModel(transcription_model_size)
        self.text_translator = TextTranslator(tokenizer_name=translation_model, model_name=translation_model)
        self.audio_generation = AudioGenerator(tts_model_name=tts_model_name, tts_checkpoint_dir=checkpoints_dir)
        self.audio_output_path = audio_output_path
        self.new_audio_path = new_audio_path
        self.output_video_path = output_video_path
        self.video_replacer = VideoReplacer(video_path)
        self.segmenter = TextSegmenter()

    def run_pipeline(self):
        self.video_downloader.download_video()
        self.audio_extractor.extract_audio_from_video()

        self.transcription_model.load_model()
        original_text_raw = self.transcription_model.transcribe_audio(self.audio_output_path)
        original_text = [segment['text'].strip() for segment in original_text_raw['segments']]
      
        self.text_translator.load_model()
        english_text_list = self.text_translator.translate_text(original_text)
        english_text = ' '.join(english_text_list)

        self.audio_generation.load_tts_model()
        new_audio = self.audio_generation.generate_audio_from_text(english_text, self.audio_output_path, self.new_audio_path)

        translated_text_raw = self.transcription_model.transcribe_audio(self.new_audio_path)
        segmented_text = self.segmenter.segment_text(translated_text_raw, english_text_list)

        russian_audio = AudioSegment.from_file(self.audio_output_path)
        english_audio = AudioSegment.from_file(self.new_audio_path)

        russian_segments = original_text_raw['segments']
        english_segments = segmented_text

        synchronized_audio = AudioProcessorUtils.synchronize_audio(russian_audio, english_audio, russian_segments, english_segments)
        synchronized_audio.export("synchronized_audio.wav", format="wav")

        self.video_replacer.replace_audio_in_video("synchronized_audio.wav", self.output_video_path)
        return Audio('synchronized_audio.wav')
