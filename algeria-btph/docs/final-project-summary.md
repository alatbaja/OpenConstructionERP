# ملخص المشروع النهائي — الجزائر BTPH

الحالة: **تطبيق يعمل** — API + قاعدة بيانات + واجهة عربية + رفع ملفات داخل حقل الفاتورة.

## المكونات

| المكوّن | الملف | الحالة |
|---|---|---|
| نماذج الفاتورة (Pydantic) | `algeria_btph/backend/schemas/invoice.py` | ✅ |
| قاعدة بيانات SQLite (SQLAlchemy 2.0) | `algeria_btph/backend/db.py` | ✅ |
| CRUD + تحديث الوثائق | `algeria_btph/backend/repository.py` | ✅ |
| FastAPI (فواتير + رفع multipart + تنزيل) | `algeria_btph/backend/api.py` | ✅ |
| واجهة ويب عربية RTL | نفس الملف (`GET /`) | ✅ |
| تخزين الملفات على القرص | `algeria_btph/services/storage.py` | ✅ |
| نقطة تشغيل واحدة | `algeria_btph/__main__.py` → `python -m algeria_btph` | ✅ |

## سير التحقق النهائي (نفّذ فعلياً)

1. `POST /api/invoices` → إنشاء `INV-0001` / `BT-2026-TEST` ✅
2. `POST /api/invoices/INV-0001/documents` (PNG كتوقيع) → HTTP 200 ✅
3. `GET /api/invoices/INV-0001` → `documents: [(signature, sig.png, image/png)]` ✅
4. `GET /api/documents/INV-0001/sig.png` → تنزيل مطابق بايت-ببايت (`cmp` ✅)
5. `GET /` → الواجهة العربية تُخدَم ✅

## قرارات التصميم

- **الملفات داخل حقل الفاتورة**: المسار يُخزَّن في `documents` (JSON) ضمن سجل الفاتورة — لا جداول منفصلة.
- **القرص لا الـ BLOB**: أسهل نسخاً احتياطياً ومعاينة؛ جاهز للترقية إلى S3/MinIO.
- **حماية التنزيل**: فقط الملفات المسجلة في الفاتورة + منع اجتياز المسار.
- **واجهة بلا بناء**: HTML/JS واحد مضمّن — صفر تبعيات واجهة.

## الخطوات القادمة

1. Décompte / Situation (حالات الأعمال)
2. أسعار CNTC-BTPH + BPU/DQE
3. حسابات LF2026 (TVA 19/9، CACOBATPH)
4. مصادقة وأدوار
