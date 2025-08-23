from textwrap import dedent
import shutil
import tarfile

from release.src.utils.Manifest import Manifest
from release.src.utils.Paths import ProjectPath

from release.src.utils.ConsoleIO import print_status

class BuildScriptGenerator:
    def __init__(self, manifest: Manifest, ppath : ProjectPath):
        self.manifest = manifest
        self.ppath = ppath

        self.temp_dir = ppath.temp_dir
        self.output_dir = ppath.output_dir
        
        self.output_name = f"{manifest.full_name}.run"
        self.output_path = self.output_dir / self.output_name

    def generate(self):
        print_status("INF", "Preparing .run archive...")

        self.output_dir.mkdir(parents=True, exist_ok=True)
        archive_path = self.output_dir / f"{self.manifest.name}.tar.gz"

        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(self.temp_dir, arcname=".")

        print_status("INF", f"Packed: {archive_path.name}")

        header = self.generate_script_header()

        with self.output_path.open("wb") as out_file:
            out_file.write(header)
            with archive_path.open("rb") as archive_file:
                shutil.copyfileobj(archive_file, out_file)

        self.output_path.chmod(0o755)
        archive_path.unlink()  # cleanup

        print_status("OK", f"Final: {self.output_path}")

    def generate_script_header(self) -> bytes:
        return dedent(f"""
            #!/bin/sh
            set -e
            START_DIR="$(pwd)"
            TMPDIR=$(mktemp -d 2>/dev/null || mktemp -d -t 'release_unpack')
            trap 'cd "$START_DIR"; rm -rf "$TMPDIR"' EXIT

            BASE_URL="${{1:-$REPO}}"
            if [ -z "$BASE_URL" ]; then
                echo "Enter base repo URL (with or without .git):"
                read BASE_URL
                BASE_URL=$(echo "$BASE_URL" | tr -d '\\r' | xargs)
            fi
            BASE_URL="${{BASE_URL%.git}}"

            echo "Branch for templates? [templates/{self.manifest.version}]"
            read TEMPLATE_BRANCH
            if [ -z "$TEMPLATE_BRANCH" ]; then
                TEMPLATE_BRANCH="templates/{self.manifest.version}"
            fi

            ARCHIVE_LINE=$(awk '/^__ARCHIVE_BELOW__/ {{print NR + 1; exit}}' "$0")
            tail -n +$ARCHIVE_LINE "$0" | tar -xz -C "$TMPDIR" || exit 1

            echo "--- Wiki ---"
            echo "Cloning wiki repo: $BASE_URL.wiki.git"
            git clone "$BASE_URL.wiki.git" "$TMPDIR/wiki-repo" || {{
                echo "ERROR: Failed to clone wiki. Make sure it exists and you have access."
                exit 1
            }}
            cp -r "$TMPDIR/wiki"/* "$TMPDIR/wiki-repo/"

            cd "$TMPDIR/wiki-repo"
            git add -A
            if ! git diff --cached --quiet; then
                git commit -m "Update wiki from release bundle"
                git push
            else
                echo "Wiki: no changes to commit"
            fi

            echo "--- Templates ---"
            git clone "$BASE_URL.git" "$TMPDIR/main-repo"
            cd "$TMPDIR/main-repo"
            git checkout "$TEMPLATE_BRANCH" || git checkout -b "$TEMPLATE_BRANCH"

            TEMPLATE_ROOT="$TMPDIR/templates"
            if [ -d "$TEMPLATE_ROOT" ]; then
                rsync -a "$TEMPLATE_ROOT"/ ./
            else
                echo "Templates: directory not found: $TEMPLATE_ROOT"
            fi

            git add -A
            if ! git diff --cached --quiet; then
                git commit -m "Add templates from release bundle"
                git push -u origin "$TEMPLATE_BRANCH"
            else
                echo "Templates: no changes to commit"
            fi

            echo "Done"
            exit 0
            __ARCHIVE_BELOW__
        """).lstrip().encode()