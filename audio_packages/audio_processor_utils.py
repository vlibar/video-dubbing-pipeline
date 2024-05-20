
from pydub import AudioSegment

class AudioProcessorUtils:
    @staticmethod
    def mute_voice(audio_segment, mute_start, mute_end, reduction_db=20, margin=50, fade_in_ms=100, fade_out_ms=100):
        muted_segment = (audio_segment[mute_start - margin:mute_end + margin] - reduction_db).fade_in(fade_in_ms).fade_out(fade_out_ms)
        result_audio = audio_segment[:mute_start - margin] + muted_segment + audio_segment[mute_end + margin:]
        return result_audio

    @staticmethod
    def extract_segments(audio_segment, segments):
        extracted_segments = []
        for segment in segments:
            start = int(segment['start'] * 1000)
            end = int(segment['end'] * 1000)
            extracted_segments.append(audio_segment[start:end])
        return extracted_segments

    @staticmethod
    def synchronize_audio(russian_audio, english_audio, russian_segments, english_segments):
        current_time = 0
        prev_e_end = 0

        for r_segment, e_segment in zip(russian_segments, english_segments):
            r_start = int(r_segment['start'] * 1000)
            r_end = int(r_segment['end'] * 1000)
            e_start = int(e_segment['start'] * 1000)
            e_end = int(e_segment['end'] * 1000)

            russian_audio = AudioProcessorUtils.mute_voice(russian_audio, r_start, r_end)

            e_audio_segment = english_audio[e_start:e_end]
            russian_audio = russian_audio.overlay(e_audio_segment, position=max(r_start, prev_e_end))

            prev_e_end = e_end - e_start + r_start

        return russian_audio
