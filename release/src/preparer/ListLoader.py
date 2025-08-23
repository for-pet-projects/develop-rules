from pathlib import Path
from release.src.utils.ConsoleIO import print_status

class BaseLineParser:
    comment_marker = "#"
    mapping_marker = "->"
    root_prefix = "@root "

    @classmethod
    def _commentoff(cls, raw: str) -> str:
        raw = raw.strip()
        if raw.startswith(cls.comment_marker): return None
        if cls.comment_marker in raw:
            raw = raw.split(cls.comment_marker, 1)[0].strip()
        return raw or None

    @classmethod
    def _split_mapping(cls, raw: str) -> tuple[str, str]:
        if cls.mapping_marker in raw:
            left, right = raw.split(cls.mapping_marker, 1)
        else:
            left, right = raw, raw
        return left.strip(), right.strip()
    
    @classmethod
    def _root_detect(cls, raw: str) -> tuple[str, bool]:
        if raw.startswith(cls.root_prefix):
            return raw[len(cls.root_prefix):].strip(), True
        return raw, False

    @classmethod
    def parse(cls, raw: str) -> tuple[Path, Path, bool] | None:
        raw_clean = cls._commentoff(raw)
        if raw_clean is None: return None

        raw_clean, root = cls._root_detect(raw)

        source_raw, dest_raw = cls._split_mapping(raw_clean)

        return Path(source_raw), Path(dest_raw), root


class ListLoader:
    def __init__(self, source_dir: Path, dest_dir: Path):
        self.source_dir = source_dir.resolve()
        self.dest_dir   = dest_dir.resolve()

        if self.dest_dir == self.source_dir:
            raise ValueError(f"[ERR] destination must differ from source")

    def _recursive_load(self, source_raw : Path, dest_raw : Path, root : bool) -> list[tuple[Path, Path]]:
        result: list[tuple[Path, Path]] = []    
        src     = (self.source_dir  / source_raw).resolve()
        dest    = (self.dest_dir    / dest_raw  ).resolve()

        if not src.exists():
            raise FileNotFoundError(f"[ERR] Missing list file: {src}")
        
        if src.is_file():
            if root:
                result.append((src, self.dest_dir / dest.name))
            else:
                result.append((src, dest))
        elif src.is_dir():
            for path in src.rglob("*"):
                if path.is_file():
                    if root:
                        result.append((path, self.dest_dir / path.name))
                    else:
                        rel = path.relative_to(src)
                        new_dest = dest / rel if dest else None
                        result.append((path, new_dest))
        return result


    def load(self, list_path: Path) -> list[tuple[Path, Path]]:
        result: list[tuple[Path, Path]] = []
        if not list_path.exists():
            raise FileNotFoundError(f"[ERR] Missing list file: {list_path}")
        for line in list_path.read_text(encoding="utf-8").splitlines():
            src, dst, is_root = BaseLineParser.parse(line)
            result.extend(self._recursive_load(src, dst, is_root))
        return result