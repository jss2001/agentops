# -*- coding: utf-8 -*-
# One Console AI · ITCEN 신사업 공모전 제안서 v4
# 미스터피피티 템플릿 문법 이식:
#  - 표준 헤더(오버라인 + 섹션번호 + 타이틀 + LOGO) + 이중 헤더 룰(포인트선+헤어라인)
#  - 리드 메시지 18pt(강조 run) · 키워드 16pt · 본문 12pt · 빅넘버 40pt
#  - 팔레트: #0C0C0C(잉크) · #0049F0(단일 액센트) · BFBFBF/A6A6A6/D9D9D9(그레이)
# 실행: py proposal\make_proposal.py → proposal\One_Console_AI_제안서_v4.pptx
import math
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn
from pathlib import Path

# ---------- 템플릿 팔레트 ----------
BLUE   = RGBColor(0x00, 0x49, 0xF0)
BLUE_D = RGBColor(0x4D, 0x82, 0xFF)   # 다크 표면용 밝은 블루
INK    = RGBColor(0x0C, 0x0C, 0x0C)
MUT80  = RGBColor(0x2D, 0x2D, 0x2D)
MUT48  = RGBColor(0x7A, 0x7A, 0x7A)
GRAY   = RGBColor(0xA6, 0xA6, 0xA6)
SILVER = RGBColor(0xBF, 0xBF, 0xBF)
BODY_D = RGBColor(0xCC, 0xCC, 0xCC)
HAIR   = RGBColor(0xD9, 0xD9, 0xD9)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
PARCH  = RGBColor(0xF5, 0xF5, 0xF7)
PEARL  = RGBColor(0xFB, 0xFB, 0xFB)
TILE   = RGBColor(0x28, 0x29, 0x2B)
BLACK  = RGBColor(0x0C, 0x0C, 0x0C)
FONT   = "Pretendard"

SW, SH = Inches(13.333), Inches(7.5)
ML = Inches(0.62)                       # 템플릿 좌측 마진
CW = SW - ML * 2

prs = Presentation()
prs.slide_width, prs.slide_height = SW, SH
BLANK = prs.slide_layouts[6]

# ---------- primitives ----------
def _set_font(run, size, bold, color, name=FONT, spc=None):
    f = run.font
    f.size, f.bold, f.name = Pt(size), bold, name
    f.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    ea = rPr.find(qn('a:ea'))
    if ea is None:
        ea = rPr.makeelement(qn('a:ea'), {}); rPr.append(ea)
    ea.set('typeface', name)
    if spc is not None:
        rPr.set('spc', str(int(spc * 100)))

def text(slide, x, y, w, h, paras, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
         wrap=True, spacing=1.18):
    tb = slide.shapes.add_textbox(int(x), int(y), int(w), int(h))
    tf = tb.text_frame
    tf.word_wrap = wrap; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.line_spacing = spacing
        if len(para) == 5: p.space_after = Pt(para[4])
        if isinstance(para[0], list):
            for r_ in para[0]:
                run = p.add_run(); run.text = r_[0]
                _set_font(run, r_[1], r_[2], r_[3], spc=(r_[4] if len(r_) > 4 else None))
        else:
            run = p.add_run(); run.text = para[0]
            _set_font(run, para[1], para[2], para[3])
    return tb

def box(slide, x, y, w, h, fill, line=None, r_px=14, lw=1.0,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE):
    sp = slide.shapes.add_shape(shape, int(x), int(y), int(w), int(h))
    sp.shadow.inherit = False
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        try: sp.adjustments[0] = min(0.5, (r_px / 96) / min(w / 914400, h / 914400))
        except Exception: pass
    if fill is None: sp.fill.background()
    else: sp.fill.solid(); sp.fill.fore_color.rgb = fill
    if line is None: sp.line.fill.background()
    else: sp.line.color.rgb = line; sp.line.width = Pt(lw)
    return sp

def pill(slide, x, y, w, h, label, fill, color, size=10.5, bold=True, line=None):
    box(slide, x, y, w, h, fill, line=line, r_px=999)
    text(slide, x, y + Inches(0.01), w, h - Inches(0.02), [(label, size, bold, color)],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

def conn(slide, x1, y1, x2, y2, color=HAIR, w=1.0):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, int(x1), int(y1), int(x2), int(y2))
    c.shadow.inherit = False
    c.line.color.rgb = color; c.line.width = Pt(w)
    return c

def dot(slide, cx, cy, d, fill, line=None):
    return box(slide, cx - d / 2, cy - d / 2, d, d, fill, line, shape=MSO_SHAPE.OVAL)

def linechart(slide, x, y, w, h, pts, color=BLUE, lw=2.0, dots=True):
    n = len(pts)
    xs = [x + w * i / (n - 1) for i in range(n)]
    ys = [y + h * (1 - p) for p in pts]
    for i in range(n - 1):
        conn(slide, xs[i], ys[i], xs[i + 1], ys[i + 1], color, lw)
    if dots:
        for xi, yi in zip(xs, ys):
            dot(slide, xi, yi, Inches(0.08), color)
    return xs, ys

SHOTS = Path(__file__).resolve().parent / "shots"
def _imgsize(path):
    """PNG 픽셀 크기 읽기 (외부 의존성 없이)."""
    import struct
    with open(path, "rb") as f:
        head = f.read(26)
    if head[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", head[16:24])
        return w, h
    return 1600, 1000

def browser_frame(slide, x, y, w, name, title="", cap=""):
    """브라우저 창 크롬 + 스크린샷. 세로 높이는 이미지 비율로 자동 결정.
       반환: 프레임 전체 높이(EMU)."""
    path = SHOTS / name
    iw, ih = _imgsize(path)
    bar = Inches(0.34)
    imgw = w
    imgh = int(imgw * ih / iw)
    # 크롬 바
    box(slide, x, y, w, bar, RGBColor(0x33, 0x34, 0x38), r_px=8)
    box(slide, x, y + bar / 2, w, bar / 2, RGBColor(0x33, 0x34, 0x38),
        shape=MSO_SHAPE.RECTANGLE)  # 하단 모서리 각지게
    for i, c in enumerate([RGBColor(0xFF, 0x5F, 0x57), RGBColor(0xFE, 0xBC, 0x2E),
                           RGBColor(0x28, 0xC8, 0x40)]):
        dot(slide, x + Inches(0.2) + Inches(0.18) * i, y + bar / 2, Inches(0.09), c)
    if title:
        box(slide, x + Inches(0.95), y + Inches(0.075), w - Inches(1.6), Inches(0.19),
            RGBColor(0x24, 0x25, 0x28), r_px=99)
        text(slide, x + Inches(0.95), y + Inches(0.08), w - Inches(1.6), Inches(0.19),
             [(title, 7.5, False, RGBColor(0x9A, 0x9C, 0xA6))], align=PP_ALIGN.CENTER,
             anchor=MSO_ANCHOR.MIDDLE)
    # 이미지
    slide.shapes.add_picture(str(path), int(x), int(y + bar), int(imgw), int(imgh))
    # 테두리(헤어라인)
    box(slide, x, y + bar, w, imgh, None, HAIR, r_px=0, lw=1.0, shape=MSO_SHAPE.RECTANGLE)
    total = bar + imgh
    if cap:
        text(slide, x, y + total + Inches(0.06), w, Inches(0.26),
             [(cap, 9, False, MUT48)], align=PP_ALIGN.CENTER)
    return total

def thumb(slide, x, y, w, name, label):
    """작은 스크린샷 썸네일 + 라벨 (제품 둘러보기 그리드용)."""
    path = SHOTS / name
    iw, ih = _imgsize(path)
    imgh = int(w * ih / iw)
    slide.shapes.add_picture(str(path), int(x), int(y), int(w), int(imgh))
    box(slide, x, y, w, imgh, None, HAIR, r_px=6, lw=1.0)
    text(slide, x, y + imgh + Inches(0.05), w, Inches(0.24),
         [(label, 9.5, True, INK)], align=PP_ALIGN.CENTER)
    return imgh

def shot_fit(slide, x, y, w, h, name, title="", cap="", bias="top"):
    """브라우저 크롬 + 스크린샷을 정확히 w×h 박스에 왜곡 없이 크롭해 배치.
       크롬은 [y, y+0.32], 이미지는 그 아래 h 높이. 반환: 전체 높이(EMU)."""
    path = SHOTS / name
    iw, ih = _imgsize(path)
    chrome = Inches(0.32)
    box(slide, x, y, w, chrome, RGBColor(0x33, 0x34, 0x38), r_px=7)
    box(slide, x, y + chrome / 2, w, chrome / 2, RGBColor(0x33, 0x34, 0x38),
        shape=MSO_SHAPE.RECTANGLE)
    for i, c in enumerate([RGBColor(0xFF, 0x5F, 0x57), RGBColor(0xFE, 0xBC, 0x2E),
                           RGBColor(0x28, 0xC8, 0x40)]):
        dot(slide, x + Inches(0.18) + Inches(0.17) * i, y + chrome / 2, Inches(0.085), c)
    if title:
        aw = w - Inches(1.5)
        box(slide, x + Inches(0.9), y + Inches(0.07), aw, Inches(0.18),
            RGBColor(0x22, 0x23, 0x26), r_px=99)
        text(slide, x + Inches(0.9), y + Inches(0.07), aw, Inches(0.18),
             [(title, 7.5, False, RGBColor(0x9A, 0x9C, 0xA6))],
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    pic = slide.shapes.add_picture(str(path), int(x), int(y + chrome), int(w), int(h))
    box_ar = (w / 914400) / (h / 914400)
    img_ar = iw / ih
    if box_ar >= img_ar:                       # 박스가 더 넓음 → 상하 크롭
        crop = (ih - iw / box_ar) / ih
        if bias == "top":
            pic.crop_bottom = crop
        else:
            pic.crop_top = pic.crop_bottom = crop / 2
    else:                                       # 박스가 더 좁음 → 좌우 크롭
        crop = (iw - ih * box_ar) / iw
        pic.crop_left = pic.crop_right = crop / 2
    box(slide, x, y + chrome, w, h, None, HAIR, r_px=0, lw=1.0, shape=MSO_SHAPE.RECTANGLE)
    if cap:
        text(slide, x, y + chrome + h + Inches(0.06), w, Inches(0.26),
             [(cap, 9, False, MUT48)], align=PP_ALIGN.CENTER)
    return chrome + h

PAGE = [0]
def base(mode="white"):
    s = prs.slides.add_slide(BLANK)
    bg = {"white": WHITE, "parchment": PARCH, "dark": TILE, "black": BLACK}[mode]
    box(s, 0, 0, SW, SH, bg, shape=MSO_SHAPE.RECTANGLE)
    return s

def content(num, title, lead=None, mode="white"):
    """미스터피피티 표준 헤더: 오버라인 + 번호/타이틀 + LOGO + 이중 룰 + 리드 메시지"""
    s = base(mode)
    dark = mode in ("dark", "black")
    ink = WHITE if dark else INK
    sub = GRAY if dark else MUT48
    # 오버라인 (제안서 이름)
    text(s, ML, Inches(0.52), Inches(6.0), Inches(0.26),
         [("One Console AI — AI Agent 통합 형상관리 플랫폼", 11, False, sub)])
    # 섹션 번호 + 타이틀 (템플릿: 24pt ExtraBold)
    text(s, ML, Inches(0.84), Inches(0.6), Inches(0.42), [(num, 24, True, BLUE if not dark else BLUE_D)])
    text(s, ML + Inches(0.66), Inches(0.84), Inches(9.5), Inches(0.42), [(title, 24, True, ink)])
    # LOGO 자리
    text(s, SW - Inches(1.6), Inches(0.9), Inches(1.0), Inches(0.3),
         [("ITCEN", 12, True, sub)], align=PP_ALIGN.RIGHT)
    # 이중 헤더 룰: 포인트(액센트) + 헤어라인
    conn(s, ML, Inches(1.37), ML + Inches(0.44), Inches(1.37), BLUE, 2.4)
    conn(s, ML + Inches(0.45), Inches(1.37), SW - ML, Inches(1.37),
         TILE if dark else HAIR, 1.0)
    # 리드 메시지 (템플릿 18pt · 강조 run)
    if lead:
        paras = [(lead, 17, True, ink)] if isinstance(lead, str) else [(rl,) for rl in lead]
        text(s, ML, Inches(1.58), CW, Inches(0.55), paras, spacing=1.22)
    PAGE[0] += 1
    text(s, SW - Inches(1.1), Inches(7.1), Inches(0.5), Inches(0.28),
         [(f"{PAGE[0]:02d}", 9.5, True, GRAY)], align=PP_ALIGN.RIGHT)
    return s

def lead_runs(parts):
    """parts: [(txt, blue?), ...] → 18pt 리드 런 목록"""
    return [[(t, 17, True, BLUE if b else INK) for (t, b) in parts]]

def kw_block(s, x, y, w, kw, body, kw_color=INK):
    """템플릿 반복 단위: 키워드(16B) / 라인 / 본문(12)"""
    text(s, x, y, w, Inches(0.32), [(kw, 15, True, kw_color)])
    conn(s, x, y + Inches(0.42), x + w - Inches(0.25), y + Inches(0.42), HAIR, 1.0)
    text(s, x, y + Inches(0.55), w - Inches(0.15), Inches(0.9), [(body, 11, False, MUT80)],
         spacing=1.3)

# ============================================================
# 01 · 표지
# ============================================================
s = base("black")
rc, rr = (Inches(10.5), Inches(3.75)), Inches(1.8)
box(s, rc[0] - rr, rc[1] - rr, rr * 2, rr * 2, None, RGBColor(0x3A, 0x3A, 0x3E), lw=1.2, shape=MSO_SHAPE.OVAL)
for (dx, dy, c_) in [(0, -rr, BLUE_D), (rr, 0, WHITE), (0, rr, RGBColor(0x3A, 0x3A, 0x3E)), (-rr, 0, RGBColor(0x3A, 0x3A, 0x3E))]:
    dot(s, rc[0] + dx, rc[1] + dy, Inches(0.15), c_)
text(s, rc[0] - Inches(1.2), rc[1] - Inches(0.3), Inches(2.4), Inches(0.7), [
    ("지식 → Agent →", 10.5, False, GRAY, 2), ("운영 → 개선 ↺", 10.5, False, GRAY)],
    align=PP_ALIGN.CENTER)
text(s, ML, Inches(0.55), Inches(6), Inches(0.3),
     [("ITCEN 신사업 아이디어 공모전", 12, True, GRAY)])
text(s, SW - Inches(1.72), Inches(0.55), Inches(1.1), Inches(0.3),
     [("ITCEN", 12, True, GRAY)], align=PP_ALIGN.RIGHT)
conn(s, ML, Inches(1.0), ML + Inches(0.44), Inches(1.0), BLUE, 2.4)
conn(s, ML + Inches(0.45), Inches(1.0), SW - ML, Inches(1.0), RGBColor(0x3A, 0x3A, 0x3E), 1.0)
text(s, ML, Inches(2.15), Inches(9.0), Inches(1.9), [
    ([("One Console AI", 56, True, WHITE, -1.2)], 8),
    ([("AI Agent ", 22, False, BODY_D), ("통합 형상관리 플랫폼", 22, True, WHITE)],)],
    spacing=1.1)
box(s, ML, Inches(4.42), Inches(0.56), Inches(0.05), BLUE, r_px=99)
text(s, ML, Inches(4.72), Inches(8.5), Inches(1.0), [
    ("기업 AI를, 프로젝트가 아닌 플랫폼으로.", 17, True, WHITE, 6),
    ("현장에서 반복된 문제로 시작해, 검증된 해결책을 거쳐, 사업이 됩니다.", 12, False, GRAY)])
# 하단 밴드 (템플릿 표지의 스트립)
box(s, 0, Inches(6.35), SW, Inches(0.62), TILE, shape=MSO_SHAPE.RECTANGLE)
text(s, ML, Inches(6.5), Inches(12), Inches(0.32),
     [("2026. 07   |   아이디어 제안서   |   제안팀 ____________", 11, False, BODY_D)])

# ============================================================
# 02 · 제안 요약 (00)
# ============================================================
s = content("00", "제안 요약",
            lead=lead_runs([("네 가지 심사 기준", True), ("에, 네 줄로 답합니다.", False)]))
segs = [(35, "문제 발굴", BLUE), (30, "솔루션", INK), (20, "사업화", MUT48), (15, "실행력", SILVER)]
bx = ML
for (v, l) , c_ in [((v, l), c) for (v, l, c) in segs]:
    w_ = CW * v / 100
    box(s, bx, Inches(2.3), w_ - Inches(0.05), Inches(0.46), c_, r_px=6)
    text(s, bx, Inches(2.36), w_ - Inches(0.05), Inches(0.36),
         [([(f"{v}", 12.5, True, WHITE), (f"  {l}", 9.5, False, WHITE)],)], align=PP_ALIGN.CENTER)
    bx += w_
text(s, SW - Inches(2.0), Inches(2.0), Inches(1.38), Inches(0.26),
     [("100점 만점", 9, False, GRAY)], align=PP_ALIGN.RIGHT)
cards = [
    ("35", "문제 발굴 · Industry Insight", "프로젝트마다 처음부터 다시 만드는 기업 AI",
     "대기업 현장에서 반복 확인한 구조적 비효율 — 지식·형상·로그가 전부 흩어져 있다"),
    ("30", "솔루션 유효성 · 차별성", "하나의 콘솔로 지식 · 형상 · 운영을 통합",
     "아이디어가 아니라 이미 동작하는 MVP — 콘솔 + REST API + 개선 루프"),
    ("20", "사업화 가능성", "구축 → 구독 → 운영으로 쌓이는 반복 매출",
     "아이티센 그룹 고객망이 곧 판로 — SI 본업과 같은 딜리버리 구조"),
    ("15", "실행력", "선정 다음 날부터 파일럿 준비 가능",
     "발표장에서 슬라이드가 아닌 실제 제품으로 라이브 데모"),
]
gw, gh = Inches(5.9), Inches(1.92)
for i, (score, crit, head, body) in enumerate(cards):
    x = ML + (gw + Inches(0.29)) * (i % 2)
    y = Inches(3.0) + (gh + Inches(0.24)) * (i // 2)
    box(s, x, y, gw, gh, PEARL, HAIR)
    text(s, x + Inches(0.32), y + Inches(0.26), Inches(1.15), Inches(1.4), [
        ([(score, 34, True, BLUE, -0.8)], 0), ("점", 10, False, MUT48)])
    text(s, x + Inches(1.45), y + Inches(0.28), gw - Inches(1.8), gh - Inches(0.5), [
        (crit, 9.5, True, MUT48, 4), (head, 13.5, True, INK, 5), (body, 10, False, MUT80)],
        spacing=1.2)

# ============================================================
# 03 · 현장의 발견 (01)
# ============================================================
s = content("01", "현장의 발견",
            lead=lead_runs([("“N번째 프로젝트에서, 같은 것을 또 만들고 있었다.”", True),
                            ("  — 글로벌 제조 대기업 프로젝트의 반복된 장면", False)]))
box(s, ML, Inches(2.3), Inches(6.55), Inches(4.15), WHITE, HAIR)
text(s, ML + Inches(0.38), Inches(2.52), Inches(5.8), Inches(0.3),
     [("프로젝트를 거듭해도 — 비용은 다시 들고, 자산은 남지 않는다", 12.5, True, INK)])
gx, gy, gw_, gh_ = ML + Inches(0.5), Inches(2.98), Inches(5.7), Inches(2.85)
conn(s, gx, gy + gh_, gx + gw_, gy + gh_, HAIR, 1.0)
conn(s, gx, gy, gx, gy + gh_, HAIR, 1.0)
linechart(s, gx + Inches(0.2), gy + Inches(0.2), gw_ - Inches(0.5), gh_ - Inches(0.45),
          [0.18, 0.38, 0.58, 0.78, 0.98], color=SILVER)
linechart(s, gx + Inches(0.2), gy + Inches(0.2), gw_ - Inches(0.5), gh_ - Inches(0.45),
          [0.06, 0.07, 0.06, 0.07, 0.06], color=BLUE)
text(s, gx + gw_ - Inches(1.8), gy + Inches(0.05), Inches(1.9), Inches(0.3),
     [("누적 투입 비용", 9.5, True, MUT48)])
text(s, gx + gw_ - Inches(1.8), gy + gh_ - Inches(0.6), Inches(1.9), Inches(0.3),
     [("남는 조직 자산 ≈ 0", 9.5, True, BLUE)])
for i, l in enumerate(["프로젝트 1", "2", "3", "4", "… N"]):
    text(s, gx + Inches(0.05) + (gw_ - Inches(0.5)) * i / 4 - Inches(0.35), gy + gh_ + Inches(0.08),
         Inches(0.9), Inches(0.25), [(l, 8.5, False, GRAY)], align=PP_ALIGN.CENTER)
items = [
    ("전처리 파이프라인", "프로젝트마다 재개발 — 노하우가 코드와 함께 소멸"),
    ("프롬프트 · 검색 설정", "위키·메모·머릿속에 산재 — 담당자가 단일 장애점"),
    ("운영 로그 · 피드백", "수집되지 않거나, 개선으로 연결되지 않음"),
]
for i, (h_, b_) in enumerate(items):
    y = Inches(2.3) + Inches(1.44) * i
    box(s, ML + Inches(6.85), y, Inches(5.24), Inches(1.3), WHITE, HAIR)
    text(s, ML + Inches(7.2), y + Inches(0.2), Inches(4.55), Inches(0.95), [
        ([("✕  ", 13, True, GRAY), (h_, 13, True, INK)], 4), (b_, 10.5, False, MUT80)],
        spacing=1.2)
text(s, ML + Inches(6.85), Inches(6.68) - Inches(0.55), Inches(5.24), Inches(0.5),
     [("기술이 아니라, 만든 것이 자산으로 남지 않는 ‘구조’가 문제였다.", 11, True, BLUE)],
     spacing=1.2)

# ============================================================
# 04 · 문제의 구조 (01)
# ============================================================
s = content("01", "문제의 구조",
            lead=lead_runs([("다섯 가지", True), ("가, 다섯 곳에서, 따로 관리된다.", False)]))
scatter = ["도메인 데이터", "사내 지식 (RAG)", "System Prompt", "검색 설정", "운영 로그"]
sw5 = Inches(2.28)
cxs = []
for i, t_ in enumerate(scatter):
    x = ML + (sw5 + Inches(0.17)) * i
    box(s, x, Inches(2.35), sw5, Inches(0.6), PEARL, HAIR)
    text(s, x, Inches(2.37), sw5, Inches(0.56), [(t_, 11, True, MUT80)],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    cxs.append(x + sw5 / 2)
mid = (Inches(6.67), Inches(3.55))
for cx in cxs:
    conn(s, cx, Inches(2.95), mid[0], mid[1], HAIR, 1.0)
dot(s, mid[0], mid[1], Inches(0.13), GRAY)
text(s, mid[0] + Inches(0.18), mid[1] - Inches(0.13), Inches(3.2), Inches(0.28),
     [("통합점 없음 — 각자 관리", 9.5, True, MUT48)])
stats = [("8주+", "신규 Agent 구축 리드타임", "전처리·프롬프트·검색을 매번 처음부터"),
         ("30~40%", "유사 기능 Agent 중복 개발", "부서별로 같은 봇을 각자 구축"),
         ("0", "운영 → 개선 사이클", "로그·피드백이 개선으로 연결되지 않음")]
for i, (v, l, sub) in enumerate(stats):
    x = ML + Inches(4.1) * i
    if i > 0: conn(s, x - Inches(0.12), Inches(4.15), x - Inches(0.12), Inches(5.3), HAIR, 1.0)
    text(s, x + Inches(0.12), Inches(4.05), Inches(3.7), Inches(1.45), [
        ([(v, 40, True, INK, -0.9)], 4), (l, 12.5, True, INK, 3), (sub, 10, False, MUT48)])
box(s, ML, Inches(5.65), CW, Inches(1.02), TILE)
text(s, ML + Inches(0.45), Inches(5.82), CW - Inches(0.9), Inches(0.75), [
    ("AI가 ‘운영되는 서비스’가 아니라 ‘끝나는 프로젝트’가 된다", 15.5, True, WHITE, 4),
    ("만들 때마다 비용은 다시 들고, 품질은 담당자에 좌우되며, 시간이 지나도 나아지지 않는다.", 10.5, False, BODY_D)])
text(s, ML, Inches(6.82), Inches(8), Inches(0.26),
     [("※ 수치는 당사 프로젝트 수행 경험 기반 추정치", 8.5, False, GRAY)])

# ============================================================
# 05 · Industry Insight (01)
# ============================================================
s = content("01", "Industry Insight",
            lead=lead_runs([("병목은 ‘개발’에서 ", False), ("‘운영’", True), ("으로 이동했다.", False)]))
box(s, ML, Inches(2.3), Inches(6.0), Inches(3.55), PEARL, HAIR)
text(s, ML + Inches(0.4), Inches(2.5), Inches(5.2), Inches(0.3),
     [("기업 AI 수요의 무게중심 이동", 12.5, True, INK)])
gx, gy, gw_, gh_ = ML + Inches(0.55), Inches(2.95), Inches(5.0), Inches(2.4)
conn(s, gx, gy + gh_, gx + gw_, gy + gh_, HAIR, 1.0)
linechart(s, gx + Inches(0.15), gy + Inches(0.15), gw_ - Inches(0.4), gh_ - Inches(0.4),
          [0.8, 0.68, 0.52, 0.38, 0.3], color=SILVER)
linechart(s, gx + Inches(0.15), gy + Inches(0.15), gw_ - Inches(0.4), gh_ - Inches(0.4),
          [0.2, 0.32, 0.5, 0.68, 0.85], color=BLUE)
text(s, gx + gw_ - Inches(1.55), gy + Inches(0.02), Inches(1.7), Inches(0.28),
     [("운영·개선 수요", 9.5, True, BLUE)])
text(s, gx + gw_ - Inches(1.85), gy + gh_ - Inches(0.72), Inches(2.0), Inches(0.28),
     [("신규 구축(PoC) 수요", 9.5, True, GRAY)])
for i, yr in enumerate(["2023", "2024", "2025", "2026", "2027"]):
    text(s, gx + (gw_ - Inches(0.4)) * i / 4 - Inches(0.2), gy + gh_ + Inches(0.07),
         Inches(0.7), Inches(0.24), [(yr, 8.5, False, GRAY)], align=PP_ALIGN.CENTER)
ins = [
    ("PoC → 운영", "‘만들 수 있는가’에서 ‘계속 잘 돌아가는가’로 — 운영 단계 좌초가 다수"),
    ("1 → N개", "기업당 특화 Agent 수십 개 시대 — 개별 관리는 10개부터 통제 불능"),
    ("AgentOps 공백", "Agent 형상관리 표준 부재 — 한국어·On-prem 수요는 더 비어 있다"),
]
for i, (kw, b_) in enumerate(ins):
    y = Inches(2.3) + Inches(1.2) * i
    kw_block(s, ML + Inches(6.35), y, Inches(5.15), kw, b_, kw_color=INK)
box(s, ML, Inches(6.05), CW, Inches(0.78), PEARL, HAIR)
text(s, ML + Inches(0.4), Inches(6.23), CW - Inches(0.8), Inches(0.5), [
    ([("Insight — ", 12.5, True, BLUE),
      ("기업 AI의 경쟁력은 ‘모델’이 아니라, 지식 → Agent → 운영 → 개선을 돌리는 체계에서 나온다.", 12.5, True, INK)],)])

# ============================================================
# 06 · 고객 Pain Point (01)
# ============================================================
s = content("01", "고객 Pain Point",
            lead=lead_runs([("세 개의 자리, ", False), ("하나의 고통", True), (" — 교집합은 ‘운영 체계 부재’", False)]),
            mode="parchment")
voices = [
    ("AI 개발팀장", "“봇 하나 추가하는데 왜 두 달이 걸리죠?”", "전처리·프롬프트 재작업 → 리드타임 폭증"),
    ("서비스 운영 담당", "“답변이 틀렸다는데, 뭘 고쳐야 할지 모르겠어요.”", "로그가 흩어져 원인 추적 불가"),
    ("정보보호 · 경영진", "“부서마다 AI를 따로 만드는데, 통제가 됩니까?”", "중복 투자 · 이력 부재 · 보안 리스크"),
]
for i, (role, quote, pain) in enumerate(voices):
    y = Inches(2.3) + Inches(1.5) * i
    box(s, ML, y, Inches(6.55), Inches(1.36), WHITE, HAIR)
    pill(s, ML + Inches(0.3), y + Inches(0.23), Inches(1.72), Inches(0.34), role, PARCH, MUT80, 9.5)
    text(s, ML + Inches(2.25), y + Inches(0.2), Inches(4.1), Inches(1.0), [
        (quote, 12.5, True, INK, 4), (pain, 9.5, False, MUT48)], spacing=1.2)
vc = (ML + Inches(9.35), Inches(4.15))
r_ = Inches(1.25); off = Inches(0.74)
c1 = (vc[0] - off, vc[1] - Inches(0.42))
c2 = (vc[0] + off, vc[1] - Inches(0.42))
c3 = (vc[0], vc[1] + Inches(0.76))
for (cx, cy), col, lw_ in [(c1, SILVER, 1.5), (c2, SILVER, 1.5), (c3, BLUE, 2.0)]:
    box(s, cx - r_, cy - r_, r_ * 2, r_ * 2, None, col, lw=lw_, shape=MSO_SHAPE.OVAL)
text(s, c1[0] - Inches(1.3), c1[1] - r_ - Inches(0.3), Inches(2.4), Inches(0.28),
     [("개발", 10.5, True, MUT48)], align=PP_ALIGN.CENTER)
text(s, c2[0] - Inches(1.1), c2[1] - r_ - Inches(0.3), Inches(2.4), Inches(0.28),
     [("운영", 10.5, True, MUT48)], align=PP_ALIGN.CENTER)
text(s, c3[0] - Inches(1.2), c3[1] + r_ + Inches(0.05), Inches(2.4), Inches(0.28),
     [("보안 · 경영", 10.5, True, BLUE)], align=PP_ALIGN.CENTER)
text(s, vc[0] - Inches(1.15), vc[1] - Inches(0.26), Inches(2.3), Inches(0.6), [
    ("공통분모", 9, True, MUT48, 2), ("운영 체계 부재", 12.5, True, INK)], align=PP_ALIGN.CENTER)

# ============================================================
# 07 · 솔루션 개요 (02)
# ============================================================
s = content("02", "솔루션 개요",
            lead=lead_runs([("One Console AI — ", False), ("하나의 콘솔, 하나의 선순환", True)]))
rc = (Inches(6.67), Inches(4.45)); rr = Inches(1.42)
box(s, rc[0] - rr, rc[1] - rr, rr * 2, rr * 2, None, HAIR, lw=1.4, shape=MSO_SHAPE.OVAL)
for ang in (45, 135, 225, 315):
    ax = rc[0] + rr * math.cos(math.radians(ang - 90))
    ay = rc[1] + rr * math.sin(math.radians(ang - 90))
    tb = text(s, ax - Inches(0.14), ay - Inches(0.15), Inches(0.3), Inches(0.3),
              [("➔", 12, True, BLUE)], align=PP_ALIGN.CENTER)
    tb.rotation = ang
dot(s, rc[0], rc[1], Inches(1.62), WHITE, BLUE)
text(s, rc[0] - Inches(0.81), rc[1] - Inches(0.3), Inches(1.62), Inches(0.65), [
    ("One Console", 11.5, True, BLUE, 2), ("하나의 콘솔", 9, False, MUT48)], align=PP_ALIGN.CENTER)
nodes = [
    ("① Knowledge", "흩어진 문서를 RAG 파이프라인으로 정제", rc[0] - Inches(1.5), rc[1] - rr - Inches(1.22)),
    ("② Agent Config", "bot_type 키로 프롬프트·검색 범위 형상관리", rc[0] + rr + Inches(0.35), rc[1] - Inches(0.48)),
    ("③ AI Agent", "REST API로 형상을 호출, 서비스로 수렴", rc[0] - Inches(1.5), rc[1] + rr + Inches(0.25)),
    ("④ 운영 · 개선", "로그·피드백이 콘솔로 되돌아와 다음 개선", rc[0] - rr - Inches(3.45), rc[1] - Inches(0.48)),
]
for (h_, b_, x, y) in nodes:
    box(s, x, y, Inches(3.1), Inches(0.96), WHITE, HAIR)
    text(s, x + Inches(0.22), y + Inches(0.15), Inches(2.7), Inches(0.7), [
        (h_, 12.5, True, BLUE, 3), (b_, 9.5, False, MUT80)], spacing=1.15)
text(s, ML, Inches(6.75), CW, Inches(0.3),
     [("④ → ① 운영 신호가 지식과 형상으로 되돌아온다 — 운영할수록 좋아지는 폐쇄 루프", 11, True, MUT48)],
     align=PP_ALIGN.CENTER)

# ============================================================
# 07-B · 제품 둘러보기 (02) — 실제 UI 스크린샷
# ============================================================
s = content("02", "제품 둘러보기",
            lead=lead_runs([("슬라이드가 아니라, ", False), ("실제 동작하는 제품", True), ("입니다.", False)]))
shot_fit(s, ML, Inches(2.4), Inches(6.7), Inches(3.9), "dashboard.png",
         title="One Console AI · localhost:8000",
         cap="실데이터로 동작하는 대시보드 — 선순환 구조·KPI·파이프라인 현황을 한 화면에")
rx = ML + Inches(7.05)
text(s, rx, Inches(2.4), Inches(4.5), Inches(0.3), [("함께 구현된 핵심 화면", 12, True, INK)])
grid = [("knowledge.png", "RAG 파이프라인"), ("prompts.png", "프롬프트 형상관리"),
        ("operations.png", "운영 대시보드"), ("api.png", "ITCEN-API · Chat")]
tw = Inches(2.14)
for i, (nm, lb) in enumerate(grid):
    tx = rx + (tw + Inches(0.24)) * (i % 2)
    ty = Inches(2.9) + Inches(1.78) * (i // 2)
    thumb(s, tx, ty, tw, nm, lb)
pill(s, rx, Inches(6.28), Inches(4.5), Inches(0.44),
     "8개 화면 · 19개 REST API 모두 실제 구현 완료", BLUE, WHITE, 10.5)

# ============================================================
# 08 · Knowledge (02)
# ============================================================
s = content("02", "핵심 기능 ① Knowledge",
            lead=lead_runs([("어떤 문서든, ", False), ("같은 규칙", True), ("으로 지식이 된다.", False)]))
srcs = ["Confluence", "PDF", "Excel", "이미지"]
for i, t_ in enumerate(srcs):
    x = ML + Inches(1.5) * i
    pill(s, x, Inches(2.3), Inches(1.38), Inches(0.36), t_, PEARL, MUT80, 9.5, line=HAIR)
    conn(s, x + Inches(0.69), Inches(2.66), ML + Inches(0.95), Inches(3.05), HAIR, 1.0)
flow = ["수집", "추출", "전처리", "가공", "적재", "RAGaaS 동기화"]
gap = Inches(0.07); fw = (CW - gap * 5) / 6
for i, t_ in enumerate(flow):
    last = i == len(flow) - 1
    sp = box(s, ML + (fw + gap) * i, Inches(3.05), fw, Inches(0.76),
             BLUE if last else PEARL, None if last else HAIR,
             shape=MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON)
    tf = sp.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = Inches(0.08)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = t_; _set_font(r, 11, True, WHITE if last else INK)
box(s, ML, Inches(4.15), Inches(5.85), Inches(2.5), PEARL, HAIR)
text(s, ML + Inches(0.35), Inches(4.4), Inches(5.2), Inches(2.1), [
    ("가공 단계 출력 규칙 — 전 파이프라인 강제", 12.5, True, INK, 8),
    ("✓  모든 출력은 반드시 한국어", 10.5, False, MUT80, 4),
    ("✓  서론 · 결론 · 인사말 금지", 10.5, False, MUT80, 4),
    ("✓  추측성 표현 금지 (“~인 것 같습니다” 차단)", 10.5, False, MUT80, 4),
    ("✓  사실 위주의 건조하고 명확한 문장", 10.5, False, MUT80, 7),
    ("규칙 위반 출력은 적재 전 자동 반려 · 재생성", 10.5, True, BLUE)])
box(s, ML + Inches(6.15), Inches(4.15), Inches(5.94), Inches(2.5), WHITE, HAIR)
text(s, ML + Inches(6.5), Inches(4.4), Inches(5.2), Inches(0.85), [
    ([("8주+", 26, True, GRAY, -0.6), ("  →  ", 18, False, GRAY), ("수일", 26, True, BLUE, -0.6)], 3),
    ("신규 지식 구축 리드타임", 11, True, INK)])
bx0, bw0 = ML + Inches(6.5), Inches(4.6)
box(s, bx0, Inches(5.5), bw0, Inches(0.28), PARCH, HAIR, r_px=6)
box(s, bx0, Inches(5.9), bw0 * 0.12, Inches(0.28), BLUE, r_px=6)
text(s, bx0 + bw0 + Inches(0.08), Inches(5.5), Inches(0.8), Inches(0.26), [("현행", 8.5, False, GRAY)])
text(s, bx0 + bw0 * 0.12 + Inches(0.08), Inches(5.9), Inches(1.2), Inches(0.26), [("플랫폼", 8.5, True, BLUE)])
text(s, ML + Inches(6.5), Inches(6.32), Inches(5.2), Inches(0.3),
     [("노하우가 플랫폼 기능으로 축적 · 최신성 자동 추적 · Index 단위 보안 경계", 9, False, MUT48)])

# ============================================================
# 09 · Agent Config (02)
# ============================================================
s = content("02", "핵심 기능 ② Agent Config",
            lead=lead_runs([("bot_type", True), (" — 하나의 키가 모든 형상을 꿴다.", False)]))
box(s, ML, Inches(2.4), Inches(3.4), Inches(2.5), TILE)
text(s, ML + Inches(0.35), Inches(2.72), Inches(2.8), Inches(1.95), [
    ("고유 KEY", 10, True, BLUE_D, 5),
    ([("bot_type", 27, True, WHITE, -0.5)], 8),
    ("생성 시 정하는 이 키에 형상이 매달리고,\n외부 호출도 이 키 하나로 식별됩니다.", 9.5, False, BODY_D)],
    spacing=1.2)
branches = [
    ("① 에이전트 생성", "이름 · 도메인 · 담당자 등록"),
    ("② System Prompt", "말투·역할 — 저장마다 새 버전, 원클릭 롤백"),
    ("③ 벡터 검색 설정", "Index · Top-K · 유사도 · 출처 인용 강제"),
]
bx = ML + Inches(4.55)
for i, (h_, b_) in enumerate(branches):
    y = Inches(2.28) + Inches(0.95) * i
    conn(s, ML + Inches(3.4), Inches(3.65), bx, y + Inches(0.41), HAIR, 1.0)
    box(s, bx, y, Inches(7.15), Inches(0.82), WHITE, HAIR)
    text(s, bx + Inches(0.3), y + Inches(0.13), Inches(6.6), Inches(0.58), [
        ([(h_, 12, True, INK), ("    " + b_, 10, False, MUT48)],)], anchor=MSO_ANCHOR.MIDDLE)
gx = ML + Inches(4.55); gy = Inches(5.35)
text(s, gx, gy - Inches(0.02), Inches(1.4), Inches(0.28), [("형상 완성도", 10, True, MUT48)])
for i in range(3):
    box(s, gx + Inches(1.3) + Inches(0.92) * i, gy, Inches(0.82), Inches(0.24), BLUE, r_px=5)
text(s, gx + Inches(4.2), gy - Inches(0.02), Inches(2.9), Inches(0.28),
     [("3/3 → 자동 ‘운영’ 전환", 10.5, True, BLUE)])
yv = Inches(6.1)
conn(s, ML + Inches(0.5), yv + Inches(0.12), ML + Inches(7.0), yv + Inches(0.12), HAIR, 1.2)
for i, (v, active) in enumerate([("v1.0", False), ("v1.1", False), ("v1.2", True)]):
    x = ML + Inches(0.45) + Inches(2.95) * i
    dot(s, x + Inches(0.12), yv + Inches(0.12), Inches(0.24), BLUE if active else WHITE,
        None if active else HAIR)
    text(s, x - Inches(0.36), yv + Inches(0.32), Inches(1.0), Inches(0.26),
         [(v, 10, active, BLUE if active else MUT48)], align=PP_ALIGN.CENTER)
text(s, ML + Inches(7.7), yv - Inches(0.05), Inches(4.1), Inches(0.62), [
    ("모든 변경이 버전으로 기록 — 문제 시 즉시 롤백", 10.5, True, INK)], spacing=1.2)

# ============================================================
# 10 · 운영 루프 (02)
# ============================================================
s = content("02", "핵심 기능 ③ 운영 · 개선 루프",
            lead=lead_runs([("운영 신호가, ", False), ("콘솔로 되돌아온다", True), (".", False)]))
loop = [
    ("수집", "답변 로그 전건 기록\n피드백 · 사용량 회귀"),
    ("판정", "★2 이하 → 개선 큐\n인용 실패 → 지식 공백"),
    ("조치", "Prompt 새 버전 배포\n검색 조정 · 재수집"),
    ("형상 기록", "개선 전후를 버전 비교\n효과가 데이터로 증명"),
]
nw = Inches(2.8)
for i, (h_, b_) in enumerate(loop):
    x = ML + (nw + Inches(0.3)) * i
    box(s, x, Inches(2.3), nw, Inches(1.52), PEARL if i < 3 else WHITE,
        HAIR if i < 3 else BLUE, lw=1.3)
    text(s, x + Inches(0.26), Inches(2.52), nw - Inches(0.5), Inches(1.1), [
        (h_, 13.5, True, BLUE if i == 3 else INK, 5), (b_, 9.5, False, MUT80)], spacing=1.22)
    if i < 3:
        text(s, x + nw + Inches(0.015), Inches(2.82), Inches(0.3), Inches(0.45),
             [("→", 14, True, GRAY)], align=PP_ALIGN.CENTER)
box(s, ML, Inches(4.2), Inches(6.4), Inches(2.45), WHITE, HAIR)
text(s, ML + Inches(0.4), Inches(4.4), Inches(5.6), Inches(0.3),
     [("개선 사이클 반복 → 만족도 상승 (파일럿 운영 예시)", 11.5, True, INK)])
gx, gy, gw_, gh_ = ML + Inches(0.55), Inches(4.88), Inches(5.3), Inches(1.42)
conn(s, gx, gy + gh_, gx + gw_, gy + gh_, HAIR, 1.0)
xs, ys = linechart(s, gx + Inches(0.15), gy + Inches(0.1), gw_ - Inches(0.4), gh_ - Inches(0.32),
                   [0.15, 0.3, 0.42, 0.58, 0.75, 0.9], color=BLUE)
text(s, xs[0] - Inches(0.18), ys[0] + Inches(0.08), Inches(0.7), Inches(0.24), [("86%", 9, True, GRAY)])
text(s, xs[-1] - Inches(0.55), ys[-1] - Inches(0.28), Inches(0.8), Inches(0.24), [("94%", 10, True, BLUE)])
text(s, gx, gy + gh_ + Inches(0.05), gw_, Inches(0.24),
     [("개선 사이클 1 → 6회", 8.5, False, GRAY)], align=PP_ALIGN.CENTER)
box(s, ML + Inches(6.7), Inches(4.2), Inches(5.39), Inches(2.45), TILE)
text(s, ML + Inches(7.05), Inches(4.45), Inches(4.7), Inches(2.0), [
    ([("4시간+ ", 18, True, BLUE_D, -0.4), ("멈춘 작업 자동 정리", 13, True, WHITE)], 6),
    ("장시간 running 작업을 판정·강제 종료 — 운영 안정성을 사람 없이 확보", 10, False, BODY_D, 9),
    ("“운영할수록 좋아진다”가 버전 비교로 증명 — 경쟁 입찰의 결정적 레퍼런스", 10, True, WHITE)],
    spacing=1.26)

# ============================================================
# 11 · 개발 연동 (02)
# ============================================================
s = content("02", "개발 연동 · ITCEN-API",
            lead=lead_runs([("등록한 형상을, ", False), ("REST로 그대로", True), (" 쓴다.", False)]),
            mode="parchment")
box(s, ML, Inches(2.3), Inches(6.35), Inches(3.15), INK)
code = [
    ("# 형상 가져오기", GRAY),
    ("GET  /agent/prompt/{bot_type}", BLUE_D),
    ("GET  /agent/ragaas-config/{bot_type}", BLUE_D),
    ("", WHITE),
    ("# 대화 호출 — 형상(Prompt+검색) 자동 적용", GRAY),
    ("POST /agent/chat", WHITE),
    ('     {"bot_type": "hr-assistant",', BODY_D),
    ('      "message": "육아휴직은 최대 얼마나?"}', BODY_D),
    ("", WHITE),
    ("# 피드백 회귀 — 운영 신호의 시작점", GRAY),
    ("POST /agent/feedback", WHITE),
]
tb = text(s, ML + Inches(0.4), Inches(2.56), Inches(5.6), Inches(2.7),
          [(t_, 10.5, False, c_) for (t_, c_) in code], spacing=1.26)
for p in tb.text_frame.paragraphs:
    for r in p.runs: r.font.name = "Consolas"
chips = [("19", "엔드포인트"), ("3", "형상 API"), ("0초", "저장=배포")]
for i, (v, l) in enumerate(chips):
    x = ML + Inches(2.17) * i
    box(s, x, Inches(5.65), Inches(1.98), Inches(0.72), WHITE, HAIR)
    text(s, x, Inches(5.75), Inches(1.98), Inches(0.55), [
        ([(v, 15, True, BLUE, -0.3), ("  " + l, 9.5, False, MUT48)],)],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
rt = ML + Inches(6.7)
text(s, rt, Inches(2.3), Inches(4.9), Inches(0.3),
     [("자동 생성 API 문서 · Swagger UI", 12, True, INK)])
shot_fit(s, rt, Inches(2.72), Inches(4.9), Inches(3.3), "swagger.png",
         title="localhost:8000/docs")
pill(s, rt, Inches(6.5), Inches(4.9), Inches(0.44),
     "LIVE DEMO — 발표장에서 실제 제품으로 시연", BLUE, WHITE, 10.5)

# ============================================================
# 12 · 차별성 (02)
# ============================================================
s = content("02", "차별성",
            lead=lead_runs([("‘만드는 도구’가 아니라, ", False), ("‘좋아지게 만드는 체계’", True), (".", False)]))
crit = [
    ("한국어 사내문서 파이프라인", "✕", "△", "✓"),
    ("프롬프트+검색 통합 형상관리", "✕", "△", "✓"),
    ("운영 → 개선 폐쇄 루프", "✕", "△", "✓"),
    ("On-prem 구축형 (공공·금융)", "—", "✕", "✓"),
    ("현장 운영으로 검증", "—", "△", "✓"),
]
tblf = s.shapes.add_table(6, 4, int(ML), int(Inches(2.35)), int(Inches(7.5)), int(Inches(3.8)))
tbl = tblf.table
tbl.columns[0].width = Inches(3.2)
tbl.columns[1].width = Inches(1.44)
tbl.columns[2].width = Inches(1.44)
tbl.columns[3].width = Inches(1.42)
heads = ["", "개별 구축", "해외 SaaS", "One Console"]
for j, h_ in enumerate(heads):
    c = tbl.cell(0, j)
    c.fill.solid(); c.fill.fore_color.rgb = BLUE if j == 3 else INK
    c.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = c.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = h_; _set_font(r, 10.5, True, WHITE)
for i, row in enumerate(crit, start=1):
    for j, v in enumerate(row):
        c = tbl.cell(i, j)
        c.fill.solid(); c.fill.fore_color.rgb = PEARL if j == 3 else WHITE
        c.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = c.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER
        r = p.add_run(); r.text = ("  " + v) if j == 0 else v
        if j == 0:   _set_font(r, 10.5, True, INK)
        elif j == 3: _set_font(r, 14, True, BLUE)
        else:        _set_font(r, 12, False, GRAY)
px, py, pw_, ph_ = ML + Inches(8.1), Inches(2.6), Inches(3.55), Inches(3.3)
text(s, px, Inches(2.32), pw_, Inches(0.28), [("포지셔닝", 10.5, True, MUT48)])
conn(s, px, py + ph_, px + pw_, py + ph_, HAIR, 1.0)
conn(s, px, py, px, py + ph_, HAIR, 1.0)
text(s, px + pw_ - Inches(1.8), py + ph_ + Inches(0.05), Inches(1.9), Inches(0.24),
     [("형상·운영 통합도 →", 8.5, False, GRAY)], align=PP_ALIGN.RIGHT)
tb = text(s, px - Inches(0.34), py + Inches(0.75), Inches(0.3), Inches(1.6),
          [("국내 적합성 →", 8.5, False, GRAY)])
tb.rotation = 270
for (l, fx, fy, c_, d_) in [("개별 구축", 0.18, 0.42, GRAY, Inches(0.15)),
                            ("해외 SaaS", 0.66, 0.2, GRAY, Inches(0.15)),
                            ("One Console AI", 0.8, 0.8, BLUE, Inches(0.25))]:
    cx = px + pw_ * fx; cy = py + ph_ * (1 - fy)
    dot(s, cx, cy, d_, c_)
    text(s, cx - Inches(0.9), cy + Inches(0.13), Inches(1.8), Inches(0.26),
         [(l, 9, c_ == BLUE, c_)], align=PP_ALIGN.CENTER)
text(s, ML, Inches(6.45), CW, Inches(0.35),
     [("결정적 차이 — 이 체계는 이미 현장에서 돌아가고 있습니다.", 12.5, True, INK)],
     align=PP_ALIGN.CENTER)

# ============================================================
# 13 · 그룹 시너지 (02)
# ============================================================
s = content("02", "아이티센 그룹 시너지",
            lead=lead_runs([("아이티센이라서, ", False), ("되는 사업", True), (".", False)]))
hc = (Inches(6.67), Inches(4.45))
syn = [
    ("SI 수행력", "공공·금융 구축 경험 → On-prem 딜리버리 즉시 소화", "플랫폼+구축 패키지", ML, Inches(2.35)),
    ("고객 기반", "그룹 고객망 → 파일럿·레퍼런스 최단 경로", "기존 계약 Add-on", SW - ML - Inches(4.5), Inches(2.35)),
    ("클라우드 · MSP", "그룹 클라우드와 결합 → 매니지드 운영 매출", "구독+운영 반복 매출", ML, Inches(5.25)),
    ("AI 사업 표준화", "그룹 AI 공통 기반 → 원가 절감·품질 상향", "내부 효율+외부 판매", SW - ML - Inches(4.5), Inches(5.25)),
]
box(s, hc[0] - Inches(1.6), hc[1] - Inches(0.6), Inches(3.2), Inches(1.2), BLUE, r_px=20)
text(s, hc[0] - Inches(1.6), hc[1] - Inches(0.38), Inches(3.2), Inches(0.8), [
    ("One Console AI", 14.5, True, WHITE, 3), ("그룹 역량의 교차점", 9.5, False, WHITE)],
    align=PP_ALIGN.CENTER)
for (h_, b_, tag, x, y) in syn:
    box(s, x, y, Inches(4.5), Inches(1.56), PEARL, HAIR)
    text(s, x + Inches(0.32), y + Inches(0.22), Inches(3.9), Inches(0.85), [
        (h_, 13.5, True, INK, 4), (b_, 10, False, MUT80)], spacing=1.2)
    pill(s, x + Inches(0.32), y + Inches(1.06), Inches(1.95), Inches(0.34), tag, WHITE, BLUE, 8.5, line=HAIR)
    ex = x + Inches(4.5) if x == ML else x
    conn(s, ex, y + Inches(0.78), hc[0] + (Inches(-1.6) if x == ML else Inches(1.6)),
         hc[1] + (Inches(-0.28) if y == Inches(2.35) else Inches(0.28)), HAIR, 1.0)
text(s, ML, Inches(7.0) - Inches(0.06), CW, Inches(0.3),
     [("우리가 매일 하는 일(SI·운영)을 반복 매출 구조로 바꾸는 사업입니다.", 11.5, True, INK)],
     align=PP_ALIGN.CENTER)

# ============================================================
# 14 · 시장 (03)
# ============================================================
s = content("03", "시장",
            lead=lead_runs([("커지는 판, ", False), ("비어 있는 자리", True), (".", False)]))
cx, cy = Inches(3.0), Inches(4.55)
for r_, fill, line_ in [(Inches(1.9), PARCH, HAIR), (Inches(1.28), WHITE, HAIR), (Inches(0.7), BLUE, None)]:
    box(s, cx - r_, cy - r_, r_ * 2, r_ * 2, fill, line_, shape=MSO_SHAPE.OVAL)
text(s, cx - Inches(1.0), cy - Inches(1.78), Inches(2.0), Inches(0.36),
     [("TAM  ~3조", 12, True, MUT80)], align=PP_ALIGN.CENTER)
text(s, cx - Inches(1.0), cy - Inches(1.14), Inches(2.0), Inches(0.32),
     [("SAM  ~3,000억", 11, True, MUT80)], align=PP_ALIGN.CENTER)
text(s, cx - Inches(0.7), cy - Inches(0.29), Inches(1.4), Inches(0.6), [
    ("SOM", 9.5, True, WHITE, 2), ("~50억", 14, True, WHITE)], align=PP_ALIGN.CENTER)
bx0, by0 = Inches(5.35), Inches(6.15)
for i, hgt in enumerate([0.33, 0.52, 0.76, 1.05]):
    box(s, bx0 + Inches(0.4) * i, by0 - Inches(hgt), Inches(0.28), Inches(hgt),
        BLUE if i == 3 else PARCH, None if i == 3 else HAIR, r_px=3)
text(s, bx0 - Inches(0.2), by0 + Inches(0.05), Inches(2.2), Inches(0.24),
     [("’25 → ’28 시장 성장(추정)", 8, False, GRAY)])
rt = Inches(7.3)
why = [
    ("왜 지금인가", "PoC 예산이 운영 예산으로 전환되는 변곡점 — 운영 플랫폼 구매가 시작"),
    ("왜 비어 있나", "해외 SaaS는 한국어 파이프라인 · On-prem · 공공 보안 요건에 구조적으로 취약"),
    ("왜 우리인가", "구축 소화력(SI) + 레퍼런스를 만들 고객망을 동시 보유한 사업자는 드물다"),
]
for i, (h_, b_) in enumerate(why):
    kw_block(s, rt, Inches(2.45) + Inches(1.35) * i, Inches(5.1), h_, b_)
text(s, ML, Inches(6.85), Inches(11), Inches(0.26),
     [("※ TAM 국내 기업용 생성형 AI(2027E) · SAM LLMOps/AgentOps · SOM 3년 목표(20~30사) — 추정치", 8.5, False, GRAY)])

# ============================================================
# 15 · 수익 모델 (03)
# ============================================================
s = content("03", "수익 모델",
            lead=lead_runs([("구축", True), ("으로 열고, ", False), ("구독·운영", True), ("으로 쌓는다.", False)]))
streams = [
    ("① 구축 (SI)", "1~3억 / 건", "설치 + 지식 파이프라인 초기 구축"),
    ("② 구독 (라이선스)", "월 300~1,000만", "Agent 수·사용량 티어 — 핵심 반복 매출"),
    ("③ 운영 (MSP)", "월 500만~", "모니터링 · 개선 리포트 · 튜닝 대행"),
]
cw3 = Inches(3.9)
for i, (h_, price, b_) in enumerate(streams):
    x = ML + (cw3 + Inches(0.2)) * i
    box(s, x, Inches(2.3), cw3, Inches(1.72), WHITE, HAIR)
    text(s, x + Inches(0.3), Inches(2.52), cw3 - Inches(0.6), Inches(1.3), [
        (h_, 11.5, True, MUT48, 4), ([(price, 19, True, BLUE, -0.4)], 5), (b_, 9.5, False, MUT80)],
        spacing=1.2)
box(s, ML, Inches(4.3), Inches(6.4), Inches(2.25), PEARL, HAIR)
text(s, ML + Inches(0.4), Inches(4.5), Inches(5.6), Inches(0.3),
     [("연차별 매출 구성 (예시) — 반복 매출 비중이 커진다", 11.5, True, INK)])
bx0, by0 = ML + Inches(0.9), Inches(6.28)
years = [([0.62, 0.16, 0.07], "1년차"), ([0.5, 0.45, 0.18], "2년차"), ([0.4, 0.76, 0.4], "3년차")]
cols = [SILVER, BLUE, INK]
for i, (segs_, label) in enumerate(years):
    x = bx0 + Inches(1.7) * i
    yy = by0
    for v, c_ in zip(segs_, cols):
        h_ = Inches(v * 1.15)
        box(s, x, yy - h_, Inches(0.72), h_ - Inches(0.03), c_, r_px=3)
        yy -= h_
    text(s, x - Inches(0.22), by0 + Inches(0.05), Inches(1.2), Inches(0.24),
         [(label, 8.5, False, GRAY)], align=PP_ALIGN.CENTER)
for i, (l, c_) in enumerate([("구축", SILVER), ("구독", BLUE), ("운영", INK)]):
    y = Inches(5.0) + Inches(0.38) * i
    box(s, ML + Inches(5.15), y + Inches(0.03), Inches(0.2), Inches(0.2), c_, r_px=4)
    text(s, ML + Inches(5.45), y, Inches(0.9), Inches(0.26), [(l, 9, False, MUT80)])
box(s, ML + Inches(6.7), Inches(4.3), Inches(5.39), Inches(2.25), TILE)
text(s, ML + Inches(7.05), Inches(4.58), Inches(4.7), Inches(1.75), [
    ("지식과 형상이 쌓일수록,\n떠나기 어려워진다", 14.5, True, WHITE, 7),
    ("고객이 축적한 자산이 곧 전환 비용 —\n1회성 SI가 3~5년 락인 구독·운영 매출로", 10, False, BODY_D)],
    spacing=1.28)
text(s, ML, Inches(6.82), Inches(8), Inches(0.26),
     [("※ 가격·구성은 예시 — 파일럿에서 지불의사 검증 후 확정", 8.5, False, GRAY)])

# ============================================================
# 16 · 로드맵 (03)
# ============================================================
s = content("03", "사업화 로드맵",
            lead=lead_runs([("완벽한 계획보다, ", False), ("실행 가능한 첫걸음", True), (".", False)]))
ty = Inches(3.45)
conn(s, ML + Inches(0.5), ty, ML + Inches(11.6), ty, HAIR, 1.4)
phases = [
    ("현재", "MVP 검증 완료", ["콘솔+API+파이프라인 구현", "현장에서 운영 모델 확인"], "데모 가능", True),
    ("~ 6개월", "유상 파일럿", ["그룹 고객 1~2사 PoC", "지불의사 · 가격 검증"], "파일럿 1건 계약", False),
    ("~ 18개월", "제품화 v1.0", ["멀티테넌트 · 설치형 패키징", "공공·금융 진입"], "레퍼런스 2~3건", False),
    ("18개월 ~", "산업 확장", ["산업별 템플릿 · 파트너 채널", "MSP 운영 매출 본격화"], "고객 20~30사", False),
]
for i, (period, h_, bullets, kpi, active) in enumerate(phases):
    x = ML + Inches(0.5) + Inches(3.7) * i
    dot(s, x, ty, Inches(0.26), BLUE if active else WHITE, None if active else HAIR)
    text(s, x - Inches(1.2), ty - Inches(0.95), Inches(2.4), Inches(0.72), [
        (period, 10.5, True, BLUE if active else MUT48, 3), (h_, 14, True, INK)],
        align=PP_ALIGN.CENTER)
    text(s, x - Inches(1.5), ty + Inches(0.28), Inches(3.0), Inches(0.95),
         [("· " + b_, 9.5, False, MUT80, 4) for b_ in bullets], align=PP_ALIGN.CENTER, spacing=1.2)
    pill(s, x - Inches(1.1), ty + Inches(1.42), Inches(2.2), Inches(0.4), kpi,
         BLUE if active else PEARL, WHITE if active else MUT80, 9.5,
         line=None if active else HAIR)
box(s, ML, Inches(5.9), CW, Inches(0.85), PEARL, HAIR)
text(s, ML + Inches(0.45), Inches(6.1), CW - Inches(0.9), Inches(0.5), [
    ([("첫걸음은 이미 뗐습니다 — ", 12.5, True, BLUE),
      ("필요한 것은 파일럿 고객 1개사와 소규모 TF. 6개월 내 유상 레퍼런스로 증명하겠습니다.", 12.5, True, INK)],)])

# ============================================================
# 17 · 실행력 (04)
# ============================================================
s = content("04", "실행력",
            lead=lead_runs([("아이디어가 아니라, ", False), ("제품으로", True), (" 왔습니다.", False)]),
            mode="parchment")
text(s, ML, Inches(2.25), Inches(3.0), Inches(0.28), [("제품 준비도", 10.5, True, MUT48)])
text(s, SW - ML - Inches(1.5), Inches(2.25), Inches(1.5), Inches(0.28),
     [("4 / 5 완료", 10.5, True, BLUE)], align=PP_ALIGN.RIGHT)
gseg = ["콘솔", "ITCEN-API", "RAG 파이프라인", "운영 루프", "엔터프라이즈 요건"]
sw_ = (CW - Inches(0.4)) / 5
for i, l in enumerate(gseg):
    done = i < 4
    box(s, ML + (sw_ + Inches(0.1)) * i, Inches(2.58), sw_, Inches(0.4),
        BLUE if done else WHITE, None if done else HAIR, r_px=7)
    text(s, ML + (sw_ + Inches(0.1)) * i, Inches(2.65), sw_, Inches(0.28),
         [(("✓ " if done else "") + l, 9.5, True, WHITE if done else MUT48)],
         align=PP_ALIGN.CENTER)
box(s, ML, Inches(3.3), Inches(5.9), Inches(3.1), WHITE, HAIR)
done_list = ["관리 콘솔 8개 화면 — 지식·형상·운영·개선",
             "ITCEN-API 19개 REST 엔드포인트 + Swagger",
             "RAG 파이프라인 (추출→전처리→가공→적재)",
             "bot_type 형상관리 — 버전 · 롤백 · 즉시 배포",
             "운영 루프 — 피드백 회귀 · 멈춘 작업(4h+) 정리"]
paras = [("이미 만들어 둔 것", 13.5, True, INK, 9)]
paras += [([("✓  ", 11, True, BLUE), (d, 10.5, False, MUT80)], 6) for d in done_list]
paras.append(("→ 발표장에서 라이브 데모로 확인시켜 드립니다", 10.5, True, BLUE))
text(s, ML + Inches(0.4), Inches(3.55), Inches(5.15), Inches(2.7), paras, spacing=1.2)
box(s, ML + Inches(6.2), Inches(3.3), Inches(5.9), Inches(3.1), WHITE, HAIR)
text(s, ML + Inches(6.6), Inches(3.55), Inches(5.1), Inches(2.7), [
    ("다음 단계를 위해 필요한 것", 13.5, True, INK, 9),
    ("·  TF 4~6인 (기획 1 · 개발 3 · AI 1) — 6개월", 10.5, False, MUT80, 5),
    ("·  파일럿 고객 1~2사 연결 (그룹 영업망 협조)", 10.5, False, MUT80, 5),
    ("·  엔터프라이즈 보안 요건 보강 예산", 10.5, False, MUT80, 11),
    ("6개월 목표", 12, True, BLUE, 5),
    ("·  유상 파일럿 1건 계약", 10.5, False, MUT80, 4),
    ("·  운영 데이터로 개선 효과 정량 입증", 10.5, False, MUT80)], spacing=1.2)
text(s, ML, Inches(6.7), CW, Inches(0.32),
     [("본 제안서의 모든 화면과 API는 제안팀이 직접 구현했습니다 — 선정 즉시, 다음 날부터 시작합니다.", 11.5, True, INK)],
     align=PP_ALIGN.CENTER)

# ============================================================
# 18 · 클로징
# ============================================================
s = base("black")
conn(s, ML, Inches(1.0), ML + Inches(0.44), Inches(1.0), BLUE, 2.4)
conn(s, ML + Inches(0.45), Inches(1.0), SW - ML, Inches(1.0), RGBColor(0x3A, 0x3A, 0x3E), 1.0)
text(s, ML, Inches(0.55), Inches(8), Inches(0.3),
     [("One Console AI — 마무리", 11, False, GRAY)])
text(s, ML, Inches(2.0), Inches(11.8), Inches(2.0), [
    ([("기업 AI를,", 44, True, WHITE, -1.0)], 4),
    ([("프로젝트가 아닌 ", 44, True, WHITE, -1.0), ("플랫폼", 44, True, BLUE_D, -1.0),
      ("으로.", 44, True, WHITE, -1.0)],)], spacing=1.12)
box(s, ML + Inches(0.03), Inches(4.15), Inches(0.56), Inches(0.05), BLUE, r_px=99)
for i, (v, l) in enumerate([("-52%", "신규 Agent 리드타임"), ("-38%", "중복 Agent · 운영비"),
                            ("선순환", "운영할수록 좋아지는 품질")]):
    x = ML + Inches(4.0) * i
    text(s, x, Inches(4.6), Inches(3.6), Inches(1.1), [
        ([(v, 28, True, WHITE, -0.6)], 4), (l, 11, False, GRAY)])
box(s, 0, Inches(6.35), SW, Inches(0.62), TILE, shape=MSO_SHAPE.RECTANGLE)
text(s, ML, Inches(6.5), Inches(12.2), Inches(0.32),
     [("감사합니다   |   라이브 데모(콘솔 + Swagger UI) 준비 완료   |   ※ 효과 수치는 수행 경험 기반 추정", 10.5, False, BODY_D)])

out = Path(__file__).resolve().parent / "One_Console_AI_제안서_v6_UI.pptx"
prs.save(out)
print(f"saved: {out} / slides: {len(prs.slides._sldIdLst)}")
