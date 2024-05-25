
import logging
from difflib import SequenceMatcher

class TextSegmenter:
    def __init__(self):
        self.used_indices = set()
        self.segmented_text = []

    def _prepare_translated_words(self):
        translated_words = [
            sentence[:-1].lower().replace(' - ', '-').split() if sentence[-1] == '.' else
            sentence.lower().replace(' - ', '-').split()
            for sentence in self.translated_list
        ]
        return translated_words

    def find_best_match(self, word, segments, used_indices):
        best_match_index = -1
        best_match_score = -1.0
        for i, segment in enumerate(segments):
            if i in used_indices:
                continue
            first_word = word.strip(",.!?-").lower()
            second_word = segment['word'].strip(",.!?-").lower()
            score = SequenceMatcher(None, first_word, second_word).ratio()
            if score > best_match_score:
                best_match_index = i
                best_match_score = score
        return best_match_index

    def segment_text(self, translated_text_raw, translated_list):
        self.word_segments = translated_text_raw['word_segments']
        self.translated_list = translated_list
        self.translated_words = self._prepare_translated_words()
        word_index = 0

        for sentence in self.translated_words:
            segment = {
                'start': self.word_segments[word_index]['start'],
                'end': 0,
                'text': '',
                'words': []
            }

            for word in sentence:
                match_index = self.find_best_match(word, self.word_segments, self.used_indices)
                if match_index != -1:
                    segment['words'].append(self.word_segments[match_index])
                    word_index = match_index
                    self.used_indices.add(match_index)
                else:
                    segment['words'].append({
                        'word': word,
                        'start': None,
                        'end': None
                    })
            word_index += 1

            segment['end'] = segment['words'][-1]['end']
            segment['text'] = ' '.join([word['word'] for word in segment['words']])
            self.segmented_text.append(segment)

        return self.segmented_text
