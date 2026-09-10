# مشروع الجزائر BTPH - ERP الجزائري للتشييد والمقاولات

نظام لتكييف عمليات التشييد والمقاولات للسوق الجزائري (BTPH): فواتير Décompte/Situation
مع **رفع الملفات (توقيع PNG / موافقة PDF / سجل تدقيق) داخل حقل الفاتورة نفسه**.

## 🏗️ الهيكل

```text
algeria-btph/
├── Makefile · docker-compose.yml · .gitignore
├── pyproject.toml            # pydantic + fastapi + uvicorn + sqlalchemy
├── requirements.txt
├── algeria_btph/             # الحزمة الأساسية
│   ├── __main__.py           # نقطة التشغيل الوحيدة → python -m algeria_btph
│   ├── main.py               # مشغّل uvicorn
│   ├── backend/
│   │   ├── api.py            # FastAPI: فواتير + رفع وثائق + واجهة عربية
│   │   ├── db.py             # SQLite (SQLAlchemy 2.0)
│   │   ├── repository.py     # CRUD
│   │   └── schemas/invoice.py # نماذج Pydantic
│   ├── services/storage.py   # مسارات تخزين الملفات
│   └── README.md
└── docs/                     # توثيق النماذج والتخزين
```

## 🚀 التشغيل

```bash
cd algeria-btph

# أول مرة: بيئة + تبعيات
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python -r requirements.txt

# تشغيل الخادم (0.0.0.0:8000)
make run          # أو: .venv/bin/python -m algeria_btph
```

ثم افتح `http://localhost:8000` — واجهة عربية RTL جاهزة للتجربة.

متغيرات البيئة (اختيارية): `BTPH_HOST`, `BTPH_PORT`, `BTPH_DB_PATH`, `BTPH_STORAGE_ROOT`.

## 🔌 نقاط النهاية

| الطريقة | المسار | الوظيفة |
|---|---|---|
| GET | `/` | واجهة ويب عربية |
| GET | `/api/invoices` | قائمة الفواتير |
| POST | `/api/invoices` | إنشاء فاتورة |
| GET | `/api/invoices/{id}` | تفاصيل فاتورة |
| DELETE | `/api/invoices/{id}` | حذف فاتورة |
| POST | `/api/invoices/{id}/documents` | **رفع ملف داخل حقل الفاتورة** (`multipart`: file + doc_type) |
| GET | `/api/documents/{id}/{filename}` | تنزيل/عرض ملف مرفوع |

مثال رفع توقيع:

```bash
curl -X POST http://localhost:8000/api/invoices/INV-0001/documents \
     -F "file=@signature.png;type=image/png" \
     -F "doc_type=signature"
```

## 📦 نموذج الوثيقة داخل الفاتورة

| الحقل | الوصف |
|---|---|
| `doc_type` | signature / approval / audit_record / pdf_bilan / autre |
| `file_path` | مسار الملف المخزن على القرص |
| `original_name` | اسم الملف الأصلي |
| `mime_type` | نوع MIME (PDF/PNG/JPG...) |
| `size` | الحجم بالبايت |

- الملفات تُحفظ في `storage/invoices/<رقم_الفاتورة>/` (قابلة للتغيير عبر `BTPH_STORAGE_ROOT`)
- المسار يُسجَّل **داخل حقل `documents` في سجل الفاتورة نفسه** (JSON في SQLite)
- التنزيل محمي: فقط الملفات المسجلة ضمن الفاتورة، مع منع اجتياز المسار
- حد الحجم: 10 MB

## ✅ ما تم التحقق منه عملياً

إنشاء فاتورة → رفع PNG كتوقيع → ظهوره في حقل `documents` → تنزيله مطابقاً بايت-ببايت → الواجهة تُخدَم بنجاح.

## 🔄 الخطوات القادمة

1. Décompte / Situation (حالات أعمال المقاولات)
2. قاعدة أسعار CNTC-BTPH + قالب BPU/DQE
3. ربط LF2026 (TVA 19/9، CACOBATPH 12.21%) بالحسابات
4. مصادقة + أدوار للمستخدمين
