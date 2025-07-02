from pathlib import Path
from release.src.translate.ClientAPi import DeepLApiClient
from release.src.utils.Markdown import extract_translatables, merge_translation

class MarkdownFileTranslator:
    def __init__(self, path: Path, client: DeepLApiClient, target_lang: str):
        self.path = path
        self.client = client
        self.lang = target_lang

    def translate(self) -> str:
        content = self.path.read_text(encoding="utf-8")
        translatables = extract_translatables(content)

        translated_chunks = []
        for chunk in translatables:
            translated = self.client.translate(chunk, self.lang)
            translated_chunks.append(translated)

        return merge_translation(content, translatables, translated_chunks)
