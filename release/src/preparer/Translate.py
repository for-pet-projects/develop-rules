import hashlib, json, functools
from pathlib import Path
from release.src.utils.ConsoleIO import print_status, prompt

def update_registry_on_success(func):
    @functools.wraps(func)
    def wrapper(self, original: Path):
        rel_path = original.relative_to(self.project_root)
        current_hash = self._hash_content(original)
        result = func(self, original)
        self.registry.set_hash(str(rel_path), current_hash)
        return result
    return wrapper

class TranslationRegistry:
    def __init__(self, lang: str, i18n_root: Path):
        self.lang = lang
        self.i18n_root = i18n_root
        self.registry_path = i18n_root / lang / ".hashes.json"
        self.data = self._load()

    def _load(self) -> dict:
        if self.registry_path.exists():
            try:
                return json.loads(self.registry_path.read_text(encoding="utf-8"))
            except Exception:
                return {}
        return {}

    def save(self):
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        self.registry_path.write_text(json.dumps(self.data, indent=2), encoding="utf-8")

    def get_hash(self, rel_path: str) -> str | None:
        return self.data.get(rel_path)

    def set_hash(self, rel_path: str, hash_val: str):
        self.data[rel_path] = hash_val

class TranslationGate:
    def __init__(self, lang: str, i18n_root: Path, project_root : Path):
        self.lang = lang
        self.i18n_root = i18n_root
        self.project_root = project_root

        self.registry = TranslationRegistry(lang, i18n_root)

    def _hash_content(self, path: Path) -> str:
        data = path.read_bytes()
        return hashlib.sha256(data).hexdigest()

    @update_registry_on_success
    def ensure(self, original: Path) -> Path:
        if not original.exists():
            raise FileNotFoundError(f"Missing source file: {original}")
        
        if self.lang == "en":
            return original
        
        rel_path = original.relative_to(self.project_root)
        translated = self.i18n_root / self.lang / rel_path

        original_hash = self._hash_content(original)
        stored_hash = self.registry.get_hash(str(rel_path))

        if translated.exists() and \
            (stored_hash == original_hash or stored_hash is None):
            return translated

        if translated.exists():
            print_status("WRN", f"Translation outdated: {translated}")

            if prompt("Use original instead?", False):
                return original
            else:
                return translated
        else:
            print_status("WRN", f"Translation missing: {translated}")
            print_status("INF", f"Original: {original}")

            if prompt("Use original instead?", False):
                return original 
            else:
                raise RuntimeError(f"Missing valid translation for: {rel_path}")
            
    def save(self):
        self.registry.save()

class Translator:
    def __init__(self, lang: str, i18n_root: Path, project_root : Path):
        self.lang = lang
        self.i18n_root = i18n_root
        self.project_root = project_root

        self.gate = TranslationGate(lang, i18n_root, project_root)

    def ensure_all(self, files: list[Path]) -> list[Path]:
        result = [self.gate.ensure(path) for path in files]

        if prompt("Update translate hash registry?"):
            self.gate.save()

        return result
        