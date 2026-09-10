"""قاعدة البيانات (SQLite) لمشروع الجزائر BTPH.

الملفات المرفوعة تُخزَّن على القرص، ويُحفظ مسارها داخل حقل `documents`
(JSON) في سجل الفاتورة نفسه — كما هو مطلوب.
"""

from __future__ import annotations

import os
from datetime import date
from pathlib import Path

from sqlalchemy import JSON, Date, Float, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, session, sessionmaker

# <repo>/algeria_btph/backend/db.py → parents[2] = algeria-btph/
_PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = Path(os.environ.get("BTPH_DB_PATH", _PROJECT_ROOT / "data" / "btph.db"))


class Base(DeclarativeBase):
    """أساس ORM."""


class InvoiceRecord(Base):
    """سجل الفاتورة — حقل `documents` يحمل الملفات/الصور/سجلات التدقيق داخل الفاتورة."""

    __tablename__ = "invoices"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    invoice_number: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    invoice_name: Mapped[str] = mapped_column(String(255))
    issue_date: Mapped[date] = mapped_column(Date)
    project_ref: Mapped[str | None] = mapped_column(String(128), nullable=True)
    customer_ref: Mapped[str | None] = mapped_column(String(128), nullable=True)
    description: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    currency: Mapped[str] = mapped_column(String(8), default="DZD")
    total_amount: Mapped[float] = mapped_column(Float, default=0.0)
    vat_rate: Mapped[float] = mapped_column(Float, default=0.19)
    status: Mapped[str] = mapped_column(String(32), default="draft")
    created_at: Mapped[date] = mapped_column(Date, default=date.today)
    documents: Mapped[list] = mapped_column(JSON, default=list)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<InvoiceRecord {self.invoice_number} docs={len(self.documents or [])}>"


_engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False},
)
_SessionLocal = sessionmaker(bind=_engine, autoflush=False, expire_on_commit=False)


def init_db() -> None:
    """إنشاء مجلد البيانات والجداول إن لم تكن موجودة."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(_engine)


def session_scope() -> session.Session:
    """جلسة قاعدة بيانات جديدة (نمط with)."""
    return _SessionLocal()


init_db()
