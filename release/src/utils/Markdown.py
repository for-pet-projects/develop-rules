def extract_translatables(content: str) -> list[str]:
    return [
        line for line in content.splitlines()
        if not line.strip().startswith("```") and "`" not in line
    ]

def merge_translation(original: str, source: list[str], translated: list[str]) -> str:
    for src, dst in zip(source, translated):
        original = original.replace(src, dst)
    return original
