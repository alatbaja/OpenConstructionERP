from __future__ import annotations

import os
from pathlib import Path
from typing import Any


def build_invoice_storage_path(base: str, invoice_number: str) -> Path:
    """إ returning مسار مجلد الفاتورة للتخزين."""

    return Path(base) / "invoices" / invoice_number


def ensure_invoice_dir(path: Path) -> Path:
    """تأكيد وجود مجلد الفاتورة وإنشاؤهหาก غير موجود."""

    path.mkdir(parents=True, exist_ok=True)
    return path
