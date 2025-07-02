import deepl, os
from release.src.utils.Print import print_status

class DeepLApiClient:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("DEEPL_API_KEY")
        if not self.api_key:
            self.api_key = input("Enter your DeepL API key: ").strip()

        self.translator = deepl.Translator(self.api_key)

    def translate(self, text: str, target_lang: str) -> str:
        print_status("INF", f"Translating via DeepL → {target_lang}")
        try:
            result = self.translator.translate_text(text, target_lang=target_lang)
            return result.text
        except Exception as e:
            print_status("ERR", f"DeepL API error: {e}")
            return text  # fallback: return original text
