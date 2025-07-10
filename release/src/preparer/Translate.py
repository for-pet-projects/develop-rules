import hashlib, json
from pathlib import Path
from release.src.utils.Print import print_status, wait_key


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

    def ensure(self, original: Path) -> Path:
        if self.lang == "en":
            return original

        rel_path = original.relative_to(self.project_root)
        translated = self.i18n_root / self.lang / rel_path

        if not original.exists():
            raise FileNotFoundError(f"Missing source file: {original}")

        original_hash = self._hash_content(original)
        stored_hash = self.registry.get_hash(str(rel_path))

        if translated.exists() and \
            (stored_hash == original_hash or stored_hash == None):
            return translated
        
        self.register(original)

        if translated.exists():
            print_status("WRN", f"Translation outdated: {translated}")

            choice = input("Use original instead? [y/N]: ").strip().lower()
            if choice == "y":
                return original
            else:
                return translated
        else:
            print_status("WRN", f"Translation missing: {translated}")
            print_status("INF", f"Original: {original}")

            choice = input("Use original instead? [y/N]: ").strip().lower()
            if choice == "y":
                return original 
            else:
                raise RuntimeError(f"Missing valid translation for: {rel_path}")
 

    def register(self, original: Path):
        rel_path = original.relative_to(self.project_root)
        original_hash = self._hash_content(original)
        self.registry.set_hash(str(rel_path), original_hash)

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

        choice = input("Update translate hash registry? [Y/n]: ").strip().lower()
        if choice != "n":
            self.gate.save()

        return result
        