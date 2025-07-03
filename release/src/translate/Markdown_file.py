import re, time, random
from pathlib import Path
from typing import List

class MarkdownFileTranslator:
    def __init__(self, api_client):
        self.api_client = api_client
        self.chunk_size = 3000

    def load_file(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def prepare_str(self, text: str) -> str:
        def replace_code_block(match):
            content = match.group(0)
            return f"<keep>\n{content}\n</keep>"

        text = re.sub(r"(^|\n)```.*?\n.*?```", replace_code_block, text, flags=re.DOTALL)

        text = re.sub(r"`[^`\n]+`", lambda m: f"<keep>{m.group(0)}</keep>", text)

        return text

    def clean_str(self, text: str) -> str:
        return text.replace("<keep>", "").replace("</keep>", "")
    
    def split_text(self, text: str) -> List[str]:
        chunks = []
        current_chunk = ""
        
        lines = text.split('\n')
        
        for line in lines:
            if len(current_chunk) + len(line) < self.chunk_size:
                current_chunk += line + '\n'
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
            
                if len(line) > self.chunk_size:
                    for i in range(0, len(line), self.chunk_size):
                        chunks.append(line[i:i+self.chunk_size])
                else:
                    current_chunk = line + '\n'
        
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks

    def translate_file(self, path: Path, target_lang: str):
        original = self.load_file(path)
        prepared = self.prepare_str(original)

        chunks = self.split_text(prepared)

        translated_chunks = []
        for chunk in chunks:
            translated = self.api_client.translate(chunk, target_lang=target_lang)
            translated_chunks.append(translated)
            time.sleep(random.uniform(5, 25))
        
        full_translation = '\n'.join(translated_chunks)
        cleaned = self.clean_str(full_translation)

        path.write_text(cleaned, encoding="utf-8")
