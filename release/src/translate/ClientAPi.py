import requests
import time
import random
import json
from urllib.parse import quote
from release.src.utils.Print import print_status

class ApiClient:
    
    def __init__(self, api_key: str | None = None):
        pass#$self.translator = DeepLWebTranslator()

    def translate(self, text: str, target_lang: str) -> str:
        try:
            translated = text#self.translator.translate(text, target_lang)
            if translated == text:
                print_status("WRN", "Translation returned original text (possible failure)")
            return translated
        except Exception as e:
            print_status("ERR", f"Translation failed: {str(e)}")
            return text  # Fallback to original text on failure