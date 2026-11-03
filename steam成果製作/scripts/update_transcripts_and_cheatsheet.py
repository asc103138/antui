#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新 22 頁旗艦版發表逐字講稿與 CheatSheet，並生成 .docx 與 .pdf
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
## 成果展 5 分鐘現場發表逐字講稿（22 頁旗艦版 · 含每頁計時標記與換頁提示）

- **發表學校**：臺中市梧棲區中正國民小學
- **社群召集人 / 發表人**：謝敦元 老師
- **社群夥伴**：王怡婷 老師、李仁耀 老師、曾泊淞 老師
- **教案主題**：積木啟發量感 · 機關驗證平衡 —— 智高積木融入三年級重量測量機關課程
- **發表總時長**：嚴格控制於 **4 分 45 秒 ～ 4 分 58 秒**（合規上限 5 分鐘，平均每頁約 13~14 秒）

---

### 【00:00 - 00:15】Slide 1 封面：積木啟發量感 · 機關驗證平衡
> **[投影片：Slide 1 封面]**
> 
> 各位評審委員、教育先進大家好！我是中正國小社群召集人謝敦元。今天代表我們社群四位老師，向各位分享我們這一年深耕的三年級跨域教案——**「積木啟發量感 · 機關驗證平衡」**。我們的核心理念是：**讓抽象的數學量感，在積木咔嗒聲中看得見、摸得到！**

---

### 【00:15 - 00:30】Slide 2 社群推動脈絡：踏實共備與 100% 執行
> **[按鍵換頁 ➜ Slide 2 社群推動脈絡]**
> 
> 本社群由我與王怡婷、李仁耀、曾泊淞老師跨數學、自然與資訊協同。從 5 月到 10 月扎實推動 7 場研習與公開觀議課，16 節課程 16,000 元經費全額無瑕結報；更特聘南投鯉魚國小陳建安名師跨校交流，展現中正國小強大共備動能！

---

### 【00:30 - 00:43】Slide 3 現場互動提問：提到重量測量，學生最常卡在哪？
> **[按鍵換頁 ➜ Slide 3 現場互動文字雲]**
> 
> （現場邀請各位老師看大螢幕文字雲）在教三年級重量時，孩子最常踩到什麼坑？我們發現全班回饋高頻集中在：**指針沒歸零看錯刻度**佔 32%、**刻度小格值讀錯**佔 38%、**公斤公克換算障礙**佔 24%。這反映出市售彈簧秤就像「黑盒子」，學生只死背數字，缺乏物理實體感知！

---

### 【00:43 - 00:56】Slide 4 教學痛點診斷：從黑盒子讀數到物理具象
> **[按鍵換頁 ➜ Slide 4 教學痛點診斷]**
> 
> 我們深入診斷三大課堂壁壘：第一，刻度密密麻麻，學生常把一小格誤判為 10g；第二，1 公斤等於 1000 公克淪為機械死背，換算失靈；第三，課本題目兩步驟加減缺乏實作，無法連結買菜等真實生活。

---

### 【00:56 - 01:09】Slide 5 課程核心依據：十二年國教數學領域指標對齊
> **[按鍵換頁 ➜ Slide 5 課綱指標對齊]**
> 
> 本教案緊密對齊十二年國教課綱三大指標：**n-II-8** 認識公克與公斤；**n-II-9** 理解等臂天平原理；以及 **n-II-2** 兩步驟加減問題。我們將課綱條目轉化為「智高積木手作調校」，落實素養導向！

---

### 【01:09 - 01:23】Slide 6 三節課循序進階架構：階梯式探究地圖
> **[按鍵換頁 ➜ Slide 6 三節課循序進階架構]**
> 
> 我們設計三節循序漸進的階梯架構：第 1 節「徒手掂重引爆認知衝突」；第 2 節「智高積木等臂機構組裝」；第 3 節「公克積木微調與生活應用」，形成由感官、機構到計量的完整探究閉環。

---

### 【01:23 - 01:36】Slide 7 第 1 節課堂實踐：徒手掂重引爆認知衝突
> **[按鍵換頁 ➜ Slide 7 第 1 節課堂實踐]**
> 
> 第一節上課，我們給學生大保麗龍方塊和小金屬球。92% 學生直覺以為大的一定重；但一閉眼盲測，掌心下沉的竟然是小鐵球！體積迷思瞬間打破。隨後雙手掂重時手腕疲勞，全班一致驚呼：「我們需要客觀、不會累的天平！」

---

### 【01:36 - 01:50】Slide 8 第 2 節課堂實踐：智高積木四核心組件組裝
> **[按鍵換頁 ➜ Slide 8 第 2 節課堂實踐]**
> 
> 第二節課化身小小工程師！學生動手組裝四大核心組件：梯形穩固基座、左右各 10 孔完全對稱橫樑、極低摩擦的轉軸軸套，以及垂直懸吊的雙測量盤。孩子在除錯卡榫中，深刻體會結構平衡的力學之美。

---

### 【01:50 - 02:03】Slide 9 物理機制解析：天平傾斜與指針判定規則
> **[按鍵換頁 ➜ Slide 9 物理機制解析]**
> 
> 我們建立清楚的力學指針語言：左盤下沉代表左邊重、右盤下沉代表右邊重；當且僅當指針垂直於中線基準時，兩側力矩完全相等！孩子親手調整零點，不再需要死記教條。

---

### 【02:03 - 02:16】Slide 10 課堂迷思快問快答：破除體積大就一定重
> **[按鍵換頁 ➜ Slide 10 課堂迷思快問快答]**
> 
> （與台下互動）請看大螢幕快問：左邊放大棉花團、右邊放小金屬塊，指針垂直平衡，誰重？課前有 38% 學生誤選棉花；課後高達 98% 孩子立刻大喊：「指針鉛直，兩者一樣重！」物理直覺完全扎根！

---

### 【02:16 - 02:29】Slide 11 第 3 節課堂實踐：單位積木與加減微調挑戰
> **[按鍵換頁 ➜ Slide 11 第 3 節課堂實踐]**
> 
> 第三節課引導個別單位走向標準單位。每顆智高標準積木恰為 5 公克！孩子放上 1 顆就是 5g、2 顆就是 10g，數算顆數乘 5，把抽象的乘法與公克讀數無縫串聯！

---

### 【02:29 - 02:42】Slide 12 課堂深度探究：兩步驟加減法情境具象化
> **[按鍵換頁 ➜ Slide 12 課堂深度探究]**
> 
> 課本最難的兩步驟問題，在天平上迎刃而解！左盤 50g、右盤 35g，天平左傾，孩子立刻動手補進 3 顆積木（加法補足）；計算空紙盒去皮重時，直接從盤中拿掉積木（減法移除），算則完全內化為肌肉記憶！

---

### 【02:42 - 02:58】Slide 13 教學典範轉移：傳統讀秤 vs STEAM 動手調校
> **[按鍵換頁 ➜ Slide 13 典範轉移 3D 對比滑桿]**
> 
> （拖曳滑桿演示）請看左右對比：傳統課堂學生面對市售黑盒子秤，指針未歸零讀錯刻度，缺乏實體感知；而在 STEAM 課堂，孩子親手組裝、逐顆微調，前後測理解度大躍升 28.5%，探究自信心爆棚！這就是最徹底的教學典範轉移！

---

### 【02:58 - 03:12】Slide 14 社群成果縱向延展 (一)：四年級 micro:bit 甩繩智動量測
> **[按鍵換頁 ➜ Slide 14 成果縱向延展 micro:bit]**
> 
> 社群成果不只停留在三年級！李仁耀老師將感測概念延伸至四年級，開發「micro:bit 甩繩軌跡神射手」，利用 3 軸加速度計即時感測跳繩震盪，以藍牙廣播串流大數據，繪製體適能統計折線圖，跨域體育大獲好評！

---

### 【03:12 - 03:26】Slide 15 社群成果縱向延展 (二)：世界機關王 (GM) 校隊梯隊
> **[按鍵換頁 ➜ Slide 15 成果縱向延展 世界機關王]**
> 
> 更令人振奮的是，我們將天平微型槓桿改裝為「重力傾斜開關」，串聯複合減速齒輪箱與軌道，完成世界機關王指定之 8 迴連續連鎖關卡！成功培訓 12 位校隊梯隊小創客，穩定度超越 90%！

---

### 【03:26 - 03:40】Slide 16 社群歷程回憶錄 (一)：萌芽共備與原型研發
> **[按鍵換頁 ➜ Slide 16 社群歷程回憶錄 (一)]**
> 
> 接下來向大家呈現中正國小社群的踏實足跡。第一張照片記錄 5 月 20 日社群啟動，四位教師齊聚拆解數學迷思；第二張則是第一代智高天平原型機組裝測試，克服卡榫摩擦，奠定整年研發基石。

---

### 【03:40 - 03:54】Slide 17 社群歷程回憶錄 (二)：校際參訪與創客交流
> **[按鍵換頁 ➜ Slide 17 社群歷程回憶錄 (二)]**
> 
> 8 月 10 日我們走出校園，親赴南投鯉魚國小創客基地，特聘世界機關王金牌教練陳建安老師深度座談。陳老師傾囊相授機構傳動與模組管理，讓我們成功將競賽級技術降轉為國小日常課堂教具！

---

### 【03:54 - 04:08】Slide 18 社群歷程回憶錄 (三)：課堂實踐與公開觀議課
> **[按鍵換頁 ➜ Slide 18 社群歷程回憶錄 (三)]**
> 
> 9 月 26 日在三年丙班進行公開觀課，黑板清晰架構公斤與公克量感階梯，學生全神貫注操作天平；10 月 1 日四年級 micro:bit 科技實測，學生奔馳於操場採集動態數據，展現跨域學習熱情！

---

### 【04:08 - 04:22】Slide 19 社群歷程回憶錄 (四)：成效研析與機關精進
> **[按鍵換頁 ➜ Slide 19 社群歷程回憶錄 (四)]**
> 
> 10 月 5 日曾泊淞與我共同主持成效研討，逐題比對前後測試卷，數據證實理解度提升 28.5%！我們更針對指針阻尼與刻度增設「鉛直基準線」，完成第二代標準化天平教具。

---

### 【04:22 - 04:36】Slide 20 社群歷程回憶錄 (五)：機關王 8 迴整合與團隊合影
> **[按鍵換頁 ➜ Slide 20 社群歷程回憶錄 (五)]**
> 
> 10 月 19 日在活動中心進行機關王 A-H 區 8 迴機構連鎖測試，鋼珠順暢觸發天平開關！右側是我們四位教師圓滿完工的燦爛合影，16 節課程 16,000 元無瑕結報，凝聚了無比堅實的團隊情誼！

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

### ⏱️ 22 頁精準節奏速查表（平均每頁 13~14 秒）

| 頁次 | 標題簡述 | 建議時間點 | 核心講述關鍵字（一眼提示，切勿看稿死背） |
| :--- | :--- | :--- | :--- |
| **S01** | 封面啟動 | `00:00 - 00:15` | 評審好，中正國小謝敦元，智高天平「看得見、摸得到」！ |
| **S02** | 社群脈絡 | `00:15 - 00:30` | 4師協同、7場活動、16節課、16,000元100%精準結報！ |
| **S03** | 現場互動 | `00:30 - 00:43` | 大螢幕文字雲：指針未歸零32%、讀錯刻度38%，黑盒子困境！ |
| **S04** | 痛點診斷 | `00:43 - 00:56` | 刻度密麻、單位換算機械背誦、兩步驟加減脫離真實生活！ |
| **S05** | 課綱對齊 | `00:56 - 01:09` | n-II-8(公克)、n-II-9(等臂天平)、n-II-2(加減算則)三大指標！ |
| **S06** | 三節架構 | `01:09 - 01:23` | 階梯探究：1節手感衝突、2節機構組裝、3節公克微調！ |
| **S07** | 第 1 節 | `01:23 - 01:36` | 大保麗龍 vs 小鐵球，體積大反而輕！手腕疲勞引爆天平需求！ |
| **S08** | 第 2 節 | `01:36 - 01:50` | 梯形底座、20孔對稱橫樑、低阻尼轉軸、雙吊盤四核心組件！ |
| **S09** | 物理機制 | `01:50 - 02:03` | 左盤沉左重、右盤沉右重，鉛直中線達成力矩平衡客觀判讀！ |
| **S10** | 迷思快問 | `02:03 - 02:16` | 大棉花 vs 小金屬，課前38%錯選，課後98%秒答「一樣重」！ |
| **S11** | 第 3 節 | `02:16 - 02:29` | 智高標準積木每顆5g，數算顆數乘5，非標準跨越到標準單位！ |
| **S12** | 深度探究 | `02:29 - 02:42` | 天平左傾補積木(加法補足)、去皮算重拿掉積木(減法移除)！ |
| **S13** | 典範轉移 | `02:42 - 02:58` | **[拖動3D滑桿]** 傳統黑盒子讀數 vs STEAM親手調校，提升28.5%！ |
| **S14** | 縱向延展1| `02:58 - 03:12` | 四年級 micro:bit 甩繩神射手，藍牙廣播串流加速度折線圖！ |
| **S15** | 縱向延展2| `03:12 - 03:26` | 天平改裝重力觸發開關，世界機關王8迴連鎖，培訓12位梯隊！ |
| **S16** | 回憶錄 1 | `03:26 - 03:40` | 0520社群啟動剖析迷思、第一代天平原型機組裝克服摩擦！ |
| **S17** | 回憶錄 2 | `03:40 - 03:54` | 0810參訪南投鯉魚國小，陳建安名師指導機構傳動與模組管理！ |
| **S18** | 回憶錄 3 | `03:54 - 04:08` | 0926三年丙班公開課板書量感階梯、1001 micro:bit科技實測！ |
| **S19** | 回憶錄 4 | `04:08 - 04:22` | 1005試教前後測答對率升28.5%、增設鉛直基準線定稿二代教具！ |
| **S20** | 回憶錄 5 | `04:22 - 04:36` | 1019機關王8迴連續觸發測試、四位教師圓滿完工大合影！ |
| **S21** | 回憶錄 6 | `04:36 - 04:50` | 附件6教案設計送件典藏、等臂天平工程規格藍圖與三階素養規準！ |
| **S22** | 結語展望 | `04:50 - 05:00` | 理解度+28.5%、滿意度96.8%！感謝教育局與輔導團隊，謝謝大家！ |

---

### 💡 評審提問攻防應答錦囊（Q&A 備戰）
1. **問：市售天平那麼多，為何要大費周章讓學生自己用智高積木組裝？**
   - **答**：市售天平是「完成品黑盒子」，指針歸零學生只當成規矩機械去轉，壞了不會修、偏了不知道為什麼。自己組裝能讓孩子親自看見轉軸摩擦力、力臂長度對稱性與力矩平衡，是將「物理科學」與「數學量感」深度整合的靈魂所在！
2. **問：如何在 3 節課內兼顧「積木組裝」與「數學課綱進度」？會不會壓縮算則教學？**
   - **答**：完全不會！我們採用預先分類的專用盒（減速零件已歸類），第 2 節組裝僅需 15 分鐘；而且正是因為孩子在天平上親眼看見「加法補足」與「去皮減法」，第 3 節處理兩步驟文字題時反而完全省去抽象講解的時間，學習效率大幅躍升！
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

# 生成 DOCX
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
r_t = p_t.add_run("成果展 5 分鐘現場發表逐字講稿（22 頁旗艦版）")
r_t.font.name = "微軟正黑體"
r_t.font.size = Pt(20)
r_t.font.bold = True
r_t.font.color.rgb = RGBColor(15, 23, 42)

p_meta = doc_t.add_paragraph()
p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_m = p_meta.add_run("發表人：謝敦元 老師 ｜ 社群夥伴：王怡婷、李仁耀、曾泊淞 ｜ 限時 5 分鐘（目標 4:50）")
r_m.font.name = "微軟正黑體"
r_m.font.size = Pt(10.5)
r_m.font.color.rgb = RGBColor(100, 116, 139)

doc_t.add_paragraph().paragraph_format.space_after = Pt(8)

# 解析每段投影片
sections = re.findall(r'### (【[\d:]+ - [\d:]+】Slide \d+ [^\n]+)\n> \*\*\[([^\]]+)\]\*\*\n>\s*\n((?:> [^\n]*\n*)+)', MD_TRANSCRIPT)
for header, cue, content in sections:
    table = doc_t.add_table(rows=2, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    # 標題列
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
    
    # 內文列
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

# 插入 22 頁速查表格
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

# 嘗試轉 PDF (Windows win32com)
try:
    import win32com.client
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    
    for docx_p in [docx_t_path, docx_c_path]:
        pdf_p = docx_p.replace(".docx", ".pdf")
        doc = word.Documents.Open(os.path.abspath(docx_p))
        doc.SaveAs(os.path.abspath(pdf_p), FileFormat=17) # 17 = wdFormatPDF
        doc.Close()
        print(f"[OK] Converted to PDF: {pdf_p}")
    word.Quit()
except Exception as e:
    print(f"[NOTE] win32com PDF conversion skipped or failed: {e}")
