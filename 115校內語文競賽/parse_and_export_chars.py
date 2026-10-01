# -*- coding: utf-8 -*-
import re
import os

with open(r'd:\antui\115校內語文競賽\四年丙班_各項目培訓資料庫\03_國語字音字形組\老師_指導指引與每日進度表(含評量標準).md', 'r', encoding='utf-8') as f:
    text = f.read()

# 解析出 20 天資料
day_blocks = text.split("#### 【Day ")[1:]
chars_20_data = []

for block in day_blocks:
    lines = block.strip().split("\n")
    header = lines[0] # e.g. "01：10/05 (一)】常用破音字與易錯部首專題（一）"
    m = re.match(r'(\d+)：(.*?)】(.*)', header)
    day_num = f"Day {m.group(1)}"
    date_str = m.group(2)
    theme_str = m.group(3)

    phonetics = []
    characters = []

    mode = None
    for line in lines[1:]:
        line = line.strip()
        if "一、字音部分" in line:
            mode = "phonetic"
            continue
        elif "二、字形部分" in line:
            mode = "character"
            continue
        elif line.startswith("---"):
            break

        if mode == "phonetic" and "➔" in line:
            # 1. 鞋「楦」子 ➔ **ㄒㄩㄢˋ**（木部，鞋楦，勿讀ㄒㄩㄢ）
            pm = re.match(r'\d+\.\s*(.*?)\s*➔\s*\*\*(.*?)\*\*[（\(](.*?)[）\)]', line)
            if pm:
                phonetics.append((pm.group(1), pm.group(2), pm.group(3)))
        elif mode == "character" and "➔" in line:
            # 1. 臉上「ㄗㄨㄛˊ」瘡 ➔ **【 痤 】**（疒部，痤瘡，勿寫成挫）
            cm = re.match(r'\d+\.\s*(.*?)\s*➔\s*\*\*【\s*(.*?)\s*】\*\*[（\(](.*?)[）\)]', line)
            if cm:
                characters.append((cm.group(1), cm.group(2), cm.group(3)))

    chars_20_data.append({
        "day": day_num,
        "date": date_str,
        "theme": theme_str,
        "phonetics": phonetics,
        "characters": characters
    })

print(f"Successfully parsed {len(chars_20_data)} days, Day 1 phonetics count: {len(chars_20_data[0]['phonetics'])}, characters count: {len(chars_20_data[0]['characters'])}")

# 將解析出來的完整資料庫存為 chars_database_400.py
with open(r'd:\antui\115校內語文競賽\chars_database_400.py', 'w', encoding='utf-8') as f:
    f.write("# -*- coding: utf-8 -*-\nCHARS_20DAYS_DATA = " + repr(chars_20_data) + "\n")

print("chars_database_400.py generated successfully.")
