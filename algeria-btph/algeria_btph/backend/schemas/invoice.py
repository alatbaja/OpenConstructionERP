from __future__ import annotations

from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class DocType(str, Enum):
    """نوع الوثيقة المرفوعة داخل الفاتورة (BTPH)."""

    SIGNATURE = "signature"            # صورة توقيع
    APPROVAL = "approval"              # صورة موافقة
    AUDIT_RECORD = "audit_record"      # سجل تدقيق
    PDF_BILAN = "pdf_bilan"            # PDF billage / استخراج
    AUTRE = "autre"                    # نوع آخر


class InvoiceDocumentFile(BaseModel):
    """ملف/وثيقة مرفوعة داخل حقل الفاتورة."""

    model_config = ConfigDict(populate_by_name=True)

    doc_type: DocType = Field(
        ...,
        description="تصنيف الوثيقة داخل الفاتورة (توقيع/موافقة/تدقيق/إلّا)",
    )
    file_path: str = Field(
        ...,
        alias="file_path",
        description="مسار الملف المخزن (تخزين محلي أو مسار storage)",
    )
    original_name: str = Field(
        ...,
        description="اسم الملف الأصلي عند الرفع",
    )
    mime_type: str = Field(
        default="application/octet-stream",
        description="نوع MIME المرفق (PDF/PNG/JPG...)",
    )
    uploaded_at: date = Field(
        default_factory=date.today,
        description="تاريخ رفع الملف",
    )

    @property
    def is_image(self) -> bool:
        return self.mime_type.startswith("image/")

    @property
    def is_pdf(self) -> bool:
        return self.mime_type == "application/pdf"


class InvoiceBase(BaseModel):
    """حقول مشتركة للفاتورة/الإيصال (BTPH)."""

    model_config = ConfigDict(populate_by_name=True)

    invoice_number: str = Field(
        ...,
        min_length=1,
        description="رقم الفاتورة / الرمز الداخلي",
    )
    invoice_name: str = Field(
        ...,
        description="اسم الفاتورة أو عنوانه الرسمي",
    )
    issue_date: date = Field(
        ...,
        description="تاريخ إصدار الفاتورة",
    )
    customer_ref: str | None = Field(
        default=None,
        description="مرجع العميل/المقاول (BPU/DQE/chantier)",
    )
    currency: str = Field(
        default="DZD",
        description="عملة الفاتورة (DZD افتراضيًا)",
    )
    total_amount: Decimal = Field(
        default=Decimal("0.00"),
        description="المبلغ الإجمالي",
    )
    vat_rate: float = Field(
        default=0.19,
        ge=0.0,
        le=1.0,
        description="نسبة الضريبة (TVA BTP）：19% أو 9% أو إلّا",
    )

    # حقل الملفات المرفوعة داخل الفاتورة
    documents: list[InvoiceDocumentFile] = Field(
        default_factory=list,
        description="قائمة الملفات/الصور/سجلات التدقيق المرفوعة داخل الفاتورة",
    )


class InvoiceCreate(InvoiceBase):
    """إنشاء فاتورة جديدة."""

    project_ref: str = Field(
        ...,
        description="مرجع المشروع / عمارة / موقع BTPH",
    )
    description: str | None = Field(
        default=None,
        description="ملاحظة إضافية",
    )


class InvoiceUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    invoice_name: str | None = None
    issue_date: date | None = None
    customer_ref: str | None = None
    total_amount: Decimal | None = None
    vat_rate: float | None = None
    description: str | None = None

    documents: list[InvoiceDocumentFile] | None = None


class InvoicePublic(InvoiceBase):
    """نموذج الفاتورة للعرض الخارجي من العميل/العميل العام."""

    id: str
    status: str = "draft"
    created_at: date = Field(default_factory=date.today)

    class Config:
        pass
