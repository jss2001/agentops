# -*- coding: utf-8 -*-
"""
PPTX에 Pretendard(Regular/Bold)를 임베드해 폰트 미설치 PC에서도 동일하게 렌더링.
원본은 보존하고 *_embedded.pptx 로 저장한다.
실행: py proposal\embed_fonts.py
"""
import shutil, zipfile, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
HERE = Path(__file__).resolve().parent
SRC = HERE / "One_Console_AI_제안서_v8.pptx"
DST = HERE / "One_Console_AI_제안서_v8_embedded.pptx"

FONT_DIR = Path(r"C:\Users\tjdtl\AppData\Local\Microsoft\Windows\Fonts")
REG = FONT_DIR / "Pretendard-Regular.ttf"
BOLD = FONT_DIR / "Pretendard-Bold.ttf"
assert REG.exists() and BOLD.exists(), "Pretendard TTF를 찾을 수 없습니다"

NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_CT = "http://schemas.openxmlformats.org/package/2006/content-types"
NS_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
REL_FONT = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/font"

shutil.copyfile(SRC, SRC.with_suffix(".bak.pptx"))  # 안전 백업

zin = zipfile.ZipFile(SRC, "r")
names = zin.namelist()
data = {n: zin.read(n) for n in names}
zin.close()

# 1) [Content_Types].xml — fntdata 기본 확장자 등록
ct = data["[Content_Types].xml"].decode("utf-8")
if "fntdata" not in ct:
    ct = ct.replace("</Types>",
        '<Default Extension="fntdata" ContentType="application/x-fontdata"/></Types>')
data["[Content_Types].xml"] = ct.encode("utf-8")

# 2) 폰트 파트 추가
data["ppt/fonts/font1.fntdata"] = REG.read_bytes()
data["ppt/fonts/font2.fntdata"] = BOLD.read_bytes()

# 3) presentation.xml.rels — 폰트 관계 추가
rels_path = "ppt/_rels/presentation.xml.rels"
rels = data[rels_path].decode("utf-8")
existing_ids = [int(m) for m in re.findall(r'Id="rId(\d+)"', rels)]
nid = max(existing_ids) + 1 if existing_ids else 1
rid_reg, rid_bold = f"rId{nid}", f"rId{nid+1}"
add = (f'<Relationship Id="{rid_reg}" Type="{REL_FONT}" Target="fonts/font1.fntdata"/>'
       f'<Relationship Id="{rid_bold}" Type="{REL_FONT}" Target="fonts/font2.fntdata"/>')
rels = rels.replace("</Relationships>", add + "</Relationships>")
data[rels_path] = rels.encode("utf-8")

# 4) presentation.xml — embedTrueTypeFonts 속성 + embeddedFontLst (notesSz 뒤)
pres = data["ppt/presentation.xml"].decode("utf-8")
# 4a) 루트 속성 (기존에 없는 것만 추가 — 중복 방지)
if "embedTrueTypeFonts" not in pres:
    pres = re.sub(r"(<p:presentation\b)", r'\1 embedTrueTypeFonts="1"', pres, count=1)
if "saveSubsetFonts" not in pres:
    pres = re.sub(r"(<p:presentation\b)", r'\1 saveSubsetFonts="0"', pres, count=1)
else:  # 전체 폰트를 임베드하므로 subset 플래그를 0으로 정규화
    pres = re.sub(r'saveSubsetFonts="[^"]*"', 'saveSubsetFonts="0"', pres, count=1)
# 4b) embeddedFontLst 삽입 (스키마상 notesSz 다음)
font_lst = (f'<p:embeddedFontLst><p:embeddedFont>'
            f'<p:font typeface="Pretendard"/>'
            f'<p:regular r:id="{rid_reg}"/><p:bold r:id="{rid_bold}"/>'
            f'</p:embeddedFont></p:embeddedFontLst>')
if "<p:notesSz" in pres:
    pres = re.sub(r"(<p:notesSz[^/]*/>)", r"\1" + font_lst, pres, count=1)
else:  # notesSz가 self-close가 아니면 sldSz 뒤에
    pres = re.sub(r"(</p:sldSz>|<p:sldSz[^/]*/>)", r"\1" + font_lst, pres, count=1)
data["ppt/presentation.xml"] = pres.encode("utf-8")

# 5) 다시 zip으로 저장 (대상이 PowerPoint에 열려 잠긴 경우 대체 이름으로)
try:
    zf = zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED)
except PermissionError:
    DST = DST.with_name(DST.stem + "_new" + DST.suffix)
    print(f"[안내] 대상 파일이 열려 있어 대체 이름으로 저장합니다: {DST.name}")
    zf = zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED)
with zf as z:
    for n, b in data.items():
        z.writestr(n, b)

# 검증: 재파싱 + 크기
from pptx import Presentation
p = Presentation(str(DST))
sz_mb = DST.stat().st_size / 1024 / 1024
print(f"saved: {DST}")
print(f"slides: {len(p.slides._sldIdLst)}  size: {sz_mb:.1f} MB")
print(f"embedded: Pretendard Regular({REG.stat().st_size//1024}KB) + Bold({BOLD.stat().st_size//1024}KB)")
