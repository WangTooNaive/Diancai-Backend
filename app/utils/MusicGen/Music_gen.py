from ast import Bytes
from music_generation import MusicGenerator

from transformers import AutoProcessor, MusicgenForConditionalGeneration

class MusicGenGenerator(MusicGenerator):
    def __init__(self) -> None:
        
        self.processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
        self.model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")

    def generate(self, text: str) -> Bytes:
        inputs = self.processor(
            text=[text],
            padding=True,
            return_tensors="pt",
        )
        audio_values = self.model.generate(**inputs, max_new_tokens=256)
        return audio_values