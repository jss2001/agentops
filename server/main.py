# ============================================================
# One Console AI · ITCEN-API (FastAPI)
# AI Agent 통합 형상관리 플랫폼 백엔드
#  - ITCEN  : 콘솔(웹)에서 사용하는 관리용 API
#  - Agent: 외부 AI Agent 개발에서 호출하는 제공용 API (REST)
# Swagger UI: http://localhost:8000/docs
# ============================================================
import json
import random
import re
import sqlite3
import threading
import time
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from fastapi import BackgroundTasks, Body, FastAPI, HTTPException, Path as FPath
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = Path(__file__).resolve().parent / "itcen.db"
_db_lock = threading.Lock()

# ------------------------------------------------------------
# DB
# ------------------------------------------------------------
def _connect():
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con

_con = _connect()

@contextmanager
def db():
    with _db_lock:
        yield _con
        _con.commit()

def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def ago(**kw) -> str:
    return (datetime.now() - timedelta(**kw)).strftime("%Y-%m-%d %H:%M:%S")

SCHEMA = """
CREATE TABLE IF NOT EXISTS agents(
  bot_type TEXT PRIMARY KEY, name TEXT NOT NULL, domain TEXT, description TEXT,
  owner TEXT, icon TEXT DEFAULT '🤖', tint TEXT DEFAULT '#4b5cff',
  status TEXT DEFAULT '운영', created_at TEXT);
CREATE TABLE IF NOT EXISTS prompts(
  id INTEGER PRIMARY KEY AUTOINCREMENT, bot_type TEXT NOT NULL, version TEXT NOT NULL,
  content TEXT NOT NULL, message TEXT, author TEXT, created_at TEXT);
CREATE TABLE IF NOT EXISTS ragaas_configs(
  bot_type TEXT PRIMARY KEY, index_name TEXT NOT NULL, top_k INTEGER DEFAULT 5,
  similarity_threshold REAL DEFAULT 0.72, bm25_weight REAL DEFAULT 0.3,
  rerank INTEGER DEFAULT 1, citation_required INTEGER DEFAULT 1,
  pii_masking INTEGER DEFAULT 1, multi_query INTEGER DEFAULT 0, updated_at TEXT);
CREATE TABLE IF NOT EXISTS knowledge_sources(
  id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, type TEXT, index_name TEXT,
  docs INTEGER DEFAULT 0, chunks INTEGER DEFAULT 0,
  stage TEXT DEFAULT '대기', progress INTEGER DEFAULT 0,
  freshness INTEGER DEFAULT 100, last_sync TEXT);
CREATE TABLE IF NOT EXISTS chunks(
  id INTEGER PRIMARY KEY AUTOINCREMENT, index_name TEXT, doc TEXT, content TEXT);
CREATE TABLE IF NOT EXISTS chat_logs(
  id INTEGER PRIMARY KEY AUTOINCREMENT, bot_type TEXT, question TEXT, answer TEXT,
  citations TEXT DEFAULT '[]', latency_ms INTEGER, rating INTEGER, feedback TEXT,
  created_at TEXT);
CREATE TABLE IF NOT EXISTS jobs(
  id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, bot_type TEXT,
  status TEXT DEFAULT 'running', started_at TEXT, ended_at TEXT, note TEXT);
CREATE TABLE IF NOT EXISTS pipeline_rules(
  id INTEGER PRIMARY KEY AUTOINCREMENT, rule TEXT);
"""

def seed():
    with db() as con:
        con.executescript(SCHEMA)
        if con.execute("SELECT COUNT(*) c FROM agents").fetchone()["c"]:
            return

        agents = [
            ("hr-assistant", "HR 인사비서", "인사/총무", "사내 인사규정·복리후생 질의응답", "김서연", "👤", "#4b5cff"),
            ("sales-copilot", "영업지원 Agent", "영업", "실적·경쟁사·제안서 지식 기반 영업 지원", "박준호", "📈", "#12b886"),
            ("manual-qa", "제품 매뉴얼 봇", "CS/기술지원", "제품 매뉴얼·이미지 기반 기술 질의응답", "최민아", "📘", "#8b7cff"),
            ("security-policy", "보안규정 Agent", "정보보안", "사내 보안 정책·심사 기준 안내", "정하늘", "🛡️", "#fa5252"),
            ("dev-onboarding", "개발 온보딩 봇", "R&D", "개발 위키 기반 신규 입사자 온보딩", "한지우", "💻", "#3b9dff"),
        ]
        for bt, name, dom, desc, owner, icon, tint in agents:
            con.execute(
                "INSERT INTO agents(bot_type,name,domain,description,owner,icon,tint,status,created_at) "
                "VALUES(?,?,?,?,?,?,?,?,?)",
                (bt, name, dom, desc, owner, icon, tint, "운영", ago(days=30)))

        prompts = {
            "hr-assistant": (
                "당신은 사내 인사 규정에 정통한 HR 어시스턴트입니다.\n"
                "- 모든 답변은 한국어로 작성한다.\n"
                "- 연차는 회계연도(1/1) 기준으로 계산하되, 입사 1년 미만은 월 단위 발생분을 안내한다.\n"
                "- 2026년 개정 규정(연차 이월 최대 5일)을 항상 우선 적용한다.\n"
                "- 답변 마지막에 반드시 근거 규정 조항을 인용한다.\n"
                "- 근거 문서를 찾지 못한 경우, 추측 대신 인사팀 문의 채널(#hr-help)을 안내한다."),
            "sales-copilot": (
                "당신은 B2B 영업 조직을 지원하는 영업 코파일럿입니다.\n"
                "- 모든 답변은 한국어, 사실 위주의 건조하고 명확한 문장으로 작성한다.\n"
                "- 수치를 인용할 때는 반드시 기준 시점과 출처 문서를 함께 명시한다.\n"
                "- 확인되지 않은 경쟁사 정보는 답변에 포함하지 않는다."),
            "manual-qa": (
                "당신은 제품 매뉴얼 기술지원 어시스턴트입니다.\n"
                "- 절차 안내는 번호가 매겨진 단계로 제시한다.\n"
                "- 안전 관련 경고가 문서에 있으면 반드시 함께 안내한다.\n"
                "- 매뉴얼에 없는 조작 방법은 안내하지 않는다."),
            "security-policy": (
                "당신은 사내 정보보안 규정 안내 어시스턴트입니다.\n"
                "- 불확실한 경우 단정하지 말고 근거 문서 링크를 우선 제시한다.\n"
                "- 규정 위반 소지가 있는 요청에는 보안팀 승인 절차를 안내한다."),
            "dev-onboarding": (
                "당신은 신규 입사 개발자의 온보딩을 돕는 어시스턴트입니다.\n"
                "- 개발 위키의 최신 문서를 근거로 답한다.\n"
                "- 코드/명령어는 코드 블록으로 제시한다."),
        }
        for bt, content in prompts.items():
            con.execute(
                "INSERT INTO prompts(bot_type,version,content,message,author,created_at) VALUES(?,?,?,?,?,?)",
                (bt, "v1.0", content, "최초 등록", "admin", ago(days=30)))
        # hr-assistant는 개정 이력 시연용으로 버전 몇 개 추가
        con.execute("INSERT INTO prompts(bot_type,version,content,message,author,created_at) VALUES(?,?,?,?,?,?)",
                    ("hr-assistant", "v1.1", prompts["hr-assistant"], "출장 정산 예외 케이스 few-shot 추가", "김서연", ago(days=6)))
        con.execute("INSERT INTO prompts(bot_type,version,content,message,author,created_at) VALUES(?,?,?,?,?,?)",
                    ("hr-assistant", "v1.2", prompts["hr-assistant"], "퇴직/연차 규정 최신화 반영 · 톤 정중화", "김서연", ago(hours=2)))

        cfgs = [
            ("hr-assistant", "hr-knowledge", 5, 0.72, 0.3, 1, 1, 1, 0),
            ("sales-copilot", "sales-docs", 8, 0.70, 0.3, 1, 1, 1, 0),
            ("manual-qa", "product-manual", 6, 0.72, 0.4, 1, 1, 0, 0),
            ("security-policy", "security-policy", 5, 0.74, 0.3, 1, 1, 1, 0),
            ("dev-onboarding", "dev-wiki", 5, 0.70, 0.2, 1, 0, 0, 0),
        ]
        for c in cfgs:
            con.execute(
                "INSERT INTO ragaas_configs(bot_type,index_name,top_k,similarity_threshold,bm25_weight,"
                "rerank,citation_required,pii_masking,multi_query,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?)",
                (*c, ago(days=4)))

        sources = [
            ("Confluence 스페이스 · 인사/총무", "confluence", "hr-knowledge", 1204, 4820, "완료", 100, 99, ago(minutes=20)),
            ("제품 매뉴얼 PDF (v3.2)", "pdf", "product-manual", 86, 1980, "가공", 62, 62, ago(hours=1)),
            ("영업 실적 데이터.xlsx", "excel", "sales-docs", 318, 2690, "완료", 100, 100, ago(hours=8)),
            ("회로도·다이어그램 이미지", "image", "product-manual", 440, 1160, "전처리", 35, 74, ago(hours=3)),
            ("보안정책 문서 (PDF·Word)", "pdf", "security-policy", 142, 1910, "완료", 100, 74, ago(days=12)),
            ("개발위키 (Confluence·Git)", "confluence", "dev-wiki", 2430, 5680, "완료", 100, 97, ago(minutes=5)),
        ]
        for s in sources:
            con.execute(
                "INSERT INTO knowledge_sources(name,type,index_name,docs,chunks,stage,progress,freshness,last_sync) "
                "VALUES(?,?,?,?,?,?,?,?,?)", s)

        chunks = [
            ("hr-knowledge", "인사규정 제32조", "육아휴직은 자녀 1명당 최대 1년 사용 가능하다. 남녀 근로자 모두 신청할 수 있으며, 대상은 만 8세 이하 또는 초등학교 2학년 이하 자녀를 둔 근로자이다."),
            ("hr-knowledge", "인사규정 제18조", "연차유급휴가는 회계연도(1월 1일) 기준으로 산정한다. 입사 1년 미만 근로자는 1개월 개근 시 1일의 연차가 발생한다. 2026년 개정 규정에 따라 연차 이월은 최대 5일까지 허용된다."),
            ("hr-knowledge", "근무유연제 가이드 v4", "재택근무는 매주 금요일 18시까지 익주 일정에 대해 신청하며, 팀장 승인 후 확정된다. 주 최대 3일까지 재택근무를 사용할 수 있다."),
            ("hr-knowledge", "복리후생 안내 2026", "경조사 지원은 본인 결혼 시 유급휴가 5일과 경조금이 지급된다. 자녀 학자금은 고등학교와 대학교 재학 자녀를 대상으로 연 1회 지원된다."),
            ("hr-knowledge", "출장여비 규정 제7조", "국내 출장 일비는 직급과 무관하게 1일 30,000원이며, 숙박비는 영수증 실비로 정산한다. 출장 종료 후 5영업일 이내에 정산을 완료해야 한다."),
            ("sales-docs", "영업전략_2026Q4.pptx", "2026년 4분기 자사 제품 가격은 경쟁 3사 평균 대비 +7% 수준의 중상위 포지셔닝이다. TCO 관점에서는 유지보수 비용이 낮아 3년 총비용 기준 경쟁 우위에 있다."),
            ("sales-docs", "시장분석 리포트 12월호", "4분기 주요 경쟁사의 가격 인하 폭은 평균 -4.2%로 집계되었다. 프리미엄 세그먼트 수요는 전년 대비 11% 증가했다."),
            ("sales-docs", "제안서_A고객사_최종", "A고객사 제안의 핵심 근거는 유지보수 비용 절감이다. 자사 솔루션 도입 시 연간 운영비가 기존 대비 18% 절감되는 것으로 산정되었다."),
            ("product-manual", "X-200 매뉴얼 5장", "X-200 펌웨어 초기화 절차. 1. 전원 버튼을 10초간 눌러 안전모드로 진입한다. 2. 설정 메뉴에서 초기화를 선택한다. 3. 재부팅 후 펌웨어 버전을 확인한다. 초기화 중 전원을 차단하면 장비가 손상될 수 있다."),
            ("product-manual", "X-200 매뉴얼 2장", "X-200의 정격 전압은 220V이며, 동작 온도 범위는 0도에서 40도이다. 습도 80% 이상 환경에서는 사용을 권장하지 않는다."),
            ("security-policy", "정보보안규정 제12조", "사외 반출 문서는 문서보안(DRM) 해제 승인을 받아야 한다. 승인권자는 부서장이며, 반출 이력은 6개월간 보관된다."),
            ("security-policy", "정보보안규정 제20조", "외부 클라우드 서비스 이용 시 보안팀 사전 심사가 필요하다. 고객 개인정보가 포함된 데이터는 사외 클라우드 저장이 금지된다."),
            ("dev-wiki", "온보딩 가이드", "개발 환경 구성은 사내 미러 저장소를 사용한다. VPN 접속 후 셋업 스크립트를 실행하면 표준 개발 환경이 자동 구성된다."),
            ("dev-wiki", "배포 프로세스 v3", "운영 배포는 화요일과 목요일 오후 2시에 진행된다. 배포 전 스테이징 환경에서 회귀 테스트 통과가 필수이다."),
        ]
        con.executemany("INSERT INTO chunks(index_name,doc,content) VALUES(?,?,?)", chunks)

        rules = [
            "모든 출력은 반드시 한국어로 작성한다.",
            "불필요한 서론·결론·인사말을 절대 포함하지 않는다.",
            "추측성 발언(예: \"이 이미지는 ~인 것 같습니다\")을 절대 포함하지 않는다.",
            "사실 위주의 건조하고 명확한 문장으로 구성한다.",
        ]
        con.executemany("INSERT INTO pipeline_rules(rule) VALUES(?)", [(r,) for r in rules])

        jobs = [
            ("대용량 PDF 파싱 · 제품 매뉴얼 v3.2", "manual-qa", "running", ago(hours=6), None, "OCR 처리 중 응답 없음"),
            ("외부 API 대기 · CRM 연동 조회", "sales-copilot", "running", ago(hours=5), None, "타임아웃 미설정 호출"),
            ("임베딩 배치 · 보안정책 재색인", "security-policy", "running", ago(hours=4, minutes=30), None, "워커 응답 없음"),
            ("규정 검색 · 연차 질의", "hr-assistant", "running", ago(minutes=2), None, None),
            ("일일 사용량 집계 배치", None, "done", ago(hours=9), ago(hours=8, minutes=40), None),
        ]
        con.executemany(
            "INSERT INTO jobs(name,bot_type,status,started_at,ended_at,note) VALUES(?,?,?,?,?,?)", jobs)

        # 운영 로그 시드 (7일 분포)
        seed_logs = [
            ("hr-assistant", "육아휴직은 최대 얼마나 쓸 수 있나요?", 5, 1180),
            ("hr-assistant", "재택근무 신청 마감일이 언제야?", 5, 920),
            ("sales-copilot", "경쟁사 대비 우리 제품 가격 포지셔닝 요약해줘", 4, 2100),
            ("manual-qa", "모델 X-200 펌웨어 초기화 절차 알려줘", 2, 3400),
            ("security-policy", "고객 데이터 외부 클라우드에 올려도 돼?", 4, 1500),
            ("dev-onboarding", "개발 환경 어떻게 세팅해?", 5, 1100),
            ("hr-assistant", "출장 일비가 얼마인가요?", 5, 870),
            ("sales-copilot", "A고객사 제안 핵심 근거 알려줘", 4, 1900),
        ]
        for i, (bt, q, rating, lat) in enumerate(seed_logs):
            con.execute(
                "INSERT INTO chat_logs(bot_type,question,answer,citations,latency_ms,rating,created_at) "
                "VALUES(?,?,?,?,?,?,?)",
                (bt, q, "(시드 로그) 근거 문서 기반 응답이 제공되었다.", "[]", lat, rating,
                 ago(days=random.randint(0, 6), hours=random.randint(0, 12))))

seed()

# ------------------------------------------------------------
# Pydantic 모델 (Swagger 스키마)
# ------------------------------------------------------------
class AgentCreate(BaseModel):
    bot_type: str = Field(..., description="봇을 가리키는 고유 key id. 프롬프트·검색 설정이 이 키에 매달립니다.", examples=["hr-assistant"])
    name: str = Field(..., description="에이전트 표시 이름", examples=["HR 인사비서"])
    domain: str = Field("", description="도메인 (인사/영업/CS 등)")
    description: str = Field("", description="에이전트 설명")
    owner: str = Field("", description="담당자")
    icon: str = Field("🤖", description="아이콘(이모지)")
    tint: str = Field("#4b5cff", description="테마 색상(hex)")

class PromptUpdate(BaseModel):
    content: str = Field(..., description="System Prompt 전문")
    message: str = Field("변경 사항", description="변경 메시지 (커밋 메시지처럼 기록됨)")
    author: str = Field("admin", description="작성자")

class RagaasConfigUpdate(BaseModel):
    index_name: str = Field(..., description="RAGaaS 인덱스 이름", examples=["hr-knowledge"])
    top_k: int = Field(5, ge=1, le=20, description="검색 문서 수 (Top-K)")
    similarity_threshold: float = Field(0.72, ge=0, le=1, description="유사도 임계값 — 미만 문서는 컨텍스트에서 제외")
    bm25_weight: float = Field(0.3, ge=0, le=1, description="하이브리드 가중치(BM25 비중, 나머지는 Vector)")
    rerank: bool = Field(True, description="Cross-Encoder 재정렬 사용")
    citation_required: bool = Field(True, description="출처 인용 강제 — 근거 미발견 시 '정보 없음' 반환")
    pii_masking: bool = Field(True, description="응답 내 개인정보 자동 마스킹")
    multi_query: bool = Field(False, description="멀티-쿼리 확장 (비용 증가)")

class ChatRequest(BaseModel):
    bot_type: str = Field(..., description="호출할 봇의 고유 key id", examples=["hr-assistant"])
    message: str = Field(..., description="사용자 질문", examples=["육아휴직은 최대 얼마나 쓸 수 있나요?"])
    session_id: Optional[str] = Field(None, description="대화 세션 식별자(선택)")

class Citation(BaseModel):
    doc: str = Field(..., description="근거 문서명")
    score: float = Field(..., description="유사도 점수")
    snippet: str = Field(..., description="근거 문단 발췌")

class ChatResponse(BaseModel):
    log_id: int = Field(..., description="답변 로그 ID — 피드백 전송 시 사용")
    bot_type: str
    answer: str = Field(..., description="한국어 답변 (출력 규칙 적용)")
    citations: list[Citation] = Field(..., description="근거 문서 목록")
    latency_ms: int
    config_version: str = Field(..., description="적용된 System Prompt 버전")

class FeedbackRequest(BaseModel):
    log_id: int = Field(..., description="ChatResponse의 log_id")
    rating: int = Field(..., ge=1, le=5, description="1(불만족) ~ 5(만족)")
    comment: Optional[str] = Field(None, description="피드백 코멘트(선택)")

class SourceCreate(BaseModel):
    name: str = Field(..., description="데이터 소스 이름", examples=["신제품 매뉴얼 PDF"])
    type: str = Field(..., description="confluence | pdf | excel | image", examples=["pdf"])
    index_name: str = Field(..., description="적재할 RAGaaS 인덱스", examples=["product-manual"])
    docs: int = Field(10, description="문서 수(시뮬레이션용)")

# ------------------------------------------------------------
# App
# ------------------------------------------------------------
TAGS = [
    {"name": "agent", "description": "**외부 제공 API** — 플랫폼에 등록한 형상(Prompt·검색 설정)을 AI Agent 개발에서 REST로 자유롭게 호출합니다. `bot_type`으로 봇을 식별합니다."},
    {"name": "itcen-config", "description": "**Agent Config 관리** — bot_type 하나로 ①에이전트 ②System Prompt ③벡터 검색 설정을 묶어 중앙 형상관리합니다."},
    {"name": "itcen-knowledge", "description": "**Knowledge (RAG 파이프라인)** — Confluence·PDF·Excel·이미지를 추출→전처리→가공→적재로 정제해 RAGaaS Index와 동기화합니다."},
    {"name": "itcen-ops", "description": "**운영 대시보드** — 답변 로그·피드백·사용량을 모니터링하고, 4시간 이상 멈춘 작업을 강제 종료합니다."},
]

app = FastAPI(
    title="One Console AI · ITCEN-API",
    version="1.0.0",
    description=(
        "AI Agent 통합 형상관리 플랫폼의 API입니다.\n\n"
        "- **하나의 콘솔**: 흩어진 사내 지식을 RAG 파이프라인으로 정제하고, Agent Config로 봇의 성격과 검색 범위를 빚어 AI Agent로 수렴합니다.\n"
        "- 운영 신호는 다시 콘솔로 돌아와 다음 개선의 출발점이 됩니다.\n"
        "- ITCEN(콘솔)에 등록한 내용은 이 ITCEN-API를 통해 외부에서 호출할 수 있습니다."
    ),
    openapi_tags=TAGS,
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def _agent_or_404(bot_type: str):
    with db() as con:
        row = con.execute("SELECT * FROM agents WHERE bot_type=?", (bot_type,)).fetchone()
    if not row:
        raise HTTPException(404, f"bot_type '{bot_type}'을(를) 찾을 수 없습니다. 먼저 에이전트를 생성하세요.")
    return dict(row)

def _active_prompt(bot_type: str):
    with db() as con:
        return con.execute(
            "SELECT * FROM prompts WHERE bot_type=? ORDER BY id DESC LIMIT 1", (bot_type,)).fetchone()

# ============================================================
# Agent API (외부 제공)
# ============================================================
@app.get("/agent/prompt/{bot_type}", tags=["agent"], summary="System Prompt 조회",
         description="bot_type에 등록된 최신(active) System Prompt를 반환합니다. AI Agent 개발 시 이 값을 LLM system 메시지로 사용합니다.")
def get_agent_prompt(bot_type: str = FPath(..., description="봇 고유 key id", examples=["hr-assistant"])):
    _agent_or_404(bot_type)
    p = _active_prompt(bot_type)
    if not p:
        raise HTTPException(404, f"'{bot_type}'에 등록된 System Prompt가 없습니다.")
    return {"bot_type": bot_type, "version": p["version"], "system_prompt": p["content"],
            "updated_at": p["created_at"], "author": p["author"]}

@app.get("/agent/ragaas-config/{bot_type}", tags=["agent"], summary="RAGaaS 검색 설정 조회",
         description="bot_type에 등록된 벡터 검색 설정(지식 범위·검색 정책)을 반환합니다.")
def get_agent_ragaas_config(bot_type: str = FPath(..., description="봇 고유 key id", examples=["hr-assistant"])):
    _agent_or_404(bot_type)
    with db() as con:
        c = con.execute("SELECT * FROM ragaas_configs WHERE bot_type=?", (bot_type,)).fetchone()
    if not c:
        raise HTTPException(404, f"'{bot_type}'에 등록된 검색 설정이 없습니다.")
    d = dict(c)
    for k in ("rerank", "citation_required", "pii_masking", "multi_query"):
        d[k] = bool(d[k])
    return d

_PII_RE = [
    (re.compile(r"\b01[016789]-?\d{3,4}-?\d{4}\b"), "010-****-****"),
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "***@***.***"),
    (re.compile(r"\b\d{6}-?[1-4]\d{6}\b"), "******-*******"),
]

def _retrieve(index_name: str, query: str, cfg: dict):
    tokens = [t for t in re.split(r"[\s,.\?!·'\"()\[\]]+", query) if len(t) >= 2]
    with db() as con:
        rows = con.execute("SELECT * FROM chunks WHERE index_name=?", (index_name,)).fetchall()
    scored = []
    for r in rows:
        hits = sum(1 for t in tokens if t in r["content"] or t in r["doc"])
        # 부분 일치(2글자 어근) 보정 — 조사/어미가 붙은 한국어 토큰 대응
        partial = sum(1 for t in tokens if len(t) >= 3 and any(
            t[:2] in r["content"] for _ in [0]) and t not in r["content"])
        score = hits + 0.5 * min(partial, 2)
        if score <= 0:
            continue
        sim = round(min(0.97, 0.66 + 0.07 * score), 2)
        if sim >= cfg["similarity_threshold"]:
            scored.append({"doc": r["doc"], "score": sim, "snippet": r["content"][:120]})
    scored.sort(key=lambda x: -x["score"])
    return scored[: cfg["top_k"]]

@app.post("/agent/chat", tags=["agent"], response_model=ChatResponse, summary="Agent 대화 호출",
          description=(
              "bot_type의 형상(System Prompt + RAGaaS 검색 설정)을 적용해 답변을 생성합니다.\n\n"
              "- 등록된 지식 인덱스에서 검색 → 근거 문서와 함께 한국어 답변 반환\n"
              "- `citation_required`가 켜져 있고 근거를 찾지 못하면 추측 대신 '정보 없음'을 반환\n"
              "- 모든 호출은 답변 로그로 기록되어 운영 대시보드로 되돌아옵니다 (개선 신호)"))
def agent_chat(req: ChatRequest):
    t0 = time.perf_counter()
    _agent_or_404(req.bot_type)
    p = _active_prompt(req.bot_type)
    with db() as con:
        c = con.execute("SELECT * FROM ragaas_configs WHERE bot_type=?", (req.bot_type,)).fetchone()
    if not p or not c:
        raise HTTPException(409, "형상이 불완전합니다. ①에이전트 ②프롬프트 ③검색 설정을 모두 등록하세요.")
    cfg = dict(c)

    cites = _retrieve(cfg["index_name"], req.message, cfg)
    time.sleep(random.uniform(0.15, 0.45))  # 생성 지연 시뮬레이션

    if cites:
        lines = [f"{ci['snippet']} (출처: {ci['doc']})" for ci in cites[:3]]
        answer = "\n".join(lines)
    elif cfg["citation_required"]:
        answer = ("요청하신 내용에 대한 근거 문서를 지식 베이스에서 찾을 수 없습니다. "
                  "추측에 의한 답변은 제공하지 않습니다. 담당 채널에 문의하시기 바랍니다.")
    else:
        answer = "지식 베이스에서 관련 문서를 찾지 못했습니다. 일반적인 안내가 필요하면 질문을 구체화하시기 바랍니다."

    if cfg["pii_masking"]:
        for rx, repl in _PII_RE:
            answer = rx.sub(repl, answer)

    latency = int((time.perf_counter() - t0) * 1000)
    with db() as con:
        cur = con.execute(
            "INSERT INTO chat_logs(bot_type,question,answer,citations,latency_ms,created_at) VALUES(?,?,?,?,?,?)",
            (req.bot_type, req.message, answer, json.dumps(cites, ensure_ascii=False), latency, now()))
        log_id = cur.lastrowid
    return {"log_id": log_id, "bot_type": req.bot_type, "answer": answer,
            "citations": cites, "latency_ms": latency, "config_version": p["version"]}

@app.post("/agent/feedback", tags=["agent"], summary="답변 피드백 등록",
          description="답변 로그에 사용자 평가를 기록합니다. 낮은 평가는 콘솔의 '지속 개선' 큐로 이관되어 다음 개선의 출발점이 됩니다.")
def agent_feedback(req: FeedbackRequest):
    with db() as con:
        r = con.execute("SELECT id FROM chat_logs WHERE id=?", (req.log_id,)).fetchone()
        if not r:
            raise HTTPException(404, "해당 log_id의 답변 로그가 없습니다.")
        con.execute("UPDATE chat_logs SET rating=?, feedback=? WHERE id=?",
                    (req.rating, req.comment, req.log_id))
    return {"ok": True, "log_id": req.log_id, "rating": req.rating,
            "routed_to_improvement_queue": req.rating <= 2}

# ============================================================
# ITCEN · Agent Config (bot_type 중심 형상관리)
# ============================================================
@app.get("/itcen/agents", tags=["itcen-config"], summary="에이전트 목록",
         description="등록된 모든 에이전트와 형상 완성도(프롬프트/검색 설정 등록 여부)를 반환합니다.")
def list_agents():
    with db() as con:
        rows = [dict(r) for r in con.execute("SELECT * FROM agents ORDER BY created_at").fetchall()]
        for a in rows:
            p = con.execute("SELECT version, created_at FROM prompts WHERE bot_type=? ORDER BY id DESC LIMIT 1",
                            (a["bot_type"],)).fetchone()
            c = con.execute("SELECT index_name FROM ragaas_configs WHERE bot_type=?", (a["bot_type"],)).fetchone()
            stats = con.execute(
                "SELECT COUNT(*) n, AVG(rating) r FROM chat_logs WHERE bot_type=?", (a["bot_type"],)).fetchone()
            a["prompt_version"] = p["version"] if p else None
            a["prompt_updated"] = p["created_at"] if p else None
            a["index_name"] = c["index_name"] if c else None
            a["calls"] = stats["n"]
            a["satisfaction"] = round(stats["r"] * 20) if stats["r"] else None
            a["config_complete"] = bool(p and c)
    return rows

@app.post("/itcen/agents", tags=["itcen-config"], status_code=201, summary="① 에이전트 생성",
          description="bot_type(고유 key id)을 정해 에이전트를 생성합니다. 이후 ②프롬프트 ③검색 설정을 같은 bot_type에 등록해야 운영 가능합니다.")
def create_agent(body: AgentCreate):
    if not re.fullmatch(r"[a-z0-9\-]{3,40}", body.bot_type):
        raise HTTPException(422, "bot_type은 소문자·숫자·하이픈 3~40자여야 합니다. 예: hr-assistant")
    with db() as con:
        if con.execute("SELECT 1 FROM agents WHERE bot_type=?", (body.bot_type,)).fetchone():
            raise HTTPException(409, f"bot_type '{body.bot_type}'이(가) 이미 존재합니다.")
        con.execute(
            "INSERT INTO agents(bot_type,name,domain,description,owner,icon,tint,status,created_at) "
            "VALUES(?,?,?,?,?,?,?,?,?)",
            (body.bot_type, body.name, body.domain, body.description, body.owner,
             body.icon, body.tint, "개발", now()))
    return {"ok": True, "bot_type": body.bot_type, "next": ["PUT /itcen/agents/{bot_type}/prompt", "PUT /itcen/agents/{bot_type}/ragaas-config"]}

@app.get("/itcen/agents/{bot_type}", tags=["itcen-config"], summary="에이전트 상세")
def get_agent(bot_type: str):
    a = _agent_or_404(bot_type)
    with db() as con:
        prompts = [dict(r) for r in con.execute(
            "SELECT id,version,message,author,created_at FROM prompts WHERE bot_type=? ORDER BY id DESC", (bot_type,)).fetchall()]
        cfg = con.execute("SELECT * FROM ragaas_configs WHERE bot_type=?", (bot_type,)).fetchone()
    a["prompt_versions"] = prompts
    a["ragaas_config"] = dict(cfg) if cfg else None
    return a

@app.put("/itcen/agents/{bot_type}/prompt", tags=["itcen-config"], summary="② System Prompt 등록/개정",
         description="새 버전으로 기록됩니다(형상관리). 최신 버전이 GET /agent/prompt/{bot_type}으로 제공됩니다.")
def put_prompt(bot_type: str, body: PromptUpdate):
    _agent_or_404(bot_type)
    with db() as con:
        n = con.execute("SELECT COUNT(*) c FROM prompts WHERE bot_type=?", (bot_type,)).fetchone()["c"]
        ver = f"v{1 + n // 10}.{n % 10}" if n else "v1.0"
        con.execute(
            "INSERT INTO prompts(bot_type,version,content,message,author,created_at) VALUES(?,?,?,?,?,?)",
            (bot_type, ver, body.content, body.message, body.author, now()))
    return {"ok": True, "bot_type": bot_type, "version": ver}

@app.get("/itcen/agents/{bot_type}/prompts", tags=["itcen-config"], summary="Prompt 버전 이력")
def list_prompts(bot_type: str):
    _agent_or_404(bot_type)
    with db() as con:
        return [dict(r) for r in con.execute(
            "SELECT * FROM prompts WHERE bot_type=? ORDER BY id DESC", (bot_type,)).fetchall()]

@app.put("/itcen/agents/{bot_type}/ragaas-config", tags=["itcen-config"], summary="③ 벡터 검색 설정 등록/수정",
         description="bot_type의 지식 범위(인덱스)와 검색 정책을 등록합니다. GET /agent/ragaas-config/{bot_type}으로 제공됩니다.")
def put_ragaas_config(bot_type: str, body: RagaasConfigUpdate):
    _agent_or_404(bot_type)
    with db() as con:
        con.execute(
            "INSERT INTO ragaas_configs(bot_type,index_name,top_k,similarity_threshold,bm25_weight,"
            "rerank,citation_required,pii_masking,multi_query,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?) "
            "ON CONFLICT(bot_type) DO UPDATE SET index_name=excluded.index_name, top_k=excluded.top_k, "
            "similarity_threshold=excluded.similarity_threshold, bm25_weight=excluded.bm25_weight, "
            "rerank=excluded.rerank, citation_required=excluded.citation_required, "
            "pii_masking=excluded.pii_masking, multi_query=excluded.multi_query, updated_at=excluded.updated_at",
            (bot_type, body.index_name, body.top_k, body.similarity_threshold, body.bm25_weight,
             int(body.rerank), int(body.citation_required), int(body.pii_masking), int(body.multi_query), now()))
        # 에이전트 상태 갱신: 형상 완성 시 운영 전환
        # 주의: db() 락은 비재진입이므로 같은 con으로 조회한다 (_active_prompt 호출 금지)
        has_prompt = con.execute(
            "SELECT 1 FROM prompts WHERE bot_type=? LIMIT 1", (bot_type,)).fetchone()
        if has_prompt:
            con.execute("UPDATE agents SET status='운영' WHERE bot_type=? AND status='개발'", (bot_type,))
    return {"ok": True, "bot_type": bot_type}

@app.delete("/itcen/agents/{bot_type}", tags=["itcen-config"], summary="에이전트 삭제")
def delete_agent(bot_type: str):
    _agent_or_404(bot_type)
    with db() as con:
        con.execute("DELETE FROM agents WHERE bot_type=?", (bot_type,))
        con.execute("DELETE FROM prompts WHERE bot_type=?", (bot_type,))
        con.execute("DELETE FROM ragaas_configs WHERE bot_type=?", (bot_type,))
    return {"ok": True}

# ============================================================
# ITCEN · Knowledge (RAG 파이프라인)
# ============================================================
PIPE_STAGES = ["추출", "전처리", "가공", "적재", "완료"]

@app.get("/itcen/knowledge/sources", tags=["itcen-knowledge"], summary="데이터 소스 목록")
def list_sources():
    with db() as con:
        return [dict(r) for r in con.execute("SELECT * FROM knowledge_sources ORDER BY id").fetchall()]

@app.post("/itcen/knowledge/sources", tags=["itcen-knowledge"], status_code=201, summary="데이터 소스 연결")
def create_source(body: SourceCreate):
    if body.type not in ("confluence", "pdf", "excel", "image"):
        raise HTTPException(422, "type은 confluence | pdf | excel | image 중 하나여야 합니다.")
    with db() as con:
        cur = con.execute(
            "INSERT INTO knowledge_sources(name,type,index_name,docs,chunks,stage,progress,freshness,last_sync) "
            "VALUES(?,?,?,?,0,'대기',0,0,NULL)", (body.name, body.type, body.index_name, body.docs))
        return {"ok": True, "id": cur.lastrowid}

def _run_pipeline(source_id: int):
    """추출→전처리→가공→적재 단계를 시뮬레이션하며 진행률을 갱신한다."""
    for i, stage in enumerate(PIPE_STAGES):
        for pct in range(0, 101, 25):
            progress = int((i * 100 + pct) / (len(PIPE_STAGES) - 1)) if stage != "완료" else 100
            progress = min(progress, 100)
            with db() as con:
                con.execute("UPDATE knowledge_sources SET stage=?, progress=? WHERE id=?",
                            (stage, progress, source_id))
            if stage == "완료":
                break
            time.sleep(0.35)
    with db() as con:
        r = con.execute("SELECT docs FROM knowledge_sources WHERE id=?", (source_id,)).fetchone()
        new_chunks = (r["docs"] or 10) * 4
        con.execute(
            "UPDATE knowledge_sources SET stage='완료', progress=100, chunks=?, freshness=100, last_sync=? WHERE id=?",
            (new_chunks, now(), source_id))

@app.post("/itcen/knowledge/sources/{source_id}/sync", tags=["itcen-knowledge"], summary="RAGaaS Index 동기화 실행",
          description="추출→전처리→가공→적재 파이프라인을 실행해 RAGaaS Index와 동기화합니다. 진행 상황은 소스 목록 조회로 확인합니다.")
def sync_source(source_id: int, background: BackgroundTasks):
    with db() as con:
        r = con.execute("SELECT * FROM knowledge_sources WHERE id=?", (source_id,)).fetchone()
    if not r:
        raise HTTPException(404, "데이터 소스를 찾을 수 없습니다.")
    background.add_task(_run_pipeline, source_id)
    return {"ok": True, "id": source_id, "stages": PIPE_STAGES}

@app.get("/itcen/knowledge/rules", tags=["itcen-knowledge"], summary="파이프라인 출력 규칙",
         description="가공(캡셔닝·요약·구조화) 단계의 모든 LLM 출력에 강제 적용되는 규칙입니다.")
def get_rules():
    with db() as con:
        return [r["rule"] for r in con.execute("SELECT rule FROM pipeline_rules ORDER BY id").fetchall()]

@app.get("/itcen/knowledge/indexes", tags=["itcen-knowledge"], summary="RAGaaS Index 현황")
def list_indexes():
    with db() as con:
        rows = con.execute(
            "SELECT index_name, COUNT(*) sources, SUM(docs) docs, SUM(chunks) chunks, MAX(last_sync) last_sync "
            "FROM knowledge_sources GROUP BY index_name").fetchall()
        out = []
        for r in rows:
            bots = [b["bot_type"] for b in con.execute(
                "SELECT bot_type FROM ragaas_configs WHERE index_name=?", (r["index_name"],)).fetchall()]
            out.append({**dict(r), "used_by": bots})
    return out

# ============================================================
# ITCEN · 운영 대시보드
# ============================================================
@app.get("/itcen/ops/logs", tags=["itcen-ops"], summary="답변 로그 조회",
         description="최근 답변 로그와 사용자 피드백. 낮은 평가(★2 이하)는 개선 큐 대상으로 표시됩니다.")
def ops_logs(limit: int = 30, bot_type: Optional[str] = None):
    q = "SELECT * FROM chat_logs"
    args: list = []
    if bot_type:
        q += " WHERE bot_type=?"
        args.append(bot_type)
    q += " ORDER BY id DESC LIMIT ?"
    args.append(limit)
    with db() as con:
        rows = [dict(r) for r in con.execute(q, args).fetchall()]
    for r in rows:
        r["citations"] = json.loads(r["citations"] or "[]")
        r["improvement_queue"] = bool(r["rating"] and r["rating"] <= 2)
    return rows

@app.get("/itcen/ops/usage", tags=["itcen-ops"], summary="사용량·품질 트렌드")
def ops_usage():
    with db() as con:
        total = con.execute("SELECT COUNT(*) n, AVG(latency_ms) lat, AVG(rating) r FROM chat_logs").fetchone()
        per_bot = [dict(r) for r in con.execute(
            "SELECT bot_type, COUNT(*) calls, AVG(rating) rating FROM chat_logs GROUP BY bot_type ORDER BY calls DESC").fetchall()]
        daily = [dict(r) for r in con.execute(
            "SELECT substr(created_at,1,10) day, COUNT(*) calls FROM chat_logs GROUP BY day ORDER BY day").fetchall()]
        low = con.execute("SELECT COUNT(*) n FROM chat_logs WHERE rating<=2").fetchone()["n"]
        cited = con.execute("SELECT COUNT(*) n FROM chat_logs WHERE citations!='[]'").fetchone()["n"]
    sat = round((total["r"] or 0) * 20, 1)
    return {"total_calls": total["n"], "avg_latency_ms": round(total["lat"] or 0),
            "satisfaction": sat, "citation_rate": round(cited / total["n"] * 100, 1) if total["n"] else 0,
            "low_rated": low, "per_bot": per_bot, "daily": daily}

@app.get("/itcen/ops/jobs", tags=["itcen-ops"], summary="실행 작업 목록",
         description="running 상태가 4시간을 초과한 작업은 stuck=true로 표시됩니다.")
def ops_jobs():
    with db() as con:
        rows = [dict(r) for r in con.execute("SELECT * FROM jobs ORDER BY id DESC").fetchall()]
    cutoff = datetime.now() - timedelta(hours=4)
    for r in rows:
        started = datetime.strptime(r["started_at"], "%Y-%m-%d %H:%M:%S")
        r["running_for_min"] = int((datetime.now() - started).total_seconds() // 60) if r["status"] == "running" else None
        r["stuck"] = r["status"] == "running" and started < cutoff
    return rows

@app.post("/itcen/ops/jobs/cleanup", tags=["itcen-ops"], summary="멈춘 작업 정리",
          description="**4시간 이상 running 상태로 멈춘 작업을 강제 종료**합니다. 종료된 작업 목록을 반환합니다.")
def ops_cleanup():
    cutoff = (datetime.now() - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S")
    with db() as con:
        stuck = [dict(r) for r in con.execute(
            "SELECT * FROM jobs WHERE status='running' AND started_at < ?", (cutoff,)).fetchall()]
        con.execute(
            "UPDATE jobs SET status='killed', ended_at=?, note=COALESCE(note,'')||' [4h+ 초과로 자동 정리]' "
            "WHERE status='running' AND started_at < ?", (now(), cutoff))
    return {"ok": True, "killed": len(stuck), "jobs": stuck}

@app.post("/itcen/ops/jobs/simulate-stuck", tags=["itcen-ops"], summary="멈춘 작업 재현(데모)",
          description="데모용 — 5시간 전에 시작해 멈춘 것으로 보이는 작업을 하나 추가합니다.")
def simulate_stuck():
    with db() as con:
        cur = con.execute(
            "INSERT INTO jobs(name,bot_type,status,started_at,note) VALUES(?,?,?,?,?)",
            ("데모 · 대용량 임베딩 배치", "manual-qa", "running", ago(hours=5), "데모용 멈춘 작업"))
        return {"ok": True, "id": cur.lastrowid}

@app.get("/itcen/ops/signals", tags=["itcen-ops"], summary="개선 신호",
         description="운영 데이터에서 도출된 개선 신호 — 낮은 평가 응답과 인용 실패 응답을 개선 큐로 되돌립니다.")
def ops_signals():
    with db() as con:
        low = [dict(r) for r in con.execute(
            "SELECT id,bot_type,question,rating,feedback,created_at FROM chat_logs "
            "WHERE rating<=2 ORDER BY id DESC LIMIT 10").fetchall()]
        uncited = [dict(r) for r in con.execute(
            "SELECT id,bot_type,question,created_at FROM chat_logs "
            "WHERE citations='[]' AND question NOT LIKE '(시드%' ORDER BY id DESC LIMIT 10").fetchall()]
    return {"low_rated": low, "citation_failed": uncited}

# ------------------------------------------------------------
# 정적 파일 (콘솔 웹) — API 라우트 뒤에 마운트
# ------------------------------------------------------------
app.mount("/", StaticFiles(directory=ROOT, html=True), name="console")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
