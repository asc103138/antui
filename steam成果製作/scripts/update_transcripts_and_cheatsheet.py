#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新 22 頁旗艦版發表逐字講稿與 CheatSheet，並生成 .docx 與 .pdf
徹底移除學生課堂迷思，100% 圍繞社群做了什麼（共備、自研教具、試教、議課反思、數據實證、賽事整合）。
"""

import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

DOC_DIR = r"d:\antui\steam成果製作\成果展繳交資料"

MD_TRANSCRIPT = """# 臺中市梧棲區中正國民小學 115年度STEAM教師專業學習社群
## 成果展 5 分鐘現場發表逐字講稿（22 頁旗艦版 · 圍繞社群研發作為 · 含計時標記）

- **發表學校**：臺中市梧棲區中正國民小學
- **社群召集人 / 發表人**：謝敦元 老師
- **社群夥伴**：王怡婷 老師、李仁耀 老師、曾泊淞 老師
- **教案主題**：積木啟發量感 · 機關驗證平衡 —— 智高積木融入三年級重量測量機關課程
- **發表總時長**：嚴格控制於 **4 分 45 秒 ～ 4 分 58 秒**（合規上限 5 分鐘，平均每頁約 13~14 秒）

---

### 【00:00 - 00:15】Slide 1 封面：積木啟發量感 · 機關驗證平衡
> **[投影片：Slide 1 封面]**
> 
> 各位評審委員、教育先進大家好！我是中正國小社群召集人謝敦元。今天代表我們社群四位老師，向各位分享我們這一年深耕的跨域教案——**「積木啟發量感 · 機關驗證平衡」**。我們的核心理念是：**讓抽象的數學量感，在積木咔嗒聲中看得見、摸得到！**

---

### 【00:15 - 00:30】Slide 2 社群推動脈絡：踏實共備與 100% 執行
> **[按鍵換頁 ➜ Slide 2 社群推動脈絡]**
> 
> 本社群由我與王怡婷、李仁耀、曾泊淞老師跨數學、自然與資訊協同。從 5 月到 10 月扎實推動 7 場研習與公開觀議課，16 節課程 16,000 元經費全額無瑕結報；更特聘南投鯉魚國小陳建安名師跨校交流，展現中正國小強大共備動能！

---

### 【00:30 - 00:43】Slide 3 社群研發全景地圖：四階段推進與七大里程碑
> **[按鍵換頁 ➜ Slide 3 社群研發全景架構]**
> 
> 社群這一年依循四大階段踏實研發：第一階段「教材剖析與方向確立」；第二階段「教具研發與名師交流」；第三階段「入班試教與數據實證」；第四階段「世界機關王競賽整合與教案典藏」，每一步都留下扎實的教學研究足跡！

---

### 【00:43 - 00:56】Slide 4 社群研發動機與破局策略：自製天平取代黑盒子
> **[按鍵換頁 ➜ Slide 4 社群研發動機]**
> 
> 為什麼我們要大費周章自製天平？因為市售彈簧秤就像「黑盒子」，學生只盲看指針讀數，指針沒歸零、刻度看錯都不知道原理。社群決心用智高積木自製全透明物理結構，讓力臂長度、轉軸支點與力矩平衡一目了然！

---

### 【00:56 - 01:09】Slide 5 課綱領域指標深度轉化：十二年國教數學實作對應
> **[按鍵換頁 ➜ Slide 5 課綱指標深度轉化]**
> 
> 本教案緊密對齊課綱三大指標：**n-II-8** 以 5g 單位積木建立重量基準；**n-II-9** 組裝 20 孔等臂機構理解槓桿平衡；以及 **n-II-2** 將加減算則轉化為天平增減積木。我們把課綱抽象條目落實為生動實作！

---

### 【01:09 - 01:23】Slide 6 社群三節課教案研發：階梯式探究架構
> **[按鍵換頁 ➜ Slide 6 三節課教案架構]**
> 
> 社群歷經多次共備修訂，定稿階梯式探究架構：第 1 節「手感體驗與需求建構」；第 2 節「智高積木等臂機構組裝」；第 3 節「公克積木微調與算則具象」，形成由感官啟發、結構組裝到數理計量的完整探究閉環。

---

### 【01:23 - 01:36】Slide 7 社群教學設計 (一)：第 1 節手感體驗與測量需求建構
> **[按鍵換頁 ➜ Slide 7 第 1 節教學設計]**
> 
> 第一節課，社群設計兩道實驗：首先讓學生閉眼盲測大保麗龍和小鐵球，掌心下沉的竟是小鐵球，破除視覺偏誤；接著雙手掂重時手部肌肉疲勞產生爭議，社群引導孩子達成共識：「我們需要客觀、穩定、不會累的天平！」

---

### 【01:36 - 01:50】Slide 8 社群教具研發 (二)：智高積木等臂天平四核心機構
> **[按鍵換頁 ➜ Slide 8 四核心機構工程規格]**
> 
> 社群歷經三代零件選配，定案四大核心組件：提供極低重心的梯形基座、左右各 10 孔嚴格對稱橫樑、消除卡榫摩擦的低阻尼轉軸，以及雙繩垂直懸吊托盤。讓三年級學童在 12 分鐘內就能精準完成組裝！

---

### 【01:50 - 02:03】Slide 9 社群技術突破：低阻尼轉軸除錯與基準線定規
> **[按鍵換頁 ➜ Slide 9 技術突破與調校]**
> 
> 在研發過程中，社群克服兩大技術瓶頸：第一，改採光滑軸套排除轉軸阻尼，讓 2g 微小重量也能靈敏感應；第二，在基座中央增設「零點鉛直基準線」，讓指針平衡判讀具備客觀科學標準，大幅提升測量重現性！

---

### 【02:03 - 02:16】Slide 10 社群公開觀課與專業議課：試教現場反思與精進
> **[按鍵換頁 ➜ Slide 10 公開觀課與專業議課]**
> 
> 社群在三年丙班進行公開觀議課，四位教師全員觀課。現場記錄學生實作參與率高達 100%；議課時針對懸吊繩卡榫等高問題迅速提出改良對策，並將任務單增設「估測對照欄」，展現社群反思與行動研究的實戰力！

---

### 【02:16 - 02:29】Slide 11 社群教學設計 (三)：第 3 節 5g 單位積木定量與加減微調
> **[按鍵換頁 ➜ Slide 11 第 3 節任務設計]**
> 
> 第三節課社群引導孩子走向標準單位。社群精準測量智高正方體每顆恰為 5 公克！放 1 顆是 5g、2 顆是 10g，數算顆數乘以 5，乘法倍數與重量數值在天平上完美連動，讓生活秤量任務輕鬆破解！

---

### 【02:29 - 02:42】Slide 12 社群教材創新轉化：兩步驟加減法情境具象化
> **[按鍵換頁 ➜ Slide 12 教材創新轉化]**
> 
> 課本最抽象的兩步驟加減法，在社群的天平上化為具體手感：天平左傾，右盤補積木補平（加法補足策略：35 + 15 = 50g）；計算去皮淨重時，直接從砝碼盤拿掉積木（減法移除策略：80 - 20 = 60g），徹底根除算則盲點！

---

### 【02:42 - 02:58】Slide 13 社群研發成效對比：傳統課堂困境 vs STEAM 新典範
> **[按鍵換頁 ➜ Slide 13 3D 成效對比滑桿]**
> 
> （現場演示拖曳滑桿）請看大螢幕：**向左拖動**回顧傳統黑盒子讀數困境，指針未調零、算則機械背誦；**向右拖動**展現中正社群 STEAM 研發新典範，孩子親手組裝調校，前後測理解度大躍升 28.5%，滿意度達 96.8%！這就是社群深耕的最佳見證！

---

### 【02:58 - 03:12】Slide 14 社群成果縱向延展 (一)：四年級 micro:bit 甩繩智動量測
> **[按鍵換頁 ➜ Slide 14 成果縱向延展 micro:bit]**
> 
> 社群成果進一步跨年級延展！李仁耀老師跨領域整合四年級體育與資訊，開發「micro:bit 甩繩軌跡神射手」，利用 3 軸加速度計即時感測跳繩震盪，以藍牙廣播串流大數據，繪製體適能統計折線圖，跨域成效深獲好評！

---

### 【03:12 - 03:26】Slide 15 社群成果縱向延展 (二)：世界機關王 (GM) 校隊梯隊
> **[按鍵換頁 ➜ Slide 15 成果縱向延展 世界機關王]**
> 
> 我們更將天平微型槓桿昇華為競賽級「重力傾斜開關」，串聯複合減速齒輪箱與軌道，完成世界機關王指定之 8 迴連續連鎖關卡！成功培訓 12 位校隊梯隊小創客，連續觸發穩定度超越 90%！

---

### 【03:26 - 03:40】Slide 16 社群歷程回憶錄 (一)：萌芽共備與原型研發
> **[按鍵換頁 ➜ Slide 16 社群歷程回憶錄 (一)]**
> 
> 接下來呈現社群教師的踏實足跡。第一張照片記錄 5 月 20 日社群啟動，四位教師齊聚拆解數學迷思；第二張則是第一代智高天平原型機組裝測試，克服卡榫摩擦，奠定整年研發基石。

---

### 【03:40 - 03:54】Slide 17 社群歷程回憶錄 (二)：校際參訪與創客交流
> **[按鍵換頁 ➜ Slide 17 社群歷程回憶錄 (二)]**
> 
> 8 月 10 日我們走出校園，親赴南投鯉魚國小創客基地，特聘世界機關王金牌教練陳建安老師深度座談。陳老師傾囊相授機構傳動與模組管理，讓我們成功將競賽級技術降轉為國小日常課堂教具！

---

### 【03:54 - 04:08】Slide 18 社群歷程回憶錄 (三)：教具精進與跨域研討
> **[按鍵換頁 ➜ Slide 18 社群歷程回憶錄 (三)]**
> 
> 9 月 26 日進行天平轉軸阻尼與指針精密校正，確立零點鉛直基準線，排除微摩擦干擾，讓量測靈敏度達到 2.5g 高精度；10 月 1 日怡婷老師主持科技體育跨域共備，引導社群教師探討 micro:bit 加速度數據視覺化，展現跨域研發實力！

---

### 【04:08 - 04:22】Slide 19 社群歷程回憶錄 (四)：成效研析與機關精進
> **[按鍵換頁 ➜ Slide 19 社群歷程回憶錄 (四)]**
> 
> 10 月 5 日仁耀老師與我共同主持成效研討，逐題比對前後測試卷，數據證實理解度提升 28.5%！我們更針對兩步驟加減法情境進行具象化轉化，確立第二代標準化天平教具。

---

### 【04:22 - 04:36】Slide 20 社群歷程回憶錄 (五)：機關王 8 迴整合與團隊合影
> **[按鍵換頁 ➜ Slide 20 社群歷程回憶錄 (五)]**
> 
> 10 月 19 日謝敦元召集人深入解析世界機關王賽事期程與指定關卡傳動調校策略；右側則是社群教師齊聚收斂整年研發歷程，16 節課程 16,000 元無瑕結報，凝聚了無比堅實的團隊研發成果！

---

### 【04:36 - 04:50】Slide 21 社群歷程回憶錄 (六)：教案設計正式藍圖與評量規準
> **[按鍵換頁 ➜ Slide 21 社群歷程回憶錄 (六)]**
> 
> 依計畫規定，我們已如期產出「附件 6 正式教案設計」，內嵌等臂天平 10 孔距工程藍圖與任務挑戰單，搭配三階素養規準表，兼具歷程性與總結性評量，具備極高跨校推廣價值！

---

### 【04:50 - 05:00】Slide 22 亮眼推動成效與未來展望：讓 STEAM 在中正生根
> **[按鍵換頁 ➜ Slide 22 結語與展望]**
> 
> 總結這一年：前後測提升 28.5%、學生滿意度 96.8%、教案完整送件典藏！感謝教育局與輔導團隊支持，中正國小將持續深耕，讓每個孩子在 STEAM 實作中自信發光！感謝各位聆聽，敬請指教！
"""

MD_CHEATSHEET = """# 臺中市梧棲區中正國民小學 115年度STEAM教師專業學習社群
## 成果展現場發表一頁備忘單（CheatSheet · 22頁旗艦版極簡速查）

- **發表時間**：115 年 12 月 18 日（五）上午成果展
- **發表限時**：5 分鐘（目標嚴控於 4:45 ～ 4:58 之間，預留 5 秒安全餘裕）
- **發表人**：謝敦元 老師（社群召集人）
- **主軸口號**：**積木啟發量感 · 機關驗證平衡 —— 讓抽象數學量感，在積木咔嗒聲中看得見、摸得到！**

---

### ⏱️ 22 頁精準節奏速查表（平均每頁 13~14 秒 · 圍繞社群研發作為）

| 頁次 | 標題簡述 | 建議時間點 | 核心講述關鍵字（一眼提示，切勿看稿死背） |
| :--- | :--- | :--- | :--- |
| **S01** | 封面啟動 | `00:00 - 00:15` | 評審好，中正國小謝敦元，智高天平「看得見、摸得到」！ |
| **S02** | 社群脈絡 | `00:15 - 00:30` | 4師協同、7場活動、16節課、16,000元100%精準結報！ |
| **S03** | 全景地圖 | `00:30 - 00:43` | 研發4階段：教材剖析、教具自製、試教實證、競賽典藏！ |
| **S04** | 研發動機 | `00:43 - 00:56` | 突破市售黑盒子彈簧秤，自研透明結構等臂天平！ |
| **S05** | 課綱轉化 | `00:56 - 01:09` | n-II-8(5g基底)、n-II-9(20孔等臂)、n-II-2(加減算則)三大指標！ |
| **S06** | 三節架構 | `01:09 - 01:23` | 階梯探究：1節手感衝突、2節機構組裝、3節公克微調！ |
| **S07** | 教學設計1| `01:23 - 01:36` | 盲測大保麗龍 vs 小鐵球破除視覺，手腕疲勞引爆天平需求！ |
| **S08** | 教具研發2| `01:36 - 01:50` | 梯形基座、20孔對稱橫樑、低阻尼轉軸、雙吊盤四核心組件！ |
| **S09** | 技術突破 | `01:50 - 02:03` | 轉軸除錯消除阻尼達2g靈敏度，增設零點鉛直基準線消除誤差！ |
| **S10** | 觀課議課 | `02:03 - 02:16` | 三年丙班公開課100%實作，議課決策插銷卡榫確保左右等高！ |
| **S11** | 教學設計3| `02:16 - 02:29` | 智高標準積木每顆5g，數算顆數乘5，生活秤量任務單破解！ |
| **S12** | 教材轉化 | `02:29 - 02:42` | 天平左傾補積木(加法補足)、去皮算重拿掉積木(減法移除)！ |
| **S13** | 成效對比 | `02:42 - 02:58` | **[演示滑桿]** 左拖回顧傳統困境，右拖展現社群新典範(+28.5%)！ |
| **S14** | 縱向延展1| `02:58 - 03:12` | 四年級 micro:bit 甩繩神射手，藍牙廣播串流加速度折線圖！ |
| **S15** | 縱向延展2| `03:12 - 03:26` | 天平改裝重力觸發開關，世界機關王8迴連鎖，培訓12位梯隊！ |
| **S16** | 回憶錄 1 | `03:26 - 03:40` | 0520社群啟動剖析迷思、第一代天平原型機組裝克服摩擦！ |
| **S17** | 回憶錄 2 | `03:40 - 03:54` | 0810參訪南投鯉魚國小，陳建安名師指導機構傳動與模組管理！ |
| **S18** | 回憶錄 3 | `03:54 - 04:08` | 0926天平轉軸阻尼校正定規鉛直基準線、1001 micro:bit科技跨域共備！ |
| **S19** | 回憶錄 4 | `04:08 - 04:22` | 1005試教前後測答對率升28.5%、增設鉛直基準線定稿二代教具！ |
| **S20** | 回憶錄 5 | `04:22 - 04:36` | 1019機關王8迴連續觸發測試、四位教師圓滿完工大合影！ |
| **S21** | 回憶錄 6 | `04:36 - 04:50` | 附件6教案設計送件典藏、等臂天平工程規格藍圖與三階素養規準！ |
| **S22** | 結語展望 | `04:50 - 05:00` | 理解度+28.5%、滿意度96.8%！感謝教育局與輔導團隊，謝謝大家！ |

---

### 💡 評審提問攻防應答錦囊（Q&A 備戰）
1. **問：市售天平那麼多，為何社群要大費周章自己用智高積木研發教具？**
   - **答**：市售天平是「完成品黑盒子」，指針歸零學生只當成規矩機械去轉，壞了不會修、偏了不知道為什麼。社群研發自製天平能讓孩子親自看見轉軸摩擦力、力臂長度對稱性與力矩平衡，是將「物理科學」與「數學量感」深度整合的靈魂所在！
2. **問：如何在 3 節課內兼顧「積木組裝」與「數學課綱進度」？會不會壓縮算則教學？**
   - **答**：完全不會！社群客製專用分裝盤，第 2 節組裝僅需 12 分鐘；而且正是因為孩子在天平上親眼看見「加法補足」與「去皮減法」，第 3 節處理兩步驟文字題時反而完全省去抽象講解的時間，學習效率大幅躍升！
3. **問：本教案在其他沒有大量智高積木的學校，具備推廣可行性嗎？**
   - **答**：高度可行！本教案附件 6 所載天平機構僅需 20 孔長條橫樑、梯形基座與簡單轉軸軸套，單組成本極低，亦可使用生活垂手可得之洞洞板或 3D 列印套件替換，我們更已將組裝圖與評量單無償開源共享！
"""

# 寫入 Markdown 檔案
transcript_path = os.path.join(DOC_DIR, "5分鐘發表逐字講稿_含計時標記.md")
cheatsheet_path = os.path.join(DOC_DIR, "成果展一頁備忘單_CheatSheet.md")

with open(transcript_path, "w", encoding="utf-8") as f:
    f.write(MD_TRANSCRIPT.strip())
print(f"[OK] Written {transcript_path}")

with open(cheatsheet_path, "w", encoding="utf-8") as f:
    f.write(MD_CHEATSHEET.strip())
print(f"[OK] Written {cheatsheet_path}")

def set_cell_background(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=130, right=130):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

# 1. 逐字稿 DOCX
doc_t = docx.Document()
section_t = doc_t.sections[0]
section_t.top_margin = Inches(0.7)
section_t.bottom_margin = Inches(0.7)
section_t.left_margin = Inches(0.8)
section_t.right_margin = Inches(0.8)

p_h = doc_t.add_paragraph()
p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_h = p_h.add_run("臺中市梧棲區中正國民小學 115年度STEAM教師專業學習社群")
r_h.font.name = "微軟正黑體"
r_h.font.size = Pt(12)
r_h.font.bold = True
r_h.font.color.rgb = RGBColor(2, 132, 199)

p_t = doc_t.add_paragraph()
p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_t = p_t.add_run("成果展 5 分鐘現場發表逐字講稿（22 頁旗艦版 · 聚焦社群研發作為）")
r_t.font.name = "微軟正黑體"
r_t.font.size = Pt(18)
r_t.font.bold = True
r_t.font.color.rgb = RGBColor(15, 23, 42)

p_meta = doc_t.add_paragraph()
p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_m = p_meta.add_run("發表人：謝敦元 老師 ｜ 社群夥伴：王怡婷、李仁耀、曾泊淞 ｜ 限時 5 分鐘（目標 4:50）")
r_m.font.name = "微軟正黑體"
r_m.font.size = Pt(10.5)
r_m.font.color.rgb = RGBColor(100, 116, 139)

doc_t.add_paragraph().paragraph_format.space_after = Pt(8)

sections = re.findall(r'### (【[\d:]+ - [\d:]+】Slide \d+ [^\n]+)\n> \*\*\[([^\]]+)\]\*\*\n>\s*\n((?:> [^\n]*\n*)+)', MD_TRANSCRIPT)
for header, cue, content in sections:
    table = doc_t.add_table(rows=2, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell_h = table.cell(0, 0)
    cell_h.width = Inches(6.8)
    set_cell_background(cell_h, "0284C7")
    set_cell_margins(cell_h, top=80, bottom=80, left=140, right=140)
    p_ch = cell_h.paragraphs[0]
    r_ch = p_ch.add_run(f"{header}  |  提示：{cue}")
    r_ch.font.name = "微軟正黑體"
    r_ch.font.size = Pt(11)
    r_ch.font.bold = True
    r_ch.font.color.rgb = RGBColor(255, 255, 255)
    
    cell_b = table.cell(1, 0)
    cell_b.width = Inches(6.8)
    set_cell_background(cell_b, "F8FAFC")
    set_cell_margins(cell_b, top=100, bottom=100, left=140, right=140)
    clean_lines = [re.sub(r'^>\s*', '', line).strip() for line in content.strip().splitlines() if line.strip()]
    p_cb = cell_b.paragraphs[0]
    p_cb.paragraph_format.line_spacing = 1.3
    p_cb.paragraph_format.space_after = Pt(4)
    for line in clean_lines:
        line_clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', line)
        r = p_cb.add_run(line_clean + " ")
        r.font.name = "微軟正黑體"
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(15, 23, 42)
    
    doc_t.add_paragraph().paragraph_format.space_after = Pt(6)

docx_t_path = os.path.join(DOC_DIR, "臺中市梧棲區中正國小_STEAM成果展_5分鐘現場發表逐字講稿(含計時標記).docx")
doc_t.save(docx_t_path)
print(f"[OK] Generated {docx_t_path}")

# 2. CheatSheet DOCX
doc_c = docx.Document()
section_c = doc_c.sections[0]
section_c.top_margin = Inches(0.5)
section_c.bottom_margin = Inches(0.5)
section_c.left_margin = Inches(0.6)
section_c.right_margin = Inches(0.6)

p_ch_t = doc_c.add_paragraph()
p_ch_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_c1 = p_ch_t.add_run("臺中市梧棲區中正國小 STEAM 教師社群成果展 ｜ 5分鐘現場發表一頁備忘單（CheatSheet 22頁旗艦版）\n")
r_c1.font.name = "微軟正黑體"
r_c1.font.size = Pt(13)
r_c1.font.bold = True
r_c1.font.color.rgb = RGBColor(2, 132, 199)

r_c2 = p_ch_t.add_run("發表人：謝敦元 老師 ｜ 限時 5 分鐘（目標 4:50） ｜ 口號：讓抽象數學量感，在積木咔嗒聲中看得見、摸得到！")
r_c2.font.name = "微軟正黑體"
r_c2.font.size = Pt(9.5)
r_c2.font.color.rgb = RGBColor(100, 116, 139)

doc_c.add_paragraph().paragraph_format.space_after = Pt(4)

table_c = doc_c.add_table(rows=23, cols=4)
table_c.alignment = WD_TABLE_ALIGNMENT.CENTER
table_c.autofit = False

col_widths = [Inches(0.7), Inches(1.3), Inches(1.2), Inches(3.8)]
headers = ["頁次", "標題簡述", "建議時間點", "核心講述關鍵字（一眼提示）"]

for c_idx, h in enumerate(headers):
    cell = table_c.cell(0, c_idx)
    cell.width = col_widths[c_idx]
    set_cell_background(cell, "0284C7")
    set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
    p = cell.paragraphs[0]
    r = p.add_run(h)
    r.font.name = "微軟正黑體"
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(255, 255, 255)

table_rows = re.findall(r'\| \*\*([^*]+)\*\* \| ([^|]+) \| `([^`]+)` \| ([^|]+) \|', MD_CHEATSHEET)
for r_idx, (p_num, title, t_range, key_points) in enumerate(table_rows, 1):
    row_bg = "FFFFFF" if r_idx % 2 == 1 else "F8FAFC"
    vals = [p_num, title.strip(), t_range.strip(), key_points.strip()]
    for c_idx, val in enumerate(vals):
        cell = table_c.cell(r_idx, c_idx)
        cell.width = col_widths[c_idx]
        set_cell_background(cell, row_bg)
        set_cell_margins(cell, top=40, bottom=40, left=60, right=60)
        p = cell.paragraphs[0]
        r = p.add_run(val)
        r.font.name = "微軟正黑體"
        r.font.size = Pt(8.5)
        if c_idx == 0:
            r.font.bold = True
            r.font.color.rgb = RGBColor(2, 132, 199)
        elif c_idx == 2:
            r.font.bold = True
            r.font.color.rgb = RGBColor(234, 88, 12)
        else:
            r.font.color.rgb = RGBColor(15, 23, 42)

docx_c_path = os.path.join(DOC_DIR, "臺中市梧棲區中正國小_STEAM成果展_一頁精華備忘單(CheatSheet).docx")
doc_c.save(docx_c_path)
print(f"[OK] Generated {docx_c_path}")

try:
    import win32com.client
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    
    for docx_p in [docx_t_path, docx_c_path]:
        pdf_p = docx_p.replace(".docx", ".pdf")
        doc = word.Documents.Open(os.path.abspath(docx_p))
        doc.SaveAs(os.path.abspath(pdf_p), FileFormat=17)
        doc.Close()
        print(f"[OK] Converted to PDF: {pdf_p}")
    word.Quit()
except Exception as e:
    print(f"[NOTE] win32com PDF conversion skipped or failed: {e}")
