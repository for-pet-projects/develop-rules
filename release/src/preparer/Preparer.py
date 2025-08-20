from pathlib import Path
import shutil

from release.src.utils.Paths import ProjectPath
from release.src.utils.Manifest import Manifest

from release.src.preparer.Units import UnitPreparer, WikiPreparer

class ReleasePreparer:
    def __init__(self, manifest: Manifest, ppath : ProjectPath):
        self.manifest = manifest
        self.ppath = ppath

        self.units = [
            WikiPreparer("wiki", self.manifest, self.ppath),
            UnitPreparer("templates", self.manifest, self.ppath),
        ]

    def prepare(self):
        if Path(self.ppath.temp_dir).exists():
            shutil.rmtree(self.ppath.temp_dir)
        for every in self.units:
            every.prepare()

