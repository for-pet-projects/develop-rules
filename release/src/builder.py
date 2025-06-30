import os
import tarfile
import io
from pathlib import Path
from textwrap import dedent
from typing import Union

class ReleaseRunBuilder:
    def __init__(self, root: Path, version: str, name: str, list_files: dict[str, Path], output_dir: Path):
        self.root = root
        self.version = version
        self.name = name
        self.list_files = list_files  # section -> list_file
        self.output_dir = output_dir
        self.output_path = self.output_dir / f"{name}-v{version}.run"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def collect_sources(self):
        for section, list_file in self.list_files.items():
            if not list_file.exists():
                raise FileNotFoundError(f"Missing list file: {list_file}")
            with open(list_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        parts = line.split("=>")
                        src = parts[0].strip()
                        dst = parts[1].strip() if len(parts) > 1 else src
                        full_src = self.root / src
                        if full_src.exists():
                            yield section, full_src, dst
                        else:
                            print(f"Warning: skipping missing path {full_src}")

    def generate_script_header(self) -> bytes:
        template_copy_lines = []
        template_copy_lines.append("mkdir -p \"$TMPDIR/main-repo\"")
        template_copy_lines.append("cd \"$TMPDIR/main-repo\"")
        template_copy_lines.append("TEMPLATE_ROOT=\"$TMPDIR/__TEMPLATES__\"")
        template_copy_lines.append("find \"$TEMPLATE_ROOT\" -type f | while read src; do")
        template_copy_lines.append("    rel=\"${src#$TEMPLATE_ROOT/}\"")
        template_copy_lines.append("    dst=\"$rel\"")
        template_copy_lines.append("    mkdir -p \"$(dirname \"$dst\")\"")
        template_copy_lines.append("    cp \"$src\" \"$dst\"")
        template_copy_lines.append("done")

        return dedent(f"""
            #!/bin/sh

            set -e
            START_DIR="$(pwd)"
            TMPDIR=$(mktemp -d 2>/dev/null || mktemp -d -t 'release_unpack')

            BASE_URL="${{1:-$REPO}}"

            if [ -z "$BASE_URL" ]; then
                echo "Enter base repo URL (with or without .git):"
                read BASE_URL
                BASE_URL=$(echo "$BASE_URL" | tr -d '\r' | xargs)
            fi

            BASE_URL=$(echo "$BASE_URL" | sed 's/\\.git$//')

            echo "Branch for templates? [templates/{self.version}]"
            read TEMPLATE_BRANCH
            if [ -z "$TEMPLATE_BRANCH" ]; then
                TEMPLATE_BRANCH="templates/{self.version}"
            fi

            ARCHIVE_LINE=$(awk '/^__ARCHIVE_BELOW__/ {{print NR + 1; exit}}' "$0")
            tail -n +$ARCHIVE_LINE "$0" | tar -xz -C "$TMPDIR" || exit 1

            echo "--- Wiki ---"
            echo "Cloning wiki repo: $BASE_URL.wiki.git"
            if ! git clone "$BASE_URL.wiki.git" "$TMPDIR/wiki-repo"; then
                echo "ERROR: Failed to clone wiki. Make sure it exists and you have access."
                exit 1
            fi

            mkdir -p "$TMPDIR/wiki-repo/{self.name}"
            cp -r "$TMPDIR/__WIKI__"/* "$TMPDIR/wiki-repo/{self.name}/"

            INDEX_MD="$TMPDIR/wiki-repo/{self.name}.md"
            echo "# Wiki contents for {self.name}" > "$INDEX_MD"
            echo >> "$INDEX_MD"

            cd "$TMPDIR/wiki-repo/{self.name}"
            find . -type f | sort | while read path; do
                echo "- [$(basename \"$path\")]({self.name}/$path)" >> "$INDEX_MD"
            done
            cd "$TMPDIR/wiki-repo"

            git add .
            git commit -m "Update wiki from release bundle"
            git push

            echo "--- Templates ---"
            echo "Cloning repo: $BASE_URL.git"
            git clone "$BASE_URL.git" "$TMPDIR/main-repo" || exit 1
            cd "$TMPDIR/main-repo"
            git checkout "$TEMPLATE_BRANCH" || git checkout -b "$TEMPLATE_BRANCH"

            {'\n            '.join(template_copy_lines)}

            git add .
            git commit -m "Add templates from release bundle"
            git push -u origin "$TEMPLATE_BRANCH"

            cd "$START_DIR"
            rm -rf "$TMPDIR"
            echo "Done"
            exit 0
            __ARCHIVE_BELOW__
        """).lstrip().encode()

    def build(self):
        print(f"[release] Building: {self.output_path}")

        script_header = self.generate_script_header()
        with open(self.output_path, "wb") as f:
            f.write(script_header)

        archive_stream = io.BytesIO()
        with tarfile.open(fileobj=archive_stream, mode="w:gz") as tar:
            for section, src, dst in self.collect_sources():
                arcname = Path(f"__{section.upper()}__") / dst
                tar.add(src, arcname=arcname)
                print(f"  + {arcname}")

        with open(self.output_path, "ab") as f:
            f.write(archive_stream.getvalue())

        os.chmod(self.output_path, 0o755)
        print(f"[release] Done: {self.output_path}")
