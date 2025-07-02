from pathlib import Path
import tomllib

class Manifest:
    def __init__(self, path: str | Path):
        self._path = Path(path)
        with self._path.open("rb") as f:
            self._data = tomllib.load(f)

    @property
    def name(self) -> str:
        return self._data.get("name", "unnamed-release")

    @property
    def version(self) -> str:
        return self._data.get("version", "0.0.0")

    @property
    def language(self) -> str:
        return self._data.get("language", "en")

    @property
    def git_client(self) -> str:
        return self._data.get("git_client", "github")
