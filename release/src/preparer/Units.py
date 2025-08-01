from pathlib import Path
import shutil

from release.src.utils.Paths import ProjectPath
from release.src.utils.Manifest import Manifest

from release.src.preparer.Translate import Translator
from release.src.preparer.ListLoader import ListLoader

from release.src.utils.ConsoleIO import print_status

class UnitPreparer:
    def __init__(self, name : str, manifest: Manifest, ppath : ProjectPath):
        self.manifest = manifest
        self.ppath = ppath
        
        self.source_dir = self.ppath.root_dir
        self.dest_dir   = self.ppath.temp_dir / name
        self.list_path  = self.ppath.release_dir \
            / "lists" / self.manifest.git_client / (name + ".list")

        self.list_loader = ListLoader(self.source_dir, self.dest_dir)
        self.translator = Translator(self.manifest.language, self.ppath.i18n, self.ppath.root_dir)

    def prepare(self):
        self._ensure_clean(self.dest_dir)
        
        raw_entries = self.list_loader.load(self.list_path)
        expanded_entries = []
        for src, dst in raw_entries:
            if src.is_file():
                expanded_entries.append((src, dst))
            elif src.is_dir():
                for path in src.rglob("*"):
                    if path.is_file():
                        rel = path.relative_to(src)
                        new_dest = dst / rel if dst else None
                        expanded_entries.append((path, new_dest))


        sources, destinations = zip(*expanded_entries)
        translated_sources = self.translator.ensure_all(list(sources))
        final_entries = list(zip(translated_sources, destinations))

        self._copy_from_to(final_entries)
        
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




class WikiPreparer(UnitPreparer):
    def prepare(self):
        super().prepare()
        self._generate_index()

    def _generate_index(self):
        entrypoint_name = f"{self.manifest.name}-entrypoint.md"
        entrypoint_path = self.dest_dir / entrypoint_name

        lines = [f"# Entrypoint {self.manifest.full_name}\n"]
        lines.append("<ul>")

        def walk(path: Path):
            items = []
            for entry in sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
                if entry.name == entrypoint_name:
                    continue
                rel_path = entry.relative_to(self.dest_dir).as_posix()

                if entry.is_dir():
                    children = walk(entry)
                    items.append(f"<li>{entry.name}/<ul>\n{''.join(children)}</ul></li>")
                elif entry.suffix == ".md":
                    items.append(f'<li><a href="{rel_path}">{entry.stem}</a></li>\n')
            return items

        lines.extend(walk(self.dest_dir))
        lines.append("</ul>")

        entrypoint_path.write_text("\n".join(lines), encoding="utf-8")
        print_status("OK", f"Generated index: {entrypoint_path}")