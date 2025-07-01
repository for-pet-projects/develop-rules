import tomllib
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Manifest:
    name: str
    version: str

    @classmethod
    def load(cls, path: Path) -> "Manifest":
        if not path.exists():
            raise FileNotFoundError(f"Manifest file not found: {path}")
        with open(path, "rb") as f:
            data = tomllib.load(f)
        return cls(
            name=data.get("name", "unknown"),
            version=data.get("version", "0.0.0")
        )

    def wiki_repo_url(self, base_url: str) -> str:
        base_url = base_url.rstrip("/")
        return base_url + ".wiki.git"
