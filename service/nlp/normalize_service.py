import re
import unicodedata


class NormalizeText:
    def __init__(self):
        self.text: str = None

    def get_input(self, text):
        self.text = text
        return self

    def unicode_to_ascii(self):
        self.text = self.text.lower().strip()
        normalized_str = unicodedata.normalize('NFD', self.text)
        self.text = ''.join(c for c in normalized_str if unicodedata.category(c) != "Mn")
        return self

    def add_space_before_special_chars(self):
        self.text = re.sub(r'([.!?])', r' \1', self.text)
        return self

    def remove_non_alpha_characters(self):
        self.text = re.sub(r'[^a-zA-Z.!?]+', ' ', self.text)
        return self

    def remove_extra_whitespaces(self):
        self.text = re.sub(r'\s+', ' ', self.text)
        return self

    def get_text(self):
        return self.text.strip()


def normalize(input_str):
    return (NormalizeText()
            .get_input(input_str)
            .unicode_to_ascii()
            .add_space_before_special_chars()
            .remove_non_alpha_characters()
            .remove_extra_whitespaces().get_text()
            )
