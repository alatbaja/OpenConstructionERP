"""مستودع الفواتير (Repository) — عمليات CRUD فوق SQLite."""

from __future__ import annotations

from datetime import date
from typing import Any

from algeria_btph.backend.db import InvoiceRecord, session_scope


def _as_date(value: Any) -> date:
    """تحويل قيمة التاريخ (date أو نص ISO أو None) إلى datetime.date."""
    if value is None or value == "":
        return date.today()
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


def _record_to_dict(rec: InvoiceRecord) -> dict[str, Any]:
    return {
        "id": rec.id,
        "invoice_number": rec.invoice_number,
        "invoice_name": rec.invoice_name,
        "issue_date": rec.issue_date.isoformat(),
        "project_ref": rec.project_ref,
        "customer_ref": rec.customer_ref,
        "description": rec.description,
        "currency": rec.currency,
        "total_amount": rec.total_amount,
        "vat_rate": rec.vat_rate,
        "status": rec.status,
        "created_at": rec.created_at.isoformat(),
        "documents": rec.documents or [],
    }


def _next_invoice_id(sess: session_scope) -> str:  # type: ignore[valid-type]
    from algeria_btph.backend.db import InvoiceRecord as _R

    last = (
        sess.query(_R)
        .order_by(_R.id.desc())
        .first()
    )
    if last is None:
        return "INV-0001"
    try:
        n = int(last.id.split("-")[-1]) + 1
        return f"INV-{n:04d}"
    except ValueError:
        return f"INV-{len(sess.query(_R).all()) + 1:04d}"


def create_invoice(data: dict[str, Any]) -> dict[str, Any]:
    """إنشاء فاتورة جديدة مع وثائقها (المسارات فقط)."""
    with session_scope() as sess:
        rec = InvoiceRecord(
            id=_next_invoice_id(sess),
            invoice_number=data["invoice_number"],
            invoice_name=data["invoice_name"],
            issue_date=_as_date(data.get("issue_date")),
            project_ref=data.get("project_ref"),
            customer_ref=data.get("customer_ref"),
            description=data.get("description"),
            currency=data.get("currency", "DZD"),
            total_amount=float(data.get("total_amount") or 0.0),
            vat_rate=float(data.get("vat_rate") or 0.19),
            status="draft",
            documents=data.get("documents") or [],
        )
        sess.add(rec)
        sess.commit()
        return _record_to_dict(rec)


def list_invoices() -> list[dict[str, Any]]:
    with session_scope() as sess:
        recs = sess.query(InvoiceRecord).order_by(InvoiceRecord.id).all()
        return [_record_to_dict(r) for r in recs]


def get_invoice(inv_id: str) -> dict[str, Any] | None:
    with session_scope() as sess:
        rec = sess.query(InvoiceRecord).filter(InvoiceRecord.id == inv_id).first()
        return _record_to_dict(rec) if rec else None


def update_invoice(
    inv_id: str,
    updates: dict[str, Any],
) -> dict[str, Any] | None:
    """تحديث حقول الفاتورة أو إضافة/استبدال وثائقها."""
    allowed = {
        "invoice_name",
        "issue_date",
        "customer_ref",
        "description",
        "total_amount",
        "vat_rate",
        "status",
        "documents",
    }
    with session_scope() as sess:
        rec = sess.query(InvoiceRecord).filter(InvoiceRecord.id == inv_id).first()
        if rec is None:
            return None
        for k, v in updates.items():
            if k in allowed:
                if k in ("total_amount", "vat_rate"):
                    setattr(rec, k, float(v))
                elif k == "issue_date":
                    setattr(rec, k, _as_date(v))
                else:
                    setattr(rec, k, v)
        sess.commit()
        return _record_to_dict(rec)


def delete_invoice(inv_id: str) -> bool:
    with session_scope() as sess:
        rec = sess.query(InvoiceRecord).filter(InvoiceRecord.id == inv_id).first()
        if rec is None:
            return False
        sess.delete(rec)
        sess.commit()
        return True
