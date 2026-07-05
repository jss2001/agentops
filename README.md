# One Console AI

**AI Agent 통합 형상관리 플랫폼 (AgentOps)** — ITCEN 신사업 공모전 제안 프로젝트

흩어진 사내 지식을 RAG 파이프라인으로 정제하고, `bot_type` 하나로 System Prompt·검색 설정을 중앙 형상관리하며, 운영 신호가 다시 콘솔로 되돌아오는 **선순환(Flywheel)** 구조로 기업 AI를 프로젝트가 아닌 플랫폼으로 운영합니다.

## 구성

```
├─ index.html / assets/        # 관리 콘솔 SPA (대시보드·지식·Config·운영·Chat 등 8개 화면)
├─ server/main.py              # FastAPI 백엔드 (ITCEN-API, 19개 REST 엔드포인트 + Swagger)
├─ run.bat                     # 원클릭 실행 (의존성 설치 + uvicorn 기동)
├─ DESIGN.md                   # 디자인 시스템 (Apple 스펙 기반)
└─ proposal/                   # 제안서 PPT 및 생성 스크립트
   ├─ make_proposal.py         #   PPTX 자동 생성 (python-pptx)
   ├─ embed_fonts.py           #   Pretendard 폰트 임베드
   └─ shots/                   #   콘솔 UI 스크린샷
```

## 실행

```bat
run.bat
```
→ 콘솔: http://localhost:8000  ·  Swagger UI: http://localhost:8000/docs

> 요구사항: Python 3.11+ (`fastapi`, `uvicorn`). `run.bat`이 자동 설치합니다.

## 핵심 API

| Method | Path | 설명 |
|---|---|---|
| GET | `/agent/prompt/{bot_type}` | System Prompt 조회 |
| GET | `/agent/ragaas-config/{bot_type}` | 벡터 검색 설정 조회 |
| POST | `/agent/chat` | 형상(Prompt+검색) 적용 대화 호출 |
| POST | `/agent/feedback` | 답변 피드백 회귀 (운영 신호) |
| PUT | `/itcen/agents/{bot_type}/prompt` | 프롬프트 버전 등록/개정 |
| POST | `/itcen/knowledge/sources/{id}/sync` | RAG 파이프라인 실행 |
| POST | `/itcen/ops/jobs/cleanup` | 4시간+ 멈춘 작업 정리 |
