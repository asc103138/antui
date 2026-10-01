import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for margin_name, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{margin_name}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="D0D5DD", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def apply_font(run, font_name="微軟正黑體", size_pt=10.5, bold=False, italic=False, color_rgb=(51,51,51)):
    run.font.name = font_name
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:eastAsia'), font_name)
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(*color_rgb)

def add_h1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    apply_font(run, size_pt=14.5, bold=True, color_rgb=(15, 44, 89))
    return p

def add_h2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    apply_font(run, size_pt=12, bold=True, color_rgb=(30, 64, 175))
    return p

def add_p(doc, text, bold_prefix=None, italic=False, color_rgb=(51,65,85)):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        apply_font(r_pre, size_pt=10, bold=True, color_rgb=(30,41,59))
    run = p.add_run(text)
    apply_font(run, size_pt=10, bold=False, italic=italic, color_rgb=color_rgb)
    return p

def add_bullet(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        apply_font(r_pre, size_pt=10, bold=True, color_rgb=(30, 41, 59))
    run = p.add_run(text)
    apply_font(run, size_pt=10, bold=False, color_rgb=(51, 65, 85))
    return p

def build_class_4c_docx(out_path):
    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(0.7)
        section.bottom_margin = Inches(0.7)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    # 封面大標題
    p_t = doc.add_paragraph()
    p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t.paragraph_format.space_before = Pt(4)
    p_t.paragraph_format.space_after = Pt(2)
    r_t = p_t.add_run("臺中市梧棲區中正國小 115 學年度校內語文競賽")
    apply_font(r_t, size_pt=17, bold=True, color_rgb=(15, 44, 89))

    p_s = doc.add_paragraph()
    p_s.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_s.paragraph_format.space_before = Pt(0)
    p_s.paragraph_format.space_after = Pt(12)
    r_s = p_s.add_run("【四年丙班】專屬選手培訓教學指引：在校每日集訓與回家作業手冊")
    apply_font(r_s, size_pt=12.5, bold=True, color_rgb=(194, 65, 12))

    # 說明引言
    p_intro = doc.add_paragraph()
    r_in = p_intro.add_run("本手冊專為四年丙班（四丙）級任導師與選手量身打造。嚴格過濾高年級非相關篇目，全手冊明確分為【在校教學練習】（早自修與午休導師實操教案）與【回家作業】（學生每日功課與家長簽章）兩大專區。")
    apply_font(r_in, size_pt=9.5, italic=True, color_rgb=(71, 85, 105))

    # 壹、四丙項目與篇目
    add_h1(doc, "壹、四年丙班專屬參賽項目與指定內容總覽")
    
    events_data = [
        ["競賽項目", "比賽日期與時間", "時限", "地點", "四年丙班專屬內容與出題來源"],
        ["寫字（書法）", "115.11.05（四）08:20-09:20", "60分", "圖書室", "指定28字楷書＋落款：臺中市梧棲區中正國小四年丙班 ○○○書"],
        ["作　文", "115.11.05（四）08:00-09:30", "90分", "視聽教室", "現場公佈題目，傳統稿紙書寫，記敘與成長體悟（目標600~800字）"],
        ["國語字音字形", "115.11.05（四）12:40-12:50", "10分", "視聽教室", "200字（音100/形100），112~114全國賽試題，塗改一律不計分"],
        ["國語朗讀", "115.11.12（四）08:10-09:20", "2分", "簡報室", "四年級唯一指定篇目：林清玄〈藍蝴蝶〉（配速線約400字）"],
        ["臺灣台語朗讀", "115.11.12（四）08:10-09:20", "2分", "校史室", "四年級唯一指定篇目：周世雄〈04 阿公變魔術〉（免抽籤！精練此篇）"],
        ["國語演說", "115.11.19（四）08:10-09:20", "2分", "簡報室", "二擇一：《如果同學做了不對的事》、《我最喜歡的卡通人物》（420字）"],
        ["臺灣台語情境演說", "115.11.19（四）08:10-09:20", "2分+問答", "校史室", "題目：〈食中晝〉＋ 評判委員現場即席台語問答（Q&A）"]
    ]
    t_ev = doc.add_table(rows=len(events_data), cols=5)
    t_ev.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_ev)
    w_ev = [Inches(1.2), Inches(1.5), Inches(0.6), Inches(0.8), Inches(2.9)]
    for r_i, r_d in enumerate(events_data):
        row = t_ev.rows[r_i]
        for c_i, c_t in enumerate(r_d):
            cell = row.cells[c_i]
            cell.width = w_ev[c_i]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_margins(cell, top=70, bottom=70, left=70, right=70)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i in [0, 2, 3] else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(c_t)
            if r_i == 0:
                set_cell_background(cell, "1E3A8A")
                apply_font(run, size_pt=9, bold=True, color_rgb=(255, 255, 255))
            else:
                if r_i % 2 == 1:
                    set_cell_background(cell, "F8FAFC")
                apply_font(run, size_pt=8.5, bold=(c_i==0), color_rgb=(30, 41, 59))

    # 貳、導師輪替集訓表
    add_h1(doc, "貳、導師專用：早自修與午休每週輪替集訓排程總表")
    add_p(doc, "落實「早修 35 分鐘（08:00~08:35）＋ 午休前段 35 分鐘（12:40~13:15）」微型集訓，分組輪替、互不干擾、零衝堂：", italic=True)

    sched_data = [
        ["集訓時段", "星期一", "星期二", "星期三", "星期四", "星期五"],
        [
            "早自修\n08:00-08:35\n(35分鐘)",
            "【國語朗讀】\n〈藍蝴蝶〉正音斷句\n（字音字形在旁自測）",
            "【國語演說】\n講稿分段脫稿背誦\n（作文寫100字段落）",
            "【筆試雙軌模擬】\n作文：5分鐘大綱\n字音字形：10分鐘模考",
            "【台語朗讀】\n〈阿公變魔術〉\n台羅變調與入聲收音",
            "【口語演繹快說】\n台語情境演說快說\n國語演說鈴聲收尾"
        ],
        [
            "午休前段\n12:40-13:15\n(35分鐘)",
            "【寫字書法組】\n毛筆提按、九宮格\n（其他選手安靜午休）",
            "【台語情境演說】\n動作身段演繹\n即席問答抽問指導",
            "（全校教師研習日）\n選手自主背誦自學\n不排定集中培訓",
            "【字音字形衝刺】\n10分鐘全真模考\n【作文】導師面批",
            "【動態選手大驗收】\n全體登台走位禮儀\n2分鐘鈴聲下台實戰"
        ]
    ]
    t_sc = doc.add_table(rows=len(sched_data), cols=6)
    t_sc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_sc)
    w_sc = [Inches(1.1), Inches(1.18), Inches(1.18), Inches(1.18), Inches(1.18), Inches(1.18)]
    for r_i, r_d in enumerate(sched_data):
        row = t_sc.rows[r_i]
        for c_i, c_t in enumerate(r_d):
            cell = row.cells[c_i]
            cell.width = w_sc[c_i]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_margins(cell, top=80, bottom=80, left=70, right=70)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i == 0 or r_i == 0 else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(c_t)
            if r_i == 0:
                set_cell_background(cell, "2563EB")
                apply_font(run, size_pt=9, bold=True, color_rgb=(255, 255, 255))
            else:
                if c_i == 0:
                    set_cell_background(cell, "EFF6FF")
                    apply_font(run, size_pt=8.5, bold=True, color_rgb=(30, 58, 138))
                else:
                    apply_font(run, size_pt=8, bold=False, color_rgb=(30, 41, 59))

    doc.add_page_break()

    # ==============================
    # 第一部：在校教學練習專區
    # ==============================
    add_h1(doc, "【第一部：在校教學練習專區】（導師在校教學實操教案）")

    # 單元一：寫字
    add_h2(doc, "單元一：寫字（書法）組——在校教學操作教案")
    add_p(doc, "訓練時段：每週一午休（12:40~13:15）、每週四早自修排版指導。題目：「拒絕毒品愛自己 反對霸凌不旁觀 減速慢行少意外 共創和諧好未來」＋ 落款（中正國小四年丙班 ○○○書）。")
    add_bullet(doc, "第1步（5分鐘）：調息與執筆校正。檢查雙苞執筆法、懸腕、上身坐正、雙腳踏實。", "［執筆坐姿］")
    add_bullet(doc, "第2步（10分鐘）：黑板結構拆解。「毒」長橫微仰如展翅；「霸」雨字扁平月革中宮緊聚；「速」走之平捺三折；「未」上橫短下橫長（禁作末）。", "［結構點撥］")
    add_bullet(doc, "第3步（15分鐘）：九宮格個別指導。手把手微調回鋒收筆、折角頓挫與行氣連貫。", "［提按實作］")
    add_bullet(doc, "第4步（5分鐘）：宣紙折格與落款。指導 70cm×35cm 四開紙折四行七列＋左側落款格，示範落款小楷。", "［折格章法］")

    # 單元二：作文
    add_h2(doc, "單元二：作文組——在校教學操作教案")
    add_p(doc, "訓練時段：每週二早自修（修辭改寫）、週三早自修（大綱速成）、週四午休（個別面批）。")
    add_bullet(doc, "模組A（週三早修）：5分鐘大綱速成心智圖。出題後限時3分鐘在白紙畫出起（破題）、承（背景五感）、轉（矛盾動作特寫）、合（哲理收尾）四格架構。", "［審題立意］")
    add_bullet(doc, "模組B（週二早修）：好句子升級手術。將平淡句（如操場很熱鬧）改寫為「聽覺擬聲＋視覺色彩＋動態修辭」之亮點段落（100字）。", "［修辭雕琢］")
    add_bullet(doc, "模組C（週四午休）：個別面批與除蟲。檢視段首空兩格、剔除口語贅字（如整篇然後）、平衡各段字數（每段約150~200字）。", "［個別面批］")

    # 單元三：國語字音字形
    add_h2(doc, "單元三：國語字音字形組——在校教學操作教案")
    add_p(doc, "訓練時段：每週一、週三早自修（刷題與訂正）、每週四午休（10分鐘極速模考）。題庫：112~114全國賽試卷。")
    add_bullet(doc, "第1步（10分鐘）：高壓極速模考。發下每日 20 題卷（10音+10形），深藍/黑原子筆作答，限時1分鐘內完成（訓練3秒1字），塗改不計分！", "［極速自測］")
    add_bullet(doc, "第2步（5分鐘）：快批算分。每題 0.5 分，立即抓出錯字盲點。", "［精準對改］")
    add_bullet(doc, "第3步（10分鐘）：黑板陷阱拆解。破音字（骨髓ㄙㄨㄟˇ/瓦楞ㄌㄥˊ/勝券ㄑㄩㄢˋ/丱ㄍㄨㄢˋ角/血脈賁ㄅㄣˋ張/肺右不作市/瞥敝部）。", "［考點破譯］")
    add_bullet(doc, "第4步（5分鐘）：錯題口袋卡。將當日錯字抄入錯題卡，在校當天背熟。", "［錯題歸納］")

    # 單元四：國語朗讀
    add_h2(doc, "單元四：國語朗讀組——在校教學操作教案（林清玄〈藍蝴蝶〉）")
    add_p(doc, "訓練時段：每週一早自修（正音斷句）、每週五午休（全真走位）。篇目：四年級唯一指定篇目林清玄〈藍蝴蝶〉。")
    add_bullet(doc, "第1步（8分鐘）：逐段正音。審定「腐木（ㄈㄨˇ）」、「空檔（ㄉㄤˋ）」、「冥想（ㄇㄧㄥˊ）」、「繭（ㄐㄧㄢˇ）」調值精準度。", "［正音精雕］")
    add_bullet(doc, "第2步（10分鐘）：斷句帶讀。「在一個/狹長的●山谷裡/，住了一群●白蝴蝶/，吸食●腐木的汁液維生//」，帶出重音與短停。", "［節奏斷句］")
    add_bullet(doc, "第3步（10分鐘）：聲情轉換。毛毛蟲自問（渴望輕柔）➔ 化蛹冥想（深沉靜謐）➔ 破繭而出展翅（高亢振奮喜悅）。", "［聲情文氣］")
    add_bullet(doc, "第4步（7分鐘）：2分鐘配速。碼表計時，檢核是否恰好在 2 分鐘時抵達第 400 字（璀璨的光澤）。", "［配速控時］")

    # 單元五：臺灣台語朗讀
    add_h2(doc, "單元五：臺灣台語朗讀組——在校教學操作教案（周世雄〈阿公變魔術〉）")
    add_p(doc, "訓練時段：每週四早自修（拼音變調）、每週五午休（全真走位）。篇目：四年級唯一指定篇目周世雄〈04 阿公變魔術〉。")
    add_bullet(doc, "第1步（8分鐘）：官方音檔影子跟讀（Shadowing）。一句接一句跟讀，模仿發音部位與尾韻。", "［聽音跟讀］")
    add_bullet(doc, "第2步（10分鐘）：入聲收音急截。-p（喙瀾㴙㴙滴）、-t（一目𥍉仔）、-h（沓沓仔）；精修「飼豬、刁故意」連續變調。", "［變調入聲］")
    add_bullet(doc, "第3步（10分鐘）：祖孫情口氣（khuì-kháu）。阿公笑咍咍、豬仔鼾鼾叫、隱無sik袂食得之詼諧趣味語調。", "［口氣韻味］")
    add_bullet(doc, "第4步（7分鐘）：2分鐘配速。測算 2 分鐘恰好讀至「白米崁牢咧」（約 380 字）。", "［配速線測試］")

    # 單元六：國語演說
    add_h2(doc, "單元六：國語演說組——在校教學操作教案（二擇一題目）")
    add_p(doc, "訓練時段：每週二早自修（脫稿背誦）、週五早自修（聽鈴反應）、週五午休（走位）。")
    add_bullet(doc, "第1步（8分鐘）：四格骨架抽背。不看稿抽背：破題（25秒）➔ 故事（50秒）➔ 啟發（30秒）➔ 結尾（15秒）。", "［骨架背誦］")
    add_bullet(doc, "第2步（10分鐘）：抓除語言贅字。只要出現「然後、那個、那、嗯」，導師立刻按鈴打斷，要求重述直到零贅字。", "［除贅手術］")
    add_bullet(doc, "第3步（10分鐘）：視線三角與手勢。視線每 15 秒左中右切換；設計猶豫收胸、合十真摯、展開呼應 3 個自然手勢。", "［眼神手勢］")
    add_bullet(doc, "第4步（7分鐘）：抗鈴聲實戰。1:30 敲鈴一響進結論，1:50 完稿鞠躬致謝下台。", "［鈴聲掌控］")

    # 單元七：臺灣台語情境演說
    add_h2(doc, "單元七：臺灣台語情境演說組——在校教學操作教案（〈食中晝〉）")
    add_p(doc, "訓練時段：每週二午休（動作與問答）、週五早修（快說）、週五午休（驗收）。")
    add_bullet(doc, "第1步（10分鐘）：生動身段大師班。演練 4 個肢體：肚子餓摸肚子、推倒菜桶大驚失色、掩嘴發愣、跪地拿布鑢仔擦地板。", "［身段演繹］")
    add_bullet(doc, "第2步（15分鐘）：評判即席問答（Q&A）現場抽考。導師扮演嚴肅評審，以台語抽問應急處理、校園喜愛菜色、故事啟發三大題，引導學生分三步禮貌回答。", "［即席問答］")
    add_bullet(doc, "第3步（10分鐘）：完整計時演練。演說 1:45 完稿，問答 30 秒俐落回答，展現大方台語風采。", "［全真驗收］")

    doc.add_page_break()

    # ==============================
    # 第二部：回家作業學習單專區
    # ==============================
    add_h1(doc, "【第二部：回家作業學習單專區】（學生每日任務與家長簽章）")
    add_p(doc, "本專區載明各項目選手週一至週四每日 15~20 分鐘精熟作業，以及週末全真模擬驗收任務。家長每日檢閱後請於表格中簽名確認：", italic=True)

    def add_homework_table(title, rows_data):
        add_h2(doc, title)
        table = doc.add_table(rows=len(rows_data), cols=4)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(table)
        widths = [Inches(1.0), Inches(3.8), Inches(1.5), Inches(0.9)]
        for r_i, r_d in enumerate(rows_data):
            row = table.rows[r_i]
            for c_i, c_t in enumerate(r_d):
                cell = row.cells[c_i]
                cell.width = widths[c_i]
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i in [0, 3] else WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                run = p.add_run(c_t)
                if r_i == 0:
                    set_cell_background(cell, "0F766E")
                    apply_font(run, size_pt=9, bold=True, color_rgb=(255, 255, 255))
                else:
                    if r_i % 2 == 1:
                        set_cell_background(cell, "F0FDFA")
                    apply_font(run, size_pt=8.5, bold=(c_i==0), color_rgb=(30, 41, 59))
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # 1. 寫字作業
    hw_calli = [
        ["天數", "每日回家作業內容（每天 15~20 分鐘）", "評量標準", "家長簽章"],
        ["週一", "在九宮格紙上精練指定字 4 字（每字書寫 5 遍，圈選最滿意 1 字）。", "重心穩健、筆鋒分明", "［ ］已完成"],
        ["週二", "在九宮格紙上精練指定字 3 字 ＋ 複習昨日 4 字（共 7 字）。", "左右相讓、橫平豎直", "［ ］已完成"],
        ["週三", "練習四字組詞連貫臨摹（如「拒絕毒品」、「反對霸凌」）。", "字徑一致、氣息連貫", "［ ］已完成"],
        ["週四", "練習落款小字：「臺中市梧棲區中正國小四年丙班 ○○○書」3 遍。", "字體清秀、大小均勻", "［ ］已完成"],
        ["週末", "【週末任務】四尺四開宣紙全篇模擬（28字＋落款）1次，45分內完成。", "［ ］特優 ［ ］優等", "家長簽章：___"]
    ]
    add_homework_table("1. 【寫字書法組】四丙每日回家作業單", hw_calli)

    # 2. 作文作業
    hw_comp = [
        ["天數", "每日回家作業內容（每天 15~20 分鐘）", "評量標準", "家長簽章"],
        ["週一", "閱讀課外好書，摘錄 2 個成語與 1 句修辭佳句，抄寫於筆記本。", "成語正確、附解釋說明", "［ ］已完成"],
        ["週二", "運用當週學習之破題法（開門見山/畫面特寫/設問），寫 80 字首段。", "破題鮮明、吸睛動人", "［ ］已完成"],
        ["週三", "進行五感摹寫微段落擴寫（描寫味道、微風或緊張表情，約100字）。", "運用動詞鏈與感官描摹", "［ ］已完成"],
        ["週四", "背誦 1 句人生哲理名言，並擴寫為 100 字總結結尾段落。", "首尾呼應、立意深刻", "［ ］已完成"],
        ["週末", "【週末任務】命題《那一刻，我長大了》，限時75分完成600~700字作文。", "稿面整潔、段落分明", "家長簽章：___"]
    ]
    add_homework_table("2. 【作文組】四丙每日回家作業單", hw_comp)

    # 3. 字音字形作業
    hw_phon = [
        ["天數", "每日回家作業內容（每天 15~20 分鐘）", "評量標準", "家長簽章"],
        ["週一", "完成每日 20 題集訓卷（Day 1），錯字紅筆在錯題本訂正 3 遍。", "字體工整、調號正確", "［ ］已完成"],
        ["週二", "完成每日 20 題集訓卷（Day 2），家長隨機口頭抽考 5 題。", "抽考正確率 100%", "［ ］已完成"],
        ["週三", "完成每日 20 題集訓卷（Day 3），整理 3 個易混淆形近字部首。", "清楚標示部首差異", "［ ］已完成"],
        ["週四", "完成每日 20 題集訓卷（Day 4），遮住答案進行 1 分鐘極速盲測。", "下筆無猶豫、零塗改", "［ ］已完成"],
        ["週末", "【週末任務】限時 2 分 30 秒完成 50 題極速測驗卷，塗改次數為 0。", "得分：___ 分（滿分25）", "家長簽章：___"]
    ]
    add_homework_table("3. 【國語字音字形組】四丙每日回家作業單", hw_phon)

    # 4. 國語朗讀作業
    hw_m_read = [
        ["天數", "每日回家作業內容（每天 15~20 分鐘）", "評量標準", "家長簽章"],
        ["週一", "對照聲情標記稿，逐字大聲朗讀〈藍蝴蝶〉全文 2 遍。", "咬字清楚、無漏字添字", "［ ］已完成"],
        ["週二", "專注練習一聲高平、四聲全降調值，朗讀前三段 3 遍。", "調號精準、氣息平穩", "［ ］已完成"],
        ["週三", "手機錄音一段 2 分鐘朗讀，回聽挑出 1 處發音含糊處重新練習。", "能自我檢視發音盲點", "［ ］已完成"],
        ["週四", "雙手捧稿呈 45 度角，全身鏡前朗讀 2 遍，注意眼神抬頭看評審。", "站姿挺拔、眼神交流", "［ ］已完成"],
        ["週末", "【週末任務】全家人面前站姿朗讀，計時2分鐘，檢測讀至第400字配速線。", "家人評分：［ ］極佳", "家長簽章：___"]
    ]
    add_homework_table("4. 【國語朗讀組】四丙每日回家作業單（〈藍蝴蝶〉專用）", hw_m_read)

    # 5. 台語朗讀作業
    hw_t_read = [
        ["天數", "每日回家作業內容（每天 15~20 分鐘）", "評量標準", "家長簽章"],
        ["週一", "看文章邊聽官方 MP3 音檔 2 遍，隨後自己逐字大聲朗讀 2 遍。", "語音貼近官方音檔", "［ ］已完成"],
        ["週二", "專練入聲字收音（-p, -t, -k, -h）與連讀變調，朗讀前兩段 3 遍。", "入聲收音短促有力", "［ ］已完成"],
        ["週三", "找出 3 個最生疏台語詞（乱鐘仔聲、隱無sik），查字典讀熟。", "掌握正確台羅讀音", "［ ］已完成"],
        ["週四", "朗讀整篇給長輩聽，請長輩針對「台語口氣（khuì-kháu）」指導。", "長輩稱讚道地流利", "［ ］已完成"],
        ["週末", "【週末任務】計時 2 分鐘錄音，檢查是否讀至第 380 字（白米崁牢咧）。", "2分鐘朗讀順暢滿分", "家長簽章：___"]
    ]
    add_homework_table("5. 【臺灣台語朗讀組】四丙每日回家作業單（〈阿公變魔術〉專用）", hw_t_read)

    # 6. 國語演說作業
    hw_m_sp = [
        ["天數", "每日回家作業內容（每天 15~20 分鐘）", "評量標準", "家長簽章"],
        ["週一", "手抄整篇 420 字講稿 1 遍，標註四段核心關鍵詞與秒數。", "深刻理解講稿骨架", "［ ］已完成"],
        ["週二", "脫稿背誦第 1、2 段 5 遍，要求聲音宏亮、字字清晰。", "完全脫稿、無斷續", "［ ］已完成"],
        ["週三", "脫稿背誦第 3、4 段 5 遍，加入設計好的 3 個自然大方手勢。", "手勢自然、不機械化", "［ ］已完成"],
        ["週四", "全身鏡前脫稿演說 3 遍，請家人抓出贅字（然後、那）。", "贅字出現次數為 0", "［ ］已完成"],
        ["週末", "【週末任務】家人錄影1次，回放檢討眼神兼顧左中右，時間控制1:45~1:55。", "演說時間：__分__秒", "家長簽章：___"]
    ]
    add_homework_table("6. 【國語演說組】四丙每日回家作業單", hw_m_sp)

    # 7. 台語情境演說作業
    hw_t_sp = [
        ["天數", "每日回家作業內容（每天 15~20 分鐘）", "評量標準", "家長簽章"],
        ["週一", "手抄台語講稿 1 遍，標出 4 個演繹動作（摸肚子、推倒、掩嘴、擦地板）。", "熟記故事情節節奏", "［ ］已完成"],
        ["週二", "鏡前演練前兩段 5 遍，把肚子餓期待與推搡頑皮模樣演出來。", "表情逗趣生動活潑", "［ ］已完成"],
        ["週三", "鏡前演練後兩段 5 遍，把跪地擦地板與認錯負責誠懇神情演出來。", "身段自然、台語清晰", "［ ］已完成"],
        ["週四", "家人以台語隨機抽問 1 題即席題目（菜桶偃倒怎麼辦），台語完整回答。", "能分三步流暢對答", "［ ］已完成"],
        ["週末", "【週末任務】錄製「2 分鐘演講 ＋ 1 題即席問答」影音檔案傳導師。", "演繹生動度：［ ］極佳", "家長簽章：___"]
    ]
    add_homework_table("7. 【臺灣台語情境演說組】四丙每日回家作業單（〈食中晝〉專用）", hw_t_sp)

    doc.add_page_break()

    # 參、四丙家庭聯絡回饋聯
    add_h1(doc, "參、四年丙班家長每週培訓回饋與導師聯絡聯（可印裁繳回）")
    add_p(doc, "每週五完成週末驗收後，請家長填寫回饋與簽名，於下週一由選手繳交導師批閱：", italic=True)

    sign_data = [
        ["臺中市梧棲區中正國小 115 學年度校內語文競賽【四年丙班】家庭聯絡回饋聯", "", "", ""],
        ["選手姓名", "____________", "參賽項目", "__________________"],
        ["訓練週次", "第 _____ 週", "日期區間", "____月____日 ～ ____月____日"],
        ["星期一作業", "［ ］已完成指定作業（耗時：___分鐘）", "家長簽章", "________________"],
        ["星期二作業", "［ ］已完成指定作業（耗時：___分鐘）", "家長簽章", "________________"],
        ["星期三作業", "［ ］已完成指定作業（耗時：___分鐘）", "家長簽章", "________________"],
        ["星期四作業", "［ ］已完成指定作業（耗時：___分鐘）", "家長簽章", "________________"],
        ["週末全真驗收", "［ ］已完成全真模擬／錄音驗收任務", "家長簽章", "________________"],
        ["家長溫馨觀察與鼓勵小語", "\n__________________________________________________________________\n", "", ""],
        ["四丙導師批閱與訓練叮嚀", "\n__________________________________________________________________\n", "", ""]
    ]
    t_sig = doc.add_table(rows=len(sign_data), cols=4)
    t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_sig)
    w_sig = [Inches(1.8), Inches(2.2), Inches(1.2), Inches(2.0)]

    for r_i, r_d in enumerate(sign_data):
        row = t_sig.rows[r_i]
        for c_i, c_t in enumerate(r_d):
            cell = row.cells[c_i]
            cell.width = w_sig[c_i]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(c_t)
            if r_i == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                set_cell_background(cell, "1E3A8A")
                apply_font(run, size_pt=10, bold=True, color_rgb=(255, 255, 255))
            elif r_i in [8, 9] and c_i == 0:
                set_cell_background(cell, "F1F5F9")
                apply_font(run, size_pt=9, bold=True, color_rgb=(30, 41, 59))
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i in [0, 2] else WD_ALIGN_PARAGRAPH.LEFT
                if c_i in [0, 2]:
                    set_cell_background(cell, "F8FAFC")
                apply_font(run, size_pt=8.5, bold=(c_i in [0, 2]), color_rgb=(30, 41, 59))

    doc.save(out_path)
    print("Class 4C guide successfully generated at:", out_path)

if __name__ == "__main__":
    out = os.path.abspath("四年丙班_校內語文競賽培訓指引與在校每日練習暨回家作業手冊.docx")
    build_class_4c_docx(out)
