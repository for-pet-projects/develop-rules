from pathlib import Path

from release.src.utils.Manifest import Manifest
from release.src.utils.Paths import ProjectPath

from release.src.translate.ClientAPi import DeepLApiClient
from release.src.translate.Markdown_file import MarkdownFileTranslator
from release.src.utils.Print import print_status

class Translator:
    def __init__(self, manifest: Manifest, ppath : ProjectPath):
        self.manifest = manifest
        self.ppath = ppath

        self.target_lang = manifest.language.upper()

        self.client = DeepLApiClient(api_key="DUMMY_API_KEY")

    def translate(self):
        pass