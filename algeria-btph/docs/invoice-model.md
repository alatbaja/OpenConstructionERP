# نموذج الفاتورة - الجزائر BTPH

## الحقول الأساسية
- `invoice_number`: رقم الفاتورة / الرمز الداخلي
- `invoice_name`: اسم الفاتورة أو العنوان الرسمي
- `issue_date`: تاريخ الإصدار
- `project_ref`: مرجع المشروع/العمارة/الموقع BTPH
- `customer_ref`: مرجع العميل/المقاول (BPU/DQE/chantier)
- `currency`: عملة الفاتورة (DZD افتراضيًا)
- `total_amount`: المبلغ الإجمالي
- `vat_rate`: نسبة الضريبة (TVA BTP): 19% أو 9% أو إلّا

## حقل الملفات المرفوعة (documents)
قائمة `InvoiceDocumentFile` داخل الفاتورة:
- `doc_type`: نوع الوثيقة (signature / approval / audit_record / pdf_bilan / autre)
- `file_path`: مسار الملف المخزن
- `original_name`: اسم الملف الأصلي عند الرفع
- `mime_type`: نوع MIME المرفق
- `uploaded_at`: تاريخ رفع الملف

### التصميم الحالي
- الملفات تُخزن كمسارات داخل قاعدة البيانات أو النظام الملفاتي
- لا تُخزن كـ binary داخل النموذج، بل كـ مسار أو رابط
- يمكن للنظام لاحقًا إضافة رفع الملفات وتخزينها في storage

## مثال استخدام
```python
from algeria_btph.backend import InvoiceCreate, InvoiceDocumentFile, DocType

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
