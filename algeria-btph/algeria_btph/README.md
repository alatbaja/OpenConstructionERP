# مشروع الجزائر BTPH

ERP مفتوح المصدر لتكييف نظام التشييد والمقاولات للسوق الجزائري (BTPH).
يغطي: BPU/DQE، Décompte/Situation، الفواتير، المعايير الجزائرية (LF2026).

## الاستخدام السريع
```python
from algeria_btph import InvoiceCreate, InvoiceDocumentFile, DocType

inv = InvoiceCreate(
    invoice_number="BT-2026-001",
    invoice_name="Devis Gros Œuvre Lot 01",
    issue_date="2026-09-09",
    project_ref="CH-Anna1",
    documents=[
        InvoiceDocumentFile(
            doc_type=DocType.SIGNATURE,
            file_path="/storage/invoices/BT-2026-001/signature.png",
            original_name="signature.png",
            mime_type="image/png",
        )
    ],
)
```

## الملفات
- `backend/` — نماذج Pydantic وخدمات التعامل مع الفواتير والملفات
- `docs/` — توثيق النموذج والتخزين
