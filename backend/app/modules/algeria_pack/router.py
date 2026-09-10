"""Algérie BTPH regional pack API routes.

Endpoints
---------
GET  /config                — Full DZ PACK_CONFIG
GET  /wilayas               — 58 wilayas
GET  /wilayas/{code}        — Single wilaya by code (01-58)
GET  /lots                  — 8 Lots BTPH
GET  /fiscal                — Fiscal summary LF2026 (TVA/IBS/TAP/Retenue/…)
GET  /etb-categories        — ETB Cat. 1-9
POST /calc/tva              — TVA calc (body: {montant_ht, tva_type})
POST /calc/retenue          — Retenue de garantie calc
POST /calc/cacobatph        — CACOBATPH calc
POST /calc/ttc              — TTC calc (HT + TVA)
"""

from __future__ import annotations

import logging
from decimal import Decimal, InvalidOperation

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.core.dz_lf2026 import (
    calc_cacobatph,
    calc_retenue_garantie,
    calc_tva,
    calc_ttc,
    get_ibs_rate,
    get_tva_rate,
)
from app.dependencies import get_current_user_id
from app.modules.algeria_pack.config import (
    ETB_CATEGORIES,
    LOTS_BTPH,
    PACK_CONFIG,
    WILAYAS,
)

router = APIRouter(dependencies=[Depends(get_current_user_id)])
logger = logging.getLogger(__name__)


# ── Schemas ─────────────────────────────────────────────────────────────────


class CalcRequest(BaseModel):
    montant: Decimal = Field(..., description="Montant (HT or masse salariale) en DA")
    tva_type: str | None = Field(None, description="normal | reduit | exonere (only for TVA)")


class CalcResponse(BaseModel):
    montant_input: str
    taux: str
    taux_pct: str
    resultat: str
    detail: str


# ── Endpoints ────────────────────────────────────────────────────────────────


@router.get("/config/")
async def get_config() -> dict:
    """Return the full Algérie BTPH Pack configuration (PACK_CONFIG)."""
    return PACK_CONFIG


@router.get("/wilayas/")
async def list_wilayas() -> dict:
    """List all 58 wilayas."""
    return {"count": len(WILAYAS), "wilayas": WILAYAS}


@router.get("/wilayas/{code}/")
async def get_wilaya(code: str) -> dict:
    """Return a single wilaya by its 2-digit code (01-58)."""
    padded = code.zfill(2)
    for w in WILAYAS:
        if w["code"] == padded:
            return w
    raise HTTPException(status_code=404, detail=f"Wilaya {code!r} introuvable (01-58)")


@router.get("/lots/")
async def list_lots() -> dict:
    """List the 8 Lots BTPH."""
    return {"count": len(LOTS_BTPH), "lots": LOTS_BTPH}


@router.get("/fiscal/")
async def get_fiscal() -> dict:
    """Fiscal summary LF2026 (subset of PACK_CONFIG['fiscal'])."""
    return PACK_CONFIG["fiscal"]


@router.get("/etb-categories/")
async def list_etb_categories() -> dict:
    """ETB qualification categories (Cat. 1-9)."""
    return {"count": len(ETB_CATEGORIES), "categories": ETB_CATEGORIES}


# ── Calc helpers ─────────────────────────────────────────────────────────────


def _parse_decimal(value: Decimal | str) -> Decimal:
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise HTTPException(status_code=422, detail=f"Montant invalide: {value!r}") from exc


@router.post("/calc/tva/")
async def calc_tva_endpoint(body: CalcRequest) -> CalcResponse:
    """Calcule la TVA pour un montant HT donné.

    Body: ``{"montant": 1000000, "tva_type": "normal"}``
    ``tva_type``: ``normal`` (19%), ``reduit`` (9%), ``exonere`` (0%).
    """
    tva_type = (body.tva_type or "normal").strip() or "normal"
    rate = get_tva_rate(tva_type)
    ht = _parse_decimal(body.montant)
    tva = calc_tva(ht, rate)
    return CalcResponse(
        montant_input=str(ht),
        taux=str(rate),
        taux_pct=f"{(rate * 100):.0f}%",
        resultat=str(tva),
        detail=f"TVA {tva_type} sur {ht} DA = {tva} DA (taux {rate})",
    )


@router.post("/calc/ttc/")
async def calc_ttc_endpoint(body: CalcRequest) -> CalcResponse:
    """Calcule le TTC (HT + TVA).

    Body: ``{"montant": 1000000, "tva_type": "normal"}``
    """
    tva_type = (body.tva_type or "normal").strip() or "normal"
    rate = get_tva_rate(tva_type)
    ht = _parse_decimal(body.montant)
    ttc = calc_ttc(ht, rate)
    return CalcResponse(
        montant_input=str(ht),
        taux=str(rate),
        taux_pct=f"{(rate * 100):.0f}%",
        resultat=str(ttc),
        detail=f"TTC = {ht} + TVA({rate}) = {ttc} DA",
    )


@router.post("/calc/retenue/")
async def calc_retenue_endpoint(body: CalcRequest) -> CalcResponse:
    """Calcule la Retenue de garantie (5%) sur un montant HT.

    Body: ``{"montant": 1000000}``
    """
    from app.core.dz_lf2026 import RETENUE_GARANTIE_PCT

    ht = _parse_decimal(body.montant)
    retenue = calc_retenue_garantie(ht)
    return CalcResponse(
        montant_input=str(ht),
        taux=str(RETENUE_GARANTIE_PCT),
        taux_pct="5%",
        resultat=str(retenue),
        detail=f"Retenue de garantie 5% sur {ht} DA = {retenue} DA",
    )


@router.post("/calc/cacobatph/")
async def calc_cacobatph_endpoint(body: CalcRequest) -> CalcResponse:
    """Calcule la CACOBATPH (12,21%) sur une masse salariale.

    Body: ``{"montant": 500000}``  (masse salariale en DA)
    """
    from app.core.dz_lf2026 import CACOBATPH_RATE

    masse = _parse_decimal(body.montant)
    cot = calc_cacobatph(masse)
    return CalcResponse(
        montant_input=str(masse),
        taux=str(CACOBATPH_RATE),
        taux_pct="12,21%",
        resultat=str(cot),
        detail=f"CACOBATPH 12,21% sur {masse} DA = {cot} DA",
    )


@router.post("/calc/ibs/")
async def calc_ibs_endpoint(body: CalcRequest) -> CalcResponse:
    """Calcule l'IBS pour une activité donnée.

    Body: ``{"montant": 1000000, "tva_type": "btp"}``  (tva_type is reused as ``activite``).

    ``activite``: ``btp`` (19%), ``service`` (23%), ``commerce`` (26%).
    """
    activite = (body.tva_type or "btp").strip() or "btp"
    rate = get_ibs_rate(activite)
    base = _parse_decimal(body.montant)
    ibs = (base * rate).quantize(Decimal("0.01"))
    return CalcResponse(
        montant_input=str(base),
        taux=str(rate),
        taux_pct=f"{(rate * 100):.0f}%",
        resultat=str(ibs),
        detail=f"IBS {activite} ({rate}) sur {base} DA = {ibs} DA",
    )
