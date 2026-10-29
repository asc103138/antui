import re
from pathlib import Path

def clean_file(path: Path):
    if not path.exists():
        return
    text = path.read_text(encoding='utf-8')
    
    # 1. 替換 \times 為 ×
    text = text.replace(r'\times', '×')
    
    # 2. 替換 $...$ 為乾淨內容
    text = re.sub(r'\$([^\$]+)\$', r'\1', text)
    
    # 3. 再次確保任何殘餘的 \times 也被清乾淨
    text = text.replace(r'\times', '×')
    
    path.write_text(text, encoding='utf-8')
    print(f"Cleaned {path.name}:")
    print(f"  Remaining '$': {text.count('$')}")
    print(f"  Remaining '\\times': {text.count(r'\times')}")

clean_file(Path(r"d:\antui\動畫簡報\index.html"))
clean_file(Path(r"d:\antui\動畫簡報\乘法.html"))
