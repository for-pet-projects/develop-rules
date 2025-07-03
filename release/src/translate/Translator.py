from release.src.utils.Manifest import Manifest
from release.src.utils.Paths import ProjectPath

from release.src.translate.ClientAPi import ApiClient
from release.src.translate.Markdown_file import MarkdownFileTranslator
from release.src.utils.Print import print_status

class Translator:
    def __init__(self, manifest: Manifest, ppath : ProjectPath):
        self.manifest   = manifest
        self.ppath      = ppath

        self.target_lang = manifest.language.upper()

        self.client         = ApiClient()
        self.md_translator  = MarkdownFileTranslator(self.client)

    def translate(self):
        if self.target_lang == "EN":
            print_status("INF", "Translation skipped (language is EN)")
            return

        for name in ["wiki", "templates"]:
            dir_path = self.ppath.temp_dir / name
            if not dir_path.exists():
                print_status("WRN", f"Missing directory for translation: {dir_path}")
                continue

            for path in dir_path.rglob("*.md"):
                print_status("TRN", f"Translating: {path}")
                try:
                    self.md_translator.translate_file(path, target_lang=self.target_lang)
                except Exception as e:
                    print_status("ERR", f"Failed to translate {path}: {e}")