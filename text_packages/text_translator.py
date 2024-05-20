
import logging
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)

class TextTranslator:
    def __init__(self, tokenizer_name, model_name):
        self.tokenizer_name = tokenizer_name
        self.model_name = model_name
        self.tokenizer = None
        self.model = None

    def load_model(self):
        try:
            logging.info("Loading translation model.")
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
            self.tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_name)
            logging.info("Model loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading translation model: {e}")

    def translate_text(self, source_text):
        if not self.model or not self.tokenizer:
            logging.error("Model or tokenizer is not loaded.")
            return []
        try:
            logging.info("Translating text.")
            translated_text = []
            inputs = self.tokenizer(source_text, return_tensors="pt", padding=True)
            outputs = self.model.generate(**inputs)
            for sentence in outputs:
                translated_text.append(self.tokenizer.decode(sentence, skip_special_tokens=True))
            logging.info("The text was successfully translated.")
            return translated_text
        except Exception as e:
            logging.error(f"Error translating text: {e}")
            return []