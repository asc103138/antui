import re
import os

html_path = '成果展繳交資料/steam-gigo-balance-deck/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    c = f.read()

secs = re.findall(r'<section[\s\S]*?</section>', c)
print(f'Total sections: {len(secs)}')

for i, s in enumerate(secs, 1):
    bg = re.search(r'data-background-image=[\'"]([^\'"]+)', s)
    bg_str = bg.group(1) if bg else 'NONE'
    t = re.search(r'<h[12][^>]*>([\s\S]*?)</h[12]>', s)
    t_str = re.sub(r'<[^>]+>', '', t.group(1)).strip() if t else 'NO TITLE'
    
    # check if bg file exists
    full_bg = os.path.normpath(os.path.join('成果展繳交資料/steam-gigo-balance-deck', bg_str))
    exists = os.path.exists(full_bg) if bg_str != 'NONE' else False
    
    # find images inside section
    imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)', s)
    
    print(f"S{i:02d}: bg={bg_str} (exists={exists}) | title={t_str[:30]} | imgs={len(imgs)}")
