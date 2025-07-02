from pathlib import Path
import shutil

from release.src.utils.Paths import ProjectPath
from release.src.utils.Manifest import Manifest
from release.src.preparer.ListLoader import ListLoader

from release.src.utils.Print import print_status

class ReleasePreparer:
    def __init__(self, manifest: Manifest, ppath : ProjectPath):
        self.manifest = manifest
        self.ppath = ppath

        self.git_client = manifest.git_client

        self.units = [
            UnitPreparer(name, self.git_client, self.ppath)
            for name in ["wiki", "templates"]
        ]

    def prepare(self):
        for every in self.units:
            every.prepare()

class UnitPreparer:
    def __init__(self, name : str, git_client : str, ppath : ProjectPath):
        self.ppath = ppath
        
        self.source_dir = self.ppath.root_dir
        self.dest_dir   = self.ppath.temp_dir / name
        self.list_path  = self.ppath.release_dir \
            / "lists" / git_client / (name + ".list")

        self.list_loader = ListLoader(self.source_dir, self.dest_dir)

    def prepare(self):
        self._ensure_clean(self.dest_dir)
        self._copy_from_to(self.list_loader.load(self.list_path))
        
    def _ensure_clean(self, path: Path):
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)

    def _copy_from_to(self, pairs: list[tuple[Path, Path]]):
        for source, dest in pairs:
            if not source.exists():
                print_status("WRN", f"Skip, not found: {source}")
                continue

            try:
                if source.is_dir():
                    shutil.copytree(source, dest, dirs_exist_ok=True)
                    print_status("OK", f"Copy DIR  {source} → {dest}")
                else:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, dest)
                    print_status("OK", f"Copy FILE {source} → {dest}")
            except Exception as e:
                print_status("ERR", f"Failed to copy {source} → {dest}: {e}")



