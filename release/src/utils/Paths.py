from pathlib import Path

class ProjectPath():
    def __init__(self, root_dir: str | Path):
        self.root_dir      = Path(root_dir)
        self.release_dir   = self.root_dir / "release"
        self.output_dir    = self.root_dir / "output"
        self.build_dir     = self.root_dir / "build"
        self.temp_dir      = self.root_dir / "temp"
