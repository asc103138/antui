---
name: antigravity-groq
description: 用 Groq 的免費 API 做「語音轉字幕」與「逐字稿清洗」，並把整條流程包成可重複使用的技能。說「語音轉字幕」「影片上字幕」「做逐字稿」「Whisper」「Groq」「把錄音整理成講義」「把 API 變成工具」時載入。
---

# Groq 語音轉字幕與逐字稿清洗

## 🔴 隱私紅線（最高優先原則）
- **嚴禁上傳**：
  - 含有未成年學生聲音或姓名的課堂錄音
  - 親師溝通、輔導紀錄、個案談話
- **可以上傳**：
  - 教師本人口述、備課錄音
  - 公開演講、教材旁白、公開影片
- **防呆規則**：上傳前務必先聽音檔**最後 30 秒**，確認沒有忘記按停止而錄進去的私人對話。

---

## 操作步驟

### 步驟一：取得 API Key
1. 至 [Groq Console](https://console.groq.com/keys) 註冊並建立 API Key。
2. 設定環境變數：
   ```powershell
   $env:GROQ_API_KEY = "你的_API_KEY"
   ```
   > ⚠️ 嚴禁將 API Key commit 到 repo 或寫入任何公開檔案中。

### 步驟二：音訊前處理（FFmpeg）
Groq 檔案大小上限為 25MB。使用 FFmpeg 壓縮為 16kHz 單聲道：
```powershell
ffmpeg -i "input.mp4" -vn -ar 16000 -ac 1 -b:a 48k "audio.mp3"
```

### 步驟三：轉錄為字幕或逐字稿（Python 範例）
```python
import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

with open("audio.mp3", "rb") as file:
    # 產生 SRT 字幕
    transcription = client.audio.transcriptions.create(
        file=( "audio.mp3", file.read() ),
        model="whisper-large-v3",
        response_format="srt",
        language="zh"
    )
    print(transcription)
```

### 步驟四：逐字稿清洗與標點整理
將轉錄出的文字餵給 AI 模型進行後處理：
- 去除口頭禪（例如：「然後」、「對」、「那個」）
- 依據句意補齊標點符號與分段
- 修正同音錯別字與專業名詞
