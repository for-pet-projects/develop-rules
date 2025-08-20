import sys, signal
from pathlib import Path

def find_repo_root() -> Path:
    path = Path(__file__).resolve()
    while path != path.parent:
        if (path / ".git").exists():
            return path
        path = path.parent
    raise RuntimeError("Could not find repo root")

repo_root = find_repo_root()
sys.path.insert(0, str(repo_root))

from release.src.utils.Paths import ProjectPath

from release.src.utils.Manifest import Manifest
from release.src.preparer.Preparer import ReleasePreparer
from release.src.builder.Builder import ReleaseBuilder

from release.src.utils.ConsoleIO import print_status, wait_key

class ReleaseRunner:
    def __init__(self):
        self.ppath = ProjectPath(find_repo_root())

        self.manifest       = Manifest(self.ppath.release_dir / "manifest.toml")
        self.preparer       = ReleasePreparer   (self.manifest, self.ppath)
        self.builder        = ReleaseBuilder    (self.manifest, self.ppath)

    def run(self):
        print_status("INF", f"Name:  {self.manifest.name}")
        print_status("INF", f"Lang:  {self.manifest.language}")
        print_status("INF", f"Git:   {self.manifest.git_client}")
        print_status("INF", f"Ver:   {self.manifest.version}")

        print_status("INI", "Preparing...")
        self.preparer.prepare()

        print_status("INF", f"Press any key to build")
        wait_key()

        print_status("INI", "Building release")
        self.builder.build()

        print_status("OK", "Release ready")
        return 0

def main():
    signal.signal(signal.SIGINT, lambda *_: \
        sys.exit("\n[WRN] Interrupted by user (Ctrl+C). Exiting gracefully."))
    runner = ReleaseRunner()
    return runner.run()

if __name__ == "__main__":
    sys.exit(main())
