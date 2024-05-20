from dubbing_pipeline import DubbingPipeline

def main():
    video_url = 'https://drive.google.com/uc?id=1jhVicMYcbgLiY43j5GEnybgAIYCc3iQC'
    video_path = 'video_path_here.mp4'
    audio_output_path = 'audio_output.wav'
    new_audio_path = 'new_audio.wav'
    output_video_path = 'dubbed_video.mp4'
    checkpoints_dir = "checkpoints_v2_0417"
    translation_model = "Helsinki-NLP/opus-mt-ru-en"
    tts_model_name = 'EN_NEWEST'
    transcription_model_size='large'

    dubbing_pipeline = DubbingPipeline(video_url, video_path, audio_output_path, new_audio_path, output_video_path, checkpoints_dir, translation_model, tts_model_name, transcription_model_size)
    final_audio = dubbing_pipeline.run_pipeline()

if __name__ == "__main__":
    main()
