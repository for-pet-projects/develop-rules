from release.src.utils.Manifest import Manifest
from release.src.utils.Paths import ProjectPath

from release.src.utils.Print import print_status
from release.src.builder.Scriptgen import BuildScriptGenerator

class ReleaseBuilder:
    def __init__(self, manifest: Manifest, ppath : ProjectPath):
        self.manifest = manifest
        self.ppath = ppath

    def build(self):
        print_status("INF", "Building release script")
        scriptgen = BuildScriptGenerator(self.manifest)
        scriptgen.generate()
