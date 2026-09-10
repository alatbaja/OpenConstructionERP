"""الواجهة البرمجية (FastAPI) لمشروع الجزائر BTPH.

نقاط النهاية:
- GET    /api/invoices                       — قائمة الفواتير
- POST   /api/invoices                       — إنشاء فاتورة
- GET    /api/invoices/{inv_id}              — تفاصيل فاتورة
- DELETE /api/invoices/{inv_id}              — حذف فاتورة
- POST   /api/invoices/{inv_id}/documents    — رفع ملف (PNG/PDF/توقيع) داخل حقل الفاتورة
- GET    /api/documents/{inv_id}/{filename}  — تنزيل/عرض ملف مرفوع
- GET    /                                   — واجهة ويب عربية للتجربة

التخزين: الملفات على القرص، والمسار يُحفظ داخل حقل `documents` في سجل الفاتورة نفسه.
"""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, Field

from algeria_btph.backend import repository
from algeria_btph.backend.schemas.invoice import DocType
from algeria_btph.services.storage import ensure_invoice_dir

# <repo>/algeria_btph/backend/api.py → parents[2] = algeria-btph/
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
STORAGE_ROOT = Path(
    __import__("os").environ.get("BTPH_STORAGE_ROOT", _PROJECT_ROOT / "storage")
)

MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10 MB

app = FastAPI(
    title="Algeria BTPH — Invoice API",
    description="فواتير BTPH مع رفع الوثائق داخل حقل الفاتورة",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class InvoiceIn(BaseModel):
    """بيانات إنشاء فاتورة جديدة."""

    invoice_number: str = Field(..., min_length=1, max_length=64)
    invoice_name: str = Field(..., min_length=1)
    issue_date: str | None = Field(default=None, description="YYYY-MM-DD")
    project_ref: str | None = None
    customer_ref: str | None = None
    description: str | None = None
    currency: str = "DZD"
    total_amount: float = 0.0
    vat_rate: float = Field(default=0.19, ge=0.0, le=1.0)


def _doc_dir(invoice_number: str) -> Path:
    return ensure_invoice_dir(STORAGE_ROOT / "invoices" / invoice_number)


def _safe_filename(name: str) -> str:
    """تنظيف اسم الملف ومنع اجتياز المسار."""
    safe = Path(name).name.replace("\\", "_").replace("/", "_").strip()
    return safe or "file"


# ── فواتير ────────────────────────────────────────────────────────────


@app.get("/api/invoices")
def list_invoices() -> list[dict]:
    return repository.list_invoices()


@app.post("/api/invoices", status_code=201)
def create_invoice(payload: InvoiceIn) -> dict:
    return repository.create_invoice(payload.model_dump())


@app.get("/api/invoices/{inv_id}")
def get_invoice(inv_id: str) -> dict:
    inv = repository.get_invoice(inv_id)
    if inv is None:
        raise HTTPException(status_code=404, detail="الفاتورة غير موجودة")
    return inv


@app.delete("/api/invoices/{inv_id}", status_code=204)
def delete_invoice(inv_id: str) -> None:
    if not repository.delete_invoice(inv_id):
        raise HTTPException(status_code=404, detail="الفاتورة غير موجودة")


# ── رفع الوثائق داخل حقل الفاتورة ────────────────────────────────────


@app.post("/api/invoices/{inv_id}/documents")
async def upload_document(
    inv_id: str,
    file: UploadFile,
    doc_type: Annotated[DocType, Form()] = DocType.AUTRE,
) -> dict:
    inv = repository.get_invoice(inv_id)
    if inv is None:
        raise HTTPException(status_code=404, detail="الفاتورة غير موجودة")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="الملف فارغ")
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="حجم الملف يتجاوز 10 MB")

    safe_name = _safe_filename(file.filename or "file")
    stored_name = f"{uuid.uuid4().hex[:8]}_{safe_name}"
    dest = _doc_dir(inv["invoice_number"]) / stored_name
    dest.write_bytes(content)

    doc = {
        "doc_type": doc_type.value if isinstance(doc_type, DocType) else str(doc_type),
        "file_path": str(dest),
        "original_name": safe_name,
        "mime_type": file.content_type or "application/octet-stream",
        "size": len(content),
    }

    documents = list(inv.get("documents") or [])
    documents.append(doc)
    updated = repository.update_invoice(inv_id, {"documents": documents})
    return updated or inv


@app.get("/api/documents/{inv_id}/{filename}")
def download_document(inv_id: str, filename: str) -> FileResponse:
    """تنزيل ملف مرفوع — فقط من ضمن وثائق الفاتورة المسجلة (حماية من اجتياز المسار)."""
    inv = repository.get_invoice(inv_id)
    if inv is None:
        raise HTTPException(status_code=404, detail="الفاتورة غير موجودة")

    wanted = _safe_filename(filename)
    for doc in inv.get("documents") or []:
        stored = Path(doc.get("file_path", ""))
        if stored.name == wanted or doc.get("original_name") == wanted:
            if stored.is_file() and STORAGE_ROOT in stored.resolve().parents:
                return FileResponse(
                    stored,
                    media_type=doc.get("mime_type", "application/octet-stream"),
                    filename=doc.get("original_name", stored.name),
                )
            raise HTTPException(status_code=410, detail="الملف مفقود من التخزين")
    raise HTTPException(status_code=404, detail="الوثيقة غير مسجلة في الفاتورة")


# ── واجهة ويب عربية بسيطة ────────────────────────────────────────────

_PAGE = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>فواتير BTPH — الجزائر</title>
<style>
  :root { --green:#0f7b3e; --ink:#1c2b23; --line:#dfe7e2; }
  * { box-sizing:border-box; font-family:"Segoe UI",Tahoma,sans-serif; }
  body { margin:0; background:#f4f7f5; color:var(--ink); }
  header { background:var(--green); color:#fff; padding:18px 24px; }
  header h1 { margin:0; font-size:1.3rem; }
  header p { margin:4px 0 0; opacity:.85; font-size:.85rem; }
  main { max-width:960px; margin:24px auto; padding:0 16px; }
  section { background:#fff; border:1px solid var(--line); border-radius:12px;
            padding:20px; margin-bottom:20px; }
  h2 { margin:0 0 14px; font-size:1.05rem; color:var(--green); }
  label { display:block; font-size:.8rem; margin:10px 0 4px; }
  input, select { width:100%; padding:9px 10px; border:1px solid var(--line);
                  border-radius:8px; font-size:.9rem; }
  .row { display:flex; gap:12px; } .row > div { flex:1; }
  button { margin-top:14px; background:var(--green); color:#fff; border:0;
           padding:10px 22px; border-radius:8px; font-size:.95rem; cursor:pointer; }
  button:hover { filter:brightness(1.1); }
  table { width:100%; border-collapse:collapse; font-size:.85rem; }
  th, td { padding:8px 10px; border-bottom:1px solid var(--line); text-align:right; }
  th { background:#eef4f0; }
  .badge { background:#eef4f0; border-radius:999px; padding:2px 10px; font-size:.75rem; }
  .docs a { display:inline-block; margin:2px 4px; color:var(--green);
            text-decoration:none; border:1px solid var(--line); border-radius:6px;
            padding:2px 8px; font-size:.75rem; }
  .del { background:none; border:0; color:#b3261e; cursor:pointer; padding:0 6px; }
  .empty { color:#7a8a80; text-align:center; padding:14px; }
</style>
</head>
<body>
<header>
  <h1>🇩🇿 فواتير BTPH — Décompte / Situation</h1>
  <p>الملفات المرفوعة (توقيع / موافقة / سجل تدقيق) تُخزَّن داخل حقل الفاتورة نفسه</p>
</header>
<main>
  <section>
    <h2>➕ فاتورة جديدة</h2>
    <form id="f">
      <div class="row">
        <div><label>رقم الفاتورة</label><input id="num" required placeholder="BT-2026-001"></div>
        <div><label>اسم الفاتورة</label><input id="name" required placeholder="Devis Gros Œuvre Lot 01"></div>
      </div>
      <div class="row">
        <div><label>تاريخ الإصدار</label><input id="date" type="date"></div>
        <div><label>مرجع المشروع</label><input id="proj" placeholder="CH-Anna1"></div>
        <div><label>المبلغ (DA)</label><input id="amt" type="number" min="0" step="0.01" value="0"></div>
      </div>
      <button>إنشاء الفاتورة</button>
    </form>
  </section>

  <section>
    <h2>📄 الفواتير</h2>
    <table id="tbl">
      <thead><tr>
        <th>الرقم</th><th>الاسم</th><th>التاريخ</th><th>المبلغ</th><th>الوثائق</th><th></th>
      </tr></thead>
      <tbody></tbody>
    </table>
    <div class="empty" id="empty">لا توجد فواتير بعد</div>
  </section>
</main>
<script>
const $ = (id) => document.getElementById(id);
const DT = {signature:"توقيع", approval:"موافقة", audit_record:"سجل تدقيق", pdf_bilan:"PDF", autre:"أخرى"};

async function refresh(){
  const r = await fetch('/api/invoices'); const list = await r.json();
  const tb = $('tbl').tBodies[0]; tb.innerHTML = '';
  $('empty').style.display = list.length ? 'none' : 'block';
  for (const inv of list){
    const tr = tb.insertRow();
    tr.innerHTML = `
      <td><b>${inv.invoice_number}</b></td>
      <td>${inv.invoice_name}</td>
      <td>${inv.issue_date}</td>
      <td>${Number(inv.total_amount).toLocaleString('fr-DZ')} ${inv.currency}</td>
      <td class="docs">
        ${(inv.documents||[]).map(d =>
          `<a href="/api/documents/${inv.id}/${encodeURIComponent(d.original_name)}" target="_blank">
             ${DT[d.doc_type]||d.doc_type}</a>`).join('') || '<span class="empty">—</span>'}
        <br>
        <input type="file" style="display:none" onchange="up(this,'${inv.id}')">
        <select onchange="upSel(this,'${inv.id}')" style="width:auto;font-size:.7rem;margin-top:4px">
          <option value="">+ رفع ملف…</option>
          ${Object.entries(DT).map(([k,v])=>`<option value="${k}">${v}</option>`).join('')}
        </select>
      </td>
      <td><button class="del" onclick="del('${inv.id}')">✕</button></td>`;
    tr.querySelector('input[type=file]')._sel = tr.querySelector('select');
  }
}
async function create(e){
  e.preventDefault();
  const body = {
    invoice_number: $('num').value, invoice_name: $('name').value,
    issue_date: $('date').value || null, project_ref: $('proj').value || null,
    total_amount: parseFloat($('amt').value||'0'), currency: 'DZD', vat_rate: 0.19
  };
  await fetch('/api/invoices', {method:'POST',
    headers:{'Content-Type':'application/json'}, body: JSON.stringify(body)});
  $('f').reset(); refresh();
}
async function up(input, invId){
  const sel = input._sel; const dt = sel.value || 'autre';
  const fd = new FormData();
  fd.append('file', input.files[0]); fd.append('doc_type', dt);
  await fetch(`/api/invoices/${invId}/documents`, {method:'POST', body: fd});
  sel.value = ''; refresh();
}
function upSel(sel, invId){
  if (!sel.value) return;
  const input = sel.closest('td').querySelector('input[type=file]');
  input._expect = sel.value; input.click();
  input.onchange = () => up(input, invId);
}
async function del(id){
  if (!confirm('حذف الفاتورة؟')) return;
  await fetch('/api/invoices/'+id, {method:'DELETE'}); refresh();
}
$('f').addEventListener('submit', create);
refresh();
</script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    return HTMLResponse(_PAGE)
