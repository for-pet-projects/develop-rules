from pathlib import Path
from release.src.utils.ConsoleIO import print_status

class ListLoader:
    def __init__(self, source_dir: Path, dest_dir: Path):
        self.source_dir = source_dir.resolve()
        self.dest_dir   = dest_dir.resolve()

    def _parse_line(self, raw: str) -> tuple[Path, Path | None] | None:
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            return None
        if "#" in raw:
            raw = raw.split("#", 1)[0].strip()
        if not raw:
            return None

        if "->" in raw:
            source_raw, dest_raw = map(str.strip, raw.split("->", 1))
            source  = (self.source_dir  / source_raw).resolve()
            dest    = (self.dest_dir    / dest_raw).resolve()
        else:
            source  = (self.source_dir  / raw).resolve()
            dest    = (self.dest_dir    / source.relative_to(self.source_dir)).resolve()

        return (source, dest)

    def load(self, list_path: Path) -> list[tuple[Path, Path | None]]:
        result = []
        if not list_path.exists():
            raise FileNotFoundError(f"[ERROR] Missing list file: {list_path}")
        for line in list_path.read_text(encoding="utf-8").splitlines():
            parsed = self._parse_line(line)
            if parsed is None:
                continue
            source, dest = parsed
            if not source.exists():
                print_status("WRN", f"Missing: {source}")
            result.append((source, dest))
        return result