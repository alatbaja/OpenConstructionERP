"""نقطة التشغيل داخل الحزمة — تفعّل `python -m algeria_btph`.

تشغيل الخادم:
    python -m algeria_btph          (من داخل مجلد algeria-btph)
أو عبر Makefile:                    make run
"""

from __future__ import annotations

from algeria_btph.main import serve

if __name__ == "__main__":
    serve()
