"""نقطة تشغيل الخادم — `python -m algeria_btph` يشغّل واجهة FastAPI.

المتغيرات البيئية:
- BTPH_HOST (افتراضي 0.0.0.0)
- BTPH_PORT (افتراضي 8000)
- BTPH_DB_PATH      — مسار ملف SQLite
- BTPH_STORAGE_ROOT — جذر تخزين الملفات المرفوعة
"""

from __future__ import annotations

import os

import uvicorn

from algeria_btph.backend.db import init_db


def serve() -> None:
    """تهيئة قاعدة البيانات ثم تشغيل خادم FastAPI."""
    init_db()
    uvicorn.run(
        "algeria_btph.backend.api:app",
        host=os.environ.get("BTPH_HOST", "0.0.0.0"),
        port=int(os.environ.get("BTPH_PORT", "8000")),
        log_level="info",
    )


if __name__ == "__main__":
    serve()
