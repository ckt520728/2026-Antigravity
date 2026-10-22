#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MediCloud Records Processor (健保醫療資訊雲端查詢資料處理器)
Author: Dr. Chu's AI Assistant
Description: Classifies and processes NHI MediCloud data into two distinct formats:
  - Format A: Diagnostic & Laboratory Reports (檢驗數據、放射影像、病理報告、用藥紀錄)
  - Format B: Hospital Discharge Summaries (跨院出院病歷摘要、手術介入、病程時間軸、出院帶藥)
Generates publication-quality Word documents (.docx) in Traditional Chinese and/or English.
"""

import os
import sys
import argparse
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

sys.stdout.reconfigure(encoding='utf-8')

BASE_DOCS_DIR = r"C:\Users\YangminRoom1\Documents\Dr Chu's file\Word Documents"
TEMPLATE_DIR = os.path.join(BASE_DOCS_DIR, "_Templates")
TEMPLATE_A = os.path.join(TEMPLATE_DIR, "MediCloud-檢驗檢查與診斷報告範本.docx")
TEMPLATE_B = os.path.join(TEMPLATE_DIR, "MediCloud-跨院出院病歷摘要範本.docx")
FALLBACK_TEMPLATE = os.path.join(TEMPLATE_DIR, "MediCloud-健保雲端摘要範本.docx")

def format_run(run, font_name="微軟正黑體", size_pt=10, bold=False, italic=False, color_rgb=(0,0,0)):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor(*color_rgb)
    rPr = run._element.get_or_add_rPr()
    rFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:ascii="{font_name}" w:hAnsi="{font_name}" w:eastAsia="{font_name}"/>')
    rPr.append(rFonts)

def set_cell_shading(cell, color_hex):
    shd_xml = f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shd_xml))

def set_grid_borders(table, color="B0C4DE", sz="4"):
    tblPr = table._tbl.tblPr
    borders_xml = f'''
    <w:tblBorders {nsdecls("w")}>
        <w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
        <w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
        <w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
        <w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
        <w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
        <w:insideV w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
    </w:tblBorders>
    '''
    tblPr.append(parse_xml(borders_xml))

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
    <w:tcMar {nsdecls("w")}>
        <w:top w:w="{top}" w:type="dxa"/>
        <w:bottom w:w="{bottom}" w:type="dxa"/>
        <w:left w:w="{left}" w:type="dxa"/>
        <w:right w:w="{right}" w:type="dxa"/>
    </w:tcMar>
    ''')
    tcPr.append(tcMar)

def add_heading_1(doc, text, lang="zh"):
    font_name = "Calibri" if lang == "en" else "微軟正黑體"
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    format_run(run, font_name=font_name, size_pt=13.5, bold=True, color_rgb=(27, 54, 93))
    return p

def add_heading_2(doc, text, lang="zh"):
    font_name = "Calibri" if lang == "en" else "微軟正黑體"
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    format_run(run, font_name=font_name, size_pt=11.5, bold=True, color_rgb=(43, 84, 126))
    return p

def add_bullet_point(doc, title, text, indent_level=0, lang="zh"):
    font_name = "Calibri" if lang == "en" else "微軟正黑體"
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    if indent_level == 1:
        p.paragraph_format.left_indent = Inches(0.25)
    elif indent_level == 2:
        p.paragraph_format.left_indent = Inches(0.45)
    bullet_symbol = "■ " if indent_level == 0 else ("• " if indent_level == 1 else "– ")
    r_bullet = p.add_run(bullet_symbol)
    format_run(r_bullet, font_name=font_name, size_pt=10, bold=True, color_rgb=(27, 54, 93))
    if title:
        sep = ": " if lang == "en" else "："
        r_title = p.add_run(title + (sep if not title.endswith(":") and not title.endswith("：") else " "))
        format_run(r_title, font_name=font_name, size_pt=10, bold=True, color_rgb=(43, 84, 126))
    r_text = p.add_run(text)
    format_run(r_text, font_name=font_name, size_pt=10, bold=False, color_rgb=(30, 30, 30))
    return p

def add_callout_box(doc, title, items, border_color="1B365D", bg_color="F4F7FA", lang="zh"):
    font_name = "Calibri" if lang == "en" else "微軟正黑體"
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    cell = table.rows[0].cells[0]
    cell.width = Inches(7.0)
    set_cell_shading(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=180, right=160)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders_xml = f'''
    <w:tcBorders {nsdecls("w")}>
        <w:top w:val="none"/>
        <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>
        <w:bottom w:val="none"/>
        <w:right w:val="none"/>
    </w:tcBorders>
    '''
    tcPr.append(parse_xml(borders_xml))
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    run_t = p.add_run(title)
    format_run(run_t, font_name=font_name, size_pt=11, bold=True, color_rgb=(27, 54, 93))
    
    for item in items:
        p_item = cell.add_paragraph()
        p_item.paragraph_format.space_before = Pt(1)
        p_item.paragraph_format.space_after = Pt(2)
        p_item.paragraph_format.line_spacing = 1.15
        
        sep = ": " if ": " in item else ("：" if "：" in item else None)
        if sep:
            pref, rest = item.split(sep, 1)
            r1 = p_item.add_run("• " + pref + (": " if lang=="en" else "："))
            format_run(r1, font_name=font_name, size_pt=9.5, bold=True, color_rgb=(43, 84, 126))
            r2 = p_item.add_run(rest)
            format_run(r2, font_name=font_name, size_pt=9.5, bold=False, color_rgb=(30, 30, 30))
        else:
            r = p_item.add_run("• " + item)
            format_run(r, font_name=font_name, size_pt=9.5, bold=False, color_rgb=(30, 30, 30))
            
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(4)

def clean_body_preserving_sectpr(doc, tbl0):
    body = doc._body._body
    tbl_elem = tbl0._tbl
    found_tbl = False
    elements_to_remove = []
    for elem in list(body):
        if elem == tbl_elem:
            found_tbl = True
            continue
        if found_tbl:
            if elem.tag.endswith('sectPr'):
                continue
            elements_to_remove.append(elem)
    for elem in elements_to_remove:
        body.remove(elem)

def detect_file_category(content):
    """
    Classifies raw input into 'lab' (Format A) or 'discharge' (Format B).
    """
    discharge_keywords = [
        "出院病歷摘要", "住院日期", "出院日期", "住院臆斷", "出院診斷",
        "Discharge Summary", "Admission date", "Hospital course",
        "住院治療經過", "出院帶藥", "出院狀況", "轉入醫院", "病房床號"
    ]
    lab_keywords = [
        "成人預防保健", "成人健檢", "健康檢查", "檢驗項目", "檢查項目",
        "總膽固醇", "三酸甘油酯", "肌酸酐", "腎絲球過濾率", "尿液蛋白質",
        "飯前血糖", "SGOT", "SGPT", "門診", "慢箋", "放射影像", "病理報告"
    ]
    
    score_discharge = sum(1 for kw in discharge_keywords if kw in content)
    score_lab = sum(1 for kw in lab_keywords if kw in content)
    
    if score_discharge >= 2 or "出院病歷摘要" in content:
        return "discharge"
    return "lab"

def extract_text_from_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".docx":
        doc = docx.Document(file_path)
        full_text = []
        for p in doc.paragraphs:
            if p.text.strip():
                full_text.append(p.text)
        for t in doc.tables:
            for r in t.rows:
                full_text.append(" | ".join([c.text.strip().replace('\n', ' ') for c in r.cells]))
        return "\n".join(full_text)
    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

def main():
    parser = argparse.ArgumentParser(description="Process and categorize NHI MediCloud data into Format A or Format B Word files.")
    parser.add_argument("--input", "-i", required=True, help="Path to input raw file (.md, .txt, .docx)")
    parser.add_argument("--category", "-c", choices=["auto", "lab", "discharge"], default="auto", help="Category: lab (Format A) or discharge (Format B)")
    parser.add_argument("--lang", "-l", choices=["zh", "en", "both"], default="both", help="Output language (zh, en, or both)")
    parser.add_argument("--output", "-o", help="Custom output docx path")
    args = parser.parse_args()

    content = extract_text_from_file(args.input)
    category = args.category
    if category == "auto":
        category = detect_file_category(content)
        print(f"Auto-detected Category: {category.upper()} ({'Format A: Diagnostic/Lab' if category=='lab' else 'Format B: Discharge Summary'})")

    print(f"File: {args.input}")
    print(f"Category: {category}")
    print(f"Target Language: {args.lang}")
    print("Use the corresponding builder functions in python or follow SKILL.md guidelines to produce pristine outputs.")

if __name__ == "__main__":
    main()
