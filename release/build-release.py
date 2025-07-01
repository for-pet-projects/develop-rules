import argparse
from pathlib import Path
from src.manifest import Manifest
from src.builder import ReleaseRunBuilder


def main():
    parser = argparse.ArgumentParser(description="Build unified release.run file")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent,
                        help="Path to project root (default: auto-detect)")
    args = parser.parse_args()

    root = args.root
    release_dir = root / "release"
    lists_dir = release_dir / "lists"
    output_dir = root / "output"

    manifest = Manifest.load(release_dir / "manifest.toml")

    list_files = {
        "wiki": lists_dir / "wiki.list",
        "templates": lists_dir / "templates.list"
    }

    builder = ReleaseRunBuilder(
        root=root,
        version=manifest.version,
        name=manifest.name,
        list_files=list_files,
        output_dir=output_dir
    )
    builder.build()


if __name__ == "__main__":
    main()