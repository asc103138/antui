"""
build_site_data.py - 自動掃描全域技能並產生網站專用的 data.json 與 skills_docs
"""
import os
import json
import re
import shutil

SKILLS_SOURCE_DIR = r"C:\Users\ccps\.gemini\config\skills"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_OUTPUT_DIR = os.path.join(BASE_DIR, "skills_docs")
DATA_JSON_PATH = os.path.join(BASE_DIR, "data.json")

# 類別對應定義
CATEGORY_MAP = {
    "12-rdq": {"cat": "🎯 智能工作流與方法論", "badge": "核心推薦", "icon": "🧭", "friendly_name": "RDQ 需求探索四象限訪談法"},
    "05-workflow": {"cat": "🎯 智能工作流與方法論", "badge": "SOP規範", "icon": "⚡", "friendly_name": "開工／收工／新專案標準流程"},
    "00-install-all": {"cat": "🎯 智能工作流與方法論", "badge": "一鍵懶人包", "icon": "📦", "friendly_name": "全套全域技能一鍵自動安裝"},
    "02-essentials": {"cat": "🎯 智能工作流與方法論", "badge": "新手必備", "icon": "🔰", "friendly_name": "AntiGravity 2 新手必要工具盤點"},

    "06-second-brain": {"cat": "🧠 第二大腦與筆記生態", "badge": "架構心法", "icon": "💡", "friendly_name": "教師第二大腦三層知識體系"},
    "06-obsidian": {"cat": "🧠 第二大腦與筆記生態", "badge": "雙向連結", "icon": "📓", "friendly_name": "Obsidian 專案筆記本機無縫對接"},
    "04-github-obsidian": {"cat": "🧠 第二大腦與筆記生態", "badge": "駕駛艙", "icon": "🛸", "friendly_name": "GitHub + Obsidian 雙向同步駕駛艙"},
    "01-notebooklm": {"cat": "🧠 第二大腦與筆記生態", "badge": "Google AI", "icon": "🤖", "friendly_name": "NotebookLM MCP / CLI 研習筆記自動化"},

    "14-advanced-docs": {"cat": "📑 文件與多媒體神器", "badge": "文書神手", "icon": "📄", "friendly_name": "進階文件處理 (PDF萬用/Word/Excel/圖片)"},
    "07-file-toolkit": {"cat": "📑 文件與多媒體神器", "badge": "三合一套件", "icon": "🧰", "friendly_name": "內部工具包 (Office/影音/Edge-TTS語音)"},
    "09-groq": {"cat": "📑 文件與多媒體神器", "badge": "高精度轉錄", "icon": "🎙️", "friendly_name": "Groq Whisper 語音轉字幕與逐字稿清洗"},
    "04-draw": {"cat": "📑 文件與多媒體神器", "badge": "視覺生圖", "icon": "🎨", "friendly_name": "Nano Banana Pro 繪圖生圖標準指引"},
    "13-video-specs": {"cat": "📑 文件與多媒體神器", "badge": "影音分鏡", "icon": "🎬", "friendly_name": "三類影片製作規範與自動化工作流"},

    "10-gemini": {"cat": "☁️ 雲端後端與本地模型", "badge": "API驗證", "icon": "✨", "friendly_name": "Gemini API 與 Google AI Studio 安全配置"},
    "07-supabase": {"cat": "☁️ 雲端後端與本地模型", "badge": "Postgres", "icon": "⚡", "friendly_name": "Supabase 雲端資料庫 MCP 整合"},
    "03-firebase": {"cat": "☁️ 雲端後端與本地模型", "badge": "Google雲端", "icon": "🔥", "friendly_name": "Firebase 雲端後端服務與安全規則"},
    "08-sheets-gas": {"cat": "☁️ 雲端後端與本地模型", "badge": "零主機庫", "icon": "📊", "friendly_name": "Google 試算表資料庫 + Apps Script 後端"},
    "09-ollama": {"cat": "☁️ 雲端後端與本地模型", "badge": "離線模型", "icon": "🦙", "friendly_name": "Ollama 本地離線模型安全對接"},

    "11-env-setup": {"cat": "⚙️ 環境工程與系統維護", "badge": "自動建置", "icon": "💻", "friendly_name": "開發環境自動建置 (Git / Node / uv)"},
    "02-github": {"cat": "⚙️ 環境工程與系統維護", "badge": "CLI工具", "icon": "🐙", "friendly_name": "GitHub CLI 認證與版本控制流程"},
    "13-chezmoi": {"cat": "⚙️ 環境工程與系統維護", "badge": "跨裝置同步", "icon": "🔄", "friendly_name": "chezmoi 跨電腦技能與設定安全同步"},
    "10-browser": {"cat": "⚙️ 環境工程與系統維護", "badge": "瀏覽器控制", "icon": "🌐", "friendly_name": "Playwright MCP 瀏覽器控制與自動化"},
    "15-windows-boot-diagnostics": {"cat": "⚙️ 環境工程與系統維護", "badge": "系統診斷", "icon": "🩺", "friendly_name": "Windows 開機與登入後效能診斷"},

    "steam-community-docs": {"cat": "🏫 教育實戰與社群成果", "badge": "公文行政", "icon": "🏆", "friendly_name": "STEAM 教師社群成果表、簽到表與領據生成"},
    "competency-test-generator": {"cat": "🏫 教育實戰與社群成果", "badge": "考卷排版", "icon": "📝", "friendly_name": "108 課綱素養命題助手 (Word 考卷自動排版)"},
    "render-zhuyin-web": {"cat": "🏫 教育實戰與社群成果", "badge": "國語排版", "icon": "🔤", "friendly_name": "中文直式/橫式注音標註與生字試卷生成"},
    "school-language-contest-coach": {"cat": "🏫 教育實戰與社群成果", "badge": "競賽教練", "icon": "🏅", "friendly_name": "校內國語文競賽全方位培訓教材生成器"},
    "17-g4-curriculum-review": {"cat": "🏫 教育實戰與社群成果", "badge": "三階審查", "icon": "🛡️", "friendly_name": "國小四年級教材與試題審查機制 (G4-Review)"},
    "18-word-zhuyin": {"cat": "📑 文件與多媒體神器", "badge": "注音排版", "icon": "🔤", "friendly_name": "Word (.docx) 國字自動注音標註與學習單排版"},
    "19-html-slide-builder": {"cat": "📑 文件與多媒體神器", "badge": "互動簡報", "icon": "📽️", "friendly_name": "Reveal.js HTML 互動簡報生成器"},

    "16-huggingface": {"cat": "☁️ 雲端後端與本地模型", "badge": "AI Hub", "icon": "🤗", "friendly_name": "Hugging Face 全域工作流 (MCP / CLI / Skills)"},
    "hf-cli": {"cat": "⚙️ 環境工程與系統維護", "badge": "Hub CLI", "icon": "🤗", "friendly_name": "Hugging Face Hub CLI 終端操作指南"},
    "huggingface-datasets": {"cat": "📑 文件與多媒體神器", "badge": "資料集", "icon": "📚", "friendly_name": "Hugging Face Datasets 檢視與下載"},
    "huggingface-gradio": {"cat": "📑 文件與多媒體神器", "badge": "Web UI", "icon": "🖼️", "friendly_name": "Gradio Web UI 與互動展示建置"},
    "huggingface-best": {"cat": "🎯 智能工作流與方法論", "badge": "模型評測", "icon": "🏆", "friendly_name": "最佳 AI 模型推薦與排行榜評估"},
    "huggingface-spaces": {"cat": "☁️ 雲端後端與本地模型", "badge": "ZeroGPU", "icon": "🚀", "friendly_name": "Hugging Face Spaces 部署與設定"},
    "huggingface-papers": {"cat": "🧠 第二大腦與筆記生態", "badge": "每日論文", "icon": "📑", "friendly_name": "Hugging Face 每日精選論文閱讀"},
    "huggingface-local-models": {"cat": "☁️ 雲端後端與本地模型", "badge": "離線推論", "icon": "💻", "friendly_name": "本機 GGUF / llama.cpp 模型選型"},

    "emil-design-eng": {"cat": "🎨 介面美學與動效工程", "badge": "設計工程", "icon": "✨", "friendly_name": "Emil Kowalski 設計工程與動效最低標準"},
    "mobile-native": {"cat": "🎨 介面美學與動效工程", "badge": "手機原生", "icon": "📱", "friendly_name": "行動端 Web 原生質感與 CSS 修復"},
}

def parse_frontmatter(content):
    meta = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            body = parts[2].strip()
            for line in fm_text.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip()
    return meta, body

def extract_triggers(text):
    triggers = []
    # 抓取 「...」 內所有觸發語
    matches = re.findall(r"「([^」]+)」", text)
    for m in matches:
        # 可能以 ／ 或 、 分隔
        parts = re.split(r"[/／、,]", m)
        for p in parts:
            p = p.strip()
            if p and len(p) <= 25 and p not in triggers:
                triggers.append(p)
    return triggers

def main():
    os.makedirs(DOCS_OUTPUT_DIR, exist_ok=True)
    skill_sources = []
    
    # 全域技能
    for folder in sorted(os.listdir(SKILLS_SOURCE_DIR)):
        skill_file = os.path.join(SKILLS_SOURCE_DIR, folder, "SKILL.md")
        if os.path.exists(skill_file):
            skill_sources.append((folder, skill_file))

    # 本地專案專屬技能
    local_gem_skill = os.path.join(BASE_DIR, "gem", ".agents", "skills", "competency-test-generator", "SKILL.md")
    if os.path.exists(local_gem_skill):
        skill_sources.append(("competency-test-generator", local_gem_skill))

    skills = []

    for folder, skill_file in skill_sources:
        with open(skill_file, "r", encoding="utf-8", errors="ignore") as f:
            raw_content = f.read()

        meta, body = parse_frontmatter(raw_content)
        name = meta.get("name", folder)
        raw_desc = meta.get("description", "")

        # 整理乾淨的簡介 (移除落落長的說「...」觸發語，取前段精華)
        clean_desc = raw_desc
        if "說「" in clean_desc:
            clean_desc = clean_desc.split("說「")[0].strip()
        elif "使用者說" in clean_desc:
            clean_desc = clean_desc.split("使用者說")[0].strip()
        elif "當使用者提到" in clean_desc:
            clean_desc = clean_desc.split("當使用者提到")[0].strip()

        triggers = extract_triggers(raw_desc)
        cat_info = CATEGORY_MAP.get(folder, {
            "cat": "🛠️ 其他工具與擴充技能",
            "badge": "技能擴充",
            "icon": "⚡",
            "friendly_name": name
        })

        # 檢測是否有專屬縮圖 (Cover Image)
        covers_dir = os.path.join(BASE_DIR, "assets", "covers")
        image_url = None
        potential_names = [
            f"cover_{folder.replace('-', '_')}.jpg",
            f"cover_{folder}.jpg",
            f"cover_{folder.replace('-', '_')}.png",
            f"cover_{folder}.png"
        ]
        for pname in potential_names:
            if os.path.exists(os.path.join(covers_dir, pname)):
                image_url = f"assets/covers/{pname}"
                break

        # 複製 SKILL.md 到 skills_docs/
        dest_doc = os.path.join(DOCS_OUTPUT_DIR, f"{folder}.md")
        with open(dest_doc, "w", encoding="utf-8") as df:
            df.write(raw_content)

        skills.append({
            "id": folder,
            "folder": folder,
            "name": name,
            "friendly_name": cat_info["friendly_name"],
            "category": cat_info["cat"],
            "badge": cat_info["badge"],
            "icon": cat_info["icon"],
            "image": image_url,
            "description": clean_desc if clean_desc else raw_desc[:120],
            "full_description": raw_desc,
            "triggers": triggers,
            "doc_filename": f"{folder}.md",
            "doc_content": body,
            "showOnMain": folder in ["emil-design-eng", "12-rdq", "14-advanced-docs", "06-second-brain", "01-notebooklm", "13-chezmoi", "steam-community-docs", "16-huggingface", "17-g4-curriculum-review", "19-html-slide-builder"]
        })

    # 分類匯總
    categories_dict = {}
    for s in skills:
        cat = s["category"]
        if cat not in categories_dict:
            categories_dict[cat] = []
        categories_dict[cat].append(s)

    projects_by_category = []
    for cat, items in categories_dict.items():
        projects_by_category.append({
            "category": cat,
            "count": len(items),
            "items": items
        })

    site_data = {
        "pageInfo": {
            "title": "敦元老師的 AntiGravity 技能倉庫｜AI Agent 備課與自動化工具庫",
            "brand": "DUN-YUAN AI",
            "brandBadge": "SKILLS",
            "ownerName": "謝敦元 (敦元老師)",
            "jobTitle": "國小教師 · STEAM 教師社群召集人 · AI Agent 實戰開發者",
            "bio": "專注於 Google AntiGravity、AI Agent 工作流、國小教育備課自動化與第二大腦知識體系構建。提供 100% 本機端隱私防護、開源模組化的高效教學與研習神器。",
            "email": "305822202+asc103138@users.noreply.github.com",
            "github": "https://github.com/asc103138",
            "repo": "https://github.com/asc103138/antui",
            "chezmoiRepo": "asc103138/dotfiles",
            "siteUrl": "https://asc103138.github.io/antui/",
            "totalSkills": len(skills),
            "lastUpdated": "2026-10-02"
        },
        "stats": [
            {"number": f"{len(skills)}+", "label": "全域 AntiGravity 技能", "icon": "🛠️"},
            {"number": "100%", "label": "本機運算 零個資外洩", "icon": "🔒"},
            {"number": "1鍵", "label": "chezmoi 跨裝置秒級同步", "icon": "🔄"},
            {"number": "24h", "label": "AI Agent 備課後勤力", "icon": "⚡"}
        ],
        "experiences": [
            {"date": "115-10", "type": "評量機制", "school": "梧棲區中正國小", "topic": "國小四年級教材與試題三階審查機制研發（南一數·翰林國·康軒社）與 Canva 作文句型牆", "showOnMain": True},
            {"date": "115-09", "type": "校園實務", "school": "梧棲區中正國小", "topic": "STEAM 教師社群：AI Agent 行政成果表與簽到公文自動化流程建置", "showOnMain": True},
            {"date": "115-09", "type": "工作流開發", "school": "AntiGravity 實戰", "topic": "RDQ Method 需求探索四象限法與 108 課綱素養命題助手工作流化", "showOnMain": True},
            {"date": "115-09", "type": "教材創作", "school": "數位教學創新", "topic": "四年級國語《鏡頭下的家鄉》Canva 繪圖填空教材與中秋彩繪柚子 360 環繞分鏡", "showOnMain": True},
            {"date": "115-09", "type": "雲端架構", "school": "第二大腦對接", "topic": "Obsidian 創作庫對接、chezmoi dotfiles 跨電腦雙機零摩擦同步架構", "showOnMain": True}
        ],
        "projects_by_category": projects_by_category,
        "skills": skills,
        "works": [
            {
                "title": "國小四年級教材與試題三階審查系統（含作文句型牆與素養題）",
                "tag": "四年級寫作與命題審查",
                "desc": "以最低標準（先備經驗/課綱指標/南一數·翰林國·康軒社版本對準）、中階（CLT認知負荷/SDGs/STEAM）與高階（迷思診斷/時事/媒體識讀）打造之全域審查體系。內含《快樂的家庭活動》Canva 填空與作文簿抄寫系統、南一數學海線淨灘試題。",
                "link": "g4-curriculum/",
                "demoLink": "g4-curriculum/worksheet.html",
                "date": "115-10"
            },
            {
                "title": "STEAM 教師社群活動行政文件生成系統",
                "tag": "教育行政自動化",
                "desc": "輸入活動照片與日期，自動比對 115 年度已簽核計畫書，秒級生成標準成果表、簽到表與講師領據，並無痛轉存 PDF 歸檔。",
                "link": "steam成果製作/",
                "date": "115-09"
            },
            {
                "title": "108 課綱素養命題助手 (Competency Exam Generator)",
                "tag": "智能評量工具",
                "desc": "以 RDQ 方法論為基底，貼上教材即可快速產出符合 108 課綱生活情境之單選/多選試題，並自動排版輸出標準 Word (docx) 學生卷與教師詳解卷。",
                "link": "gem/",
                "date": "115-09"
            },
            {
                "title": "國語四上《鏡頭下的家鄉》Canva 填空繪圖互動教材",
                "tag": "課堂教學教材",
                "desc": "田字四象限總覽與 4 頁分段放大相框頁設計，產出 16:9 原生 PPTX、A4 橫向黑白列印學習單 PDF 與單檔 HTML 網頁。",
                "link": "繁中套件/",
                "date": "115-09"
            },
            {
                "title": "360 Pomelo Cinema 中秋彩繪柚子分鏡與簡報設計",
                "tag": "影音分鏡設計",
                "desc": "透過 gemini-notebook-mcp 產出 Studio 簡報，依據 antigravity-video-specs 製作 11 個標準鏡頭腳本與防沾染操作守則。",
                "link": "中秋彩繪柚子/",
                "date": "115-09"
            }
        ]
    }

    with open(DATA_JSON_PATH, "w", encoding="utf-8") as jf:
        json.dump(site_data, jf, ensure_ascii=False, indent=2)

    print(f"✅ 成功產出 data.json (包含 {len(skills)} 個技能、{len(projects_by_category)} 個大類別)")
    print(f"✅ 成功複製全數 SKILL.md 至 {DOCS_OUTPUT_DIR}")

if __name__ == "__main__":
    main()
