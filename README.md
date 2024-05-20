# Video Dubbing Pipeline

This project provides a comprehensive pipeline for video dubbing. It includes downloading a video, extracting audio, transcribing and translating the audio, generating new audio using text-to-speech, and replacing the original audio in the video with the generated audio.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Classes and Functions](#classes-and-functions)
- [Example](#example)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/video-dubbing-pipeline.git
    cd video-dubbing-pipeline
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the Pipeline

1. Ensure you have all the necessary files in the project directory:
    - `video_download.py`
    - `audio_extractor.py`
    - `video_replacer.py`
    - `transcription_model.py`
    - `text_translator.py`
    - `audio_processor_utils.py`
    - `audio_generation.py`
    - `dubbing_pipeline.py`
    - `main.py`

2. Modify the `main.py` file to set the correct paths and model names.

3. Run the main script:

    ```bash
    python main.py
    ```

### Classes and Functions

#### `VideoDownloader`

- `__init__(self, video_url, video_path)`
- `download_video(self)`

#### `AudioExtractor`

- `__init__(self, video_path, audio_output_path)`
- `extract_audio_from_video(self)`

#### `VideoReplacer`

- `__init__(self, video_path)`
- `replace_audio_in_video(self, audio_path, output_video_path)`

#### `TranscriptionModel`

- `__init__(self, model_name)`
- `load_model(self)`
- `transcribe_audio(self, audio_path, batch_size=16)`
- `align_transcription(self, audio_path, result)`

#### `TextTranslator`

- `__init__(self, tokenizer_name, model_name)`
- `load_model(self)`
- `translate_text(self, source_text)`

#### `AudioProcessorUtils`

- `mute_voice(audio_segment, mute_start, mute_end, reduction_db=20, margin=50, fade_in_ms=100, fade_out_ms=100)`
- `extract_segments(audio_segment, segments)`
- `synchronize_audio(russian_audio, english_audio, russian_segments, english_segments)`

#### `AudioGenerator`

- `__init__(self, tts_model_name, tts_checkpoint_dir)`
- `load_tts_model(self)`
- `generate_audio_from_text(self, text, output_audio_path)`
- `overlay_audio(self, base_audio_path, overlay_audio_path, output_path)`

#### `TextSegmenter`

- `__init__(self, translated_text_raw, translated_list)`
- `find_best_match(self, word, segments, used_indices)`
- `segment_text(self)`

#### `DubbingPipeline`

- `__init__(self, video_url, video_path, audio_output_path, new_audio_path, output_video_path, model_name, checkpoints_dir)`
- `run_pipeline(self)`

### Example

```python
from dubbing_pipeline import DubbingPipeline
from IPython.display import display

def main():
    video_url = 'https://example.com/video.mp4'
    video_path = 'video.mp4'
    audio_output_path = 'audio_output.wav'
    new_audio_path = 'new_audio.wav'
    output_video_path = 'dubbed_video.mp4'
    model_name = "large-v2"
    checkpoints_dir = "checkpoints_v2_0417"

    dubbing_pipeline = DubbingPipeline(video_url, video_path, audio_output_path, new_audio_path, output_video_path, model_name, checkpoints_dir)
    final_audio = dubbing_pipeline.run_pipeline()
    display(final_audio)

if __name__ == "__main__":
    main()
