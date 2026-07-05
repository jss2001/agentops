# -*- coding: utf-8 -*-
# Vercel Python 서버리스 진입점 — FastAPI 앱(ASGI)을 그대로 노출한다.
# vercel.json 의 rewrites 가 /agent/*, /itcen/*, /docs 요청을 이 함수로 보낸다.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from server.main import app  # noqa: E402,F401  (Vercel이 `app` 변수를 ASGI로 인식)
