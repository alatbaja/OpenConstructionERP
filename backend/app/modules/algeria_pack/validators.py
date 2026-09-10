"""Algérie BTPH — validation rules (LF2026).

Registered automatically via ``app.core.module_loader`` which imports
``app.modules.algeria_pack.validators`` on startup.

Rule set: ``dz_btph`` — activated when BOQ / Project has country DZ
or when caller explicitly requests ``rule_sets=["dz_btph"]``.

Rules
-----
* dz_btph.tva_rate            — TVA must be 19% (normal) or 9% (réduit, LF2026 4 cases)
* dz_btph.retenue_garantie    — Retenue de garantie must be 5% if present
* dz_btph.tap_supprimee       — TAP must not appear (supprimée LF2024→2026)
* dz_btph.lot_btph            — Every position must belong to one of the 8 Lots BTPH
* dz_btph.cacobatph           — CACOBATPH reminder (info) when masse salariale context present
* dz_btph.bpu_structure       — BPU/DQE: ordinal must follow Lot-prefixed scheme + currency DZD

All user-facing messages go through ``app.core.validation.messages.translate``
so FR / AR can override them without code changes.
"""

from __future__ import annotations

import logging
import re
from decimal import Decimal, InvalidOperation
from typing import Any

from app.core.dz_lf2026 import (
    CACOBATPH_RATE,
    RETENUE_GARANTIE_PCT,
    TAP_RATE,
    TVA_NORMAL,
    TVA_REDUIT,
)
from app.core.validation.engine import (
    RuleCategory,
    RuleResult,
    Severity,
    ValidationContext,
    ValidationRule,
    rule_registry,
)
from app.core.validation.messages import DEFAULT_LOCALE, translate

from app.modules.algeria_pack.config import LOTS_BTPH

logger = logging.getLogger(__name__)


# ── Helpers ───────────────────────────────────────────────────────────────────


def _get_positions(context: ValidationContext) -> list[dict[str, Any]]:
    data = context.data
    if isinstance(data, dict):
        return data.get("positions", [])
    if isinstance(data, list):
        return data
    return []


def _get_locale(context: ValidationContext) -> str:
    meta = getattr(context, "metadata", None) or {}
    locale = meta.get("locale") if isinstance(meta, dict) else None
    if isinstance(locale, str) and locale:
        return locale
    return DEFAULT_LOCALE


def _ok(locale: str) -> str:
    return translate("common.ok", locale=locale)


# Valid Lot codes — 01..08
_VALID_LOT_CODES: set[str] = {lot["code"] for lot in LOTS_BTPH}
_VALID_LOT_CODES_STR = ", ".join(sorted(_VALID_LOT_CODES))

# Ordinal pattern for DZ BPU/DQE: Lot prefix optional but recommended
# e.g. "01.01", "01.02.003", "02-01", "Lot 03 / 01.05"
_BPU_ORDINAL_RE = re.compile(r"^(0[1-8]|[1-8])(\.[0-9]{1,4}){1,3}$")

# Allowed TVA rates (Decimal exact)
_ALLOWED_TVA = {TVA_NORMAL, TVA_REDUIT, Decimal("0")}  # 0 = exonéré
_ALLOWED_TVA_DISPLAY = "19% / 9% / 0% (exonéré)"


# ── Rules ─────────────────────────────────────────────────────────────────────


class DZTvaRate(ValidationRule):
    """TVA must be 19% normal, 9% réduit (LF2026), or 0% exonéré."""

    rule_id = "dz_btph.tva_rate"
    name = "DZ TVA Rate (LF2026)"
    standard = "dz_btph"
    severity = Severity.ERROR
    category = RuleCategory.COMPLIANCE
    description = "TVA on every position / BOQ total must be 19% (normal), 9% (réduit LF2026) or 0% (exonéré). TAP is ignored."

    async def validate(self, context: ValidationContext) -> list[RuleResult]:
        locale = _get_locale(context)
        positions = _get_positions(context)
        # Also check BOQ-level metadata if present
        data = context.data if isinstance(context.data, dict) else {}
        boq_tva = data.get("tva_rate") or data.get("vat_rate") or data.get("metadata", {}).get("tva_rate") if isinstance(data.get("metadata"), dict) else None

        results: list[RuleResult] = []

        # BOQ-level check (single result)
        if boq_tva is not None:
            try:
                rate = Decimal(str(boq_tva))
                # Normalise 19 -> 0.19 etc. Accept both forms.
                if rate > Decimal("1"):
                    rate = rate / Decimal("100")
                passed = rate in _ALLOWED_TVA
                if passed:
                    results.append(RuleResult(rule_id=self.rule_id, rule_name=self.name, severity=self.severity, category=self.category, passed=True, message=_ok(locale)))
                else:
                    results.append(RuleResult(rule_id=self.rule_id, rule_name=self.name, severity=self.severity, category=self.category, passed=False, message=translate("dz_btph.tva_rate.fail", locale=locale, rate=str(rate), allowed=_ALLOWED_TVA_DISPLAY), details={"given_rate": str(rate), "allowed": _ALLOWED_TVA_DISPLAY}, suggestion=translate("dz_btph.tva_rate.suggestion", locale=locale)))
            except (InvalidOperation, ValueError, TypeError):
                pass  # malformed → skip, other validators will flag

        for pos in positions:
            raw = pos.get("tva_rate")
            if raw is None:
                raw = (pos.get("tax") or {}).get("tva") if isinstance(pos.get("tax"), dict) else None
            if raw is None:
                raw = pos.get("vat_rate")
            if raw is None:
                continue  # no TVA declared → not an error for this rule (coverage is separate)
            try:
                rate = Decimal(str(raw))
                if rate > Decimal("1"):
                    rate = rate / Decimal("100")
                passed = rate in _ALLOWED_TVA
                if passed:
                    results.append(RuleResult(rule_id=self.rule_id, rule_name=self.name, severity=self.severity, category=self.category, passed=True, message=_ok(locale), element_ref=pos.get("id")))
                else:
                    results.append(RuleResult(rule_id=self.rule_id, rule_name=self.name, severity=self.severity, category=self.category, passed=False, message=translate("dz_btph.tva_rate.fail_pos", locale=locale, ordinal=pos.get("ordinal", "?"), rate=str(rate), allowed=_ALLOWED_TVA_DISPLAY), element_ref=pos.get("id"), details={"given_rate": str(rate), "ordinal": pos.get("ordinal")}, suggestion=translate("dz_btph.tva_rate.suggestion", locale=locale)))
            except (InvalidOperation, ValueError, TypeError):
                continue

        # If nothing to check, emit a passing result so the rule set is not "skipped"
        if not results and not boq_tva:
            # Check if data even looks DZ — if region is DZ, we still want a passing signal
            region = (getattr(context, "region", None) or "").upper()
            std = (getattr(context, "standard", None) or "").lower()
            if region == "DZ" or std in ("dz_btph", "dz", "algeria"):
                results.append(RuleResult(rule_id=self.rule_id, rule_name=self.name, severity=self.severity, category=self.category, passed=True, message=_ok(locale), details={"note": "no TVA declared — assumed 19% default"}))
        return results


class DZRetunueGarantie(ValidationRule):
    """Retenue de garantie must be 5% (CCAG / 15-247)."""

    rule_id = "dz_btph.retenue_garantie"
    name = "DZ Retenue de Garantie 5%"
    standard = "dz_btph"
    severity = Severity.WARNING
    category = RuleCategory.COMPLIANCE
    description = "Retenue de garantie on situations / market totals must be 5% until réception définitive."

    async def validate(self, context: ValidationContext) -> list[RuleResult]:
        locale = _get_locale(context)
        data = context.data if isinstance(context.data, dict) else {}
        positions = _get_positions(context)

        results: list[RuleResult] = []
        # BOQ-level retenue
        raw = data.get("retenue_garantie") or data.get("retention_pct")
        if isinstance(data.get("metadata"), dict):
            raw = raw or data["metadata"].get("retenue_garantie") or data["metadata"].get("retenue_pct")
        # Also scan position-level if any
        candidates: list[tuple[Any, Any]] = []
        if raw is not None:
            candidates.append((raw, None))
        for pos in positions:
            pr = pos.get("retenue_garantie") or pos.get("retenue_pct") or pos.get("retention_pct")
            if pr is not None:
                candidates.append((pr, pos))

        for raw_val, pos in candidates:
            try:
                rate = Decimal(str(raw_val))
                if rate > Decimal("1"):
                    rate = rate / Decimal("100")
                passed = rate == RETENUE_GARANTIE_PCT
                if passed:
                    results.append(RuleResult(rule_id=self.rule_id, rule_name=self.name, severity=self.severity, category=self.category, passed=True, message=_ok(locale), element_ref=pos.get("id") if pos else None))
                else:
                    ordinal = pos.get("ordinal", "?") if pos else "BOQ"
                    results.append(RuleResult(rule_id=self.rule_id, rule_name=self.name, severity=self.severity, category=self.category, passed=False, message=translate("dz_btph.retenue_garantie.fail", locale=locale, ordinal=ordinal, rate=str(rate), expected="5%"), element_ref=pos.get("id") if pos else None, details={"given": str(rate), "expected": str(RETENUE_GARANTIE_PCT)}, suggestion=translate("dz_btph.retenue_garantie.suggestion", locale=locale)))
            except (InvalidOperation, ValueError, TypeError):
                continue

        # No explicit retenue found → INFO (not an error, just a reminder — many BOQs leave it to Finance module)
        if not results:
            # Only emit when DZ context is explicit
            region = (getattr(context, "region", None) or "").upper()
            if region == "DZ":
                results.append(RuleResult(rule_id=self.rule_id, rule_name=self.name, severity=Severity.INFO, category=self.category, passed=True, message=_ok(locale), details={"note": "Retenue de garantie non déclarée — 5% sera appliquée en Situation"}))
        return results


class DZTAPSupprimee(ValidationRule):
    """TAP must not appear — supprimée LF2024, confirmée LF2026."""

    rule_id = "dz_btph.tap_supprimee"
    name = "DZ TAP Supprimée (LF2026)"
    standard = "dz_btph"
    severity = Severity.ERROR
    category = RuleCategory.COMPLIANCE
    description = "TAP (Taxe sur l'Activité Professionnelle) est supprimée depuis LF2024 et confirmée LF2026 — elle ne doit plus figurer sur la G50 ni dans les markups."

    async def validate(self, context: ValidationContext) -> list[RuleResult]:
        locale = _get_locale(context)
        data = context.data if isinstance(context.data, dict) else {}
        positions = _get_positions(context)
        results: list[RuleResult] = []

        # Check BOQ-level markups / taxes
        def _has_tap(obj: dict[str, Any]) -> bool:
            for key in ("TAP", "tap", "tap_rate", "taxe_activite", "taxe_professionnelle"):
                if key in obj and obj[key] not in (None, "", 0, "0", Decimal("0"), "0%"):
                    try:
                        v = Decimal(str(obj[key]).replace("%", "").strip())
                        if v > Decimal("1"):
                            v = v / Decimal("100")
                        if v != TAP_RATE:
                            return True
                    except Exception:
                        return True  # any non-zero textual TAP is suspect
            # scan nested tax dicts
            tax = obj.get("tax") or obj.get("taxes") or obj.get("markup")
            if isinstance(tax, dict):
                return _has_tap(tax)
            if isinstance(tax, list):
                return any(isinstance(x, dict) and _has_tap(x) for x in tax)
            return False

        if isinstance(data, dict) and _has_tap(data):
            results.append(RuleResult(rule_id=self.rule_id, rule_name=self.name, severity=self.severity, category=self.category, passed=False, message=translate("dz_btph.tap_supprimee.fail", locale=locale, detail="BOQ"), details={"where": "BOQ"}, suggestion=translate("dz_btph.tap_supprimee.suggestion", locale=locale)))

        for pos in positions:
            if _has_tap(pos):
                results.append(RuleResult(rule_id=self.rule_id, rule_name=self.name, severity=self.severity, category=self.category, passed=False, message=translate("dz_btph.tap_supprimee.fail", locale=locale, detail=pos.get("ordinal", "?")), element_ref=pos.get("id"), details={"ordinal": pos.get("ordinal")}, suggestion=translate("dz_btph.tap_supprimee.suggestion", locale=locale)))

        if not results:
            results.append(RuleResult(rule_id=self.rule_id, rule_name=self.name, severity=self.severity, category=self.category, passed=True, message=_ok(locale)))
        return results


class DZLotBTPH(ValidationRule):
    """Every non-section position must carry a Lot BTPH 01-08."""

    rule_id = "dz_btph.lot_btph"
    name = "DZ Lot BTPH 01-08"
    standard = "dz_btph"
    severity = Severity.WARNING
    category = RuleCategory.STRUCTURE
    description = "Chaque position doit être rattachée à l'un des 8 Lots BTPH (01 Gros Œuvre ... 08 Aménagements extérieurs)."

    async def validate(self, context: ValidationContext) -> list[RuleResult]:
        locale = _get_locale(context)
        positions = _get_positions(context)
        results: list[RuleResult] = []
        for pos in positions:
            ptype = str(pos.get("type") or "").lower()
            if ptype == "section":
                continue
            lot = pos.get("lot")
            if lot is None:
                lot = (pos.get("classification") or {}).get("dz_lot") if isinstance(pos.get("classification"), dict) else None
            if lot is None:
                lot = pos.get("lot_code") or pos.get("dz_lot")
            if lot is None:
                # Try to infer from section parent — accept parent lot
                lot = pos.get("section")
            lot_str = str(lot).strip().zfill(2) if lot is not None and str(lot).strip() else ""
            # Allow "01 - Gros Oeuvre" form → extract leading 2 digits
            m = re.match(r"^\s*0?([1-8])\b", lot_str)
            if m:
                lot_str = m.group(1).zfill(2)
            passed = lot_str in _VALID_LOT_CODES
            if passed:
                results.append(RuleResult(rule_id=self.rule_id, rule_name=self.name, severity=self.severity, category=self.category, passed=True, message=_ok(locale), element_ref=pos.get("id")))
            else:
                results.append(RuleResult(rule_id=self.rule_id, rule_name=self.name, severity=self.severity, category=self.category, passed=False, message=translate("dz_btph.lot_btph.fail", locale=locale, ordinal=pos.get("ordinal", "?"), lot=lot_str or "—", valid=_VALID_LOT_CODES_STR), element_ref=pos.get("id"), details={"given_lot": lot_str, "valid": sorted(_VALID_LOT_CODES)}, suggestion=translate("dz_btph.lot_btph.suggestion", locale=locale)))
        if not positions:
            return []
        # Deduplicate passing flood — keep behaviour consistent with other rules: one per position
        return results


class DZBPUStructure(ValidationRule):
    """BPU/DQE structure: ordinal should be Lot-prefixed and currency DZD."""

    rule_id = "dz_btph.bpu_structure"
    name = "DZ BPU/DQE Structure"
    standard = "dz_btph"
    severity = Severity.WARNING
    category = RuleCategory.STRUCTURE
    description = "Le BPU/DQE algérien doit structurer les ordinals par Lot (01.xx, 02.xx) et utiliser la devise DZD."

    async def validate(self, context: ValidationContext) -> list[RuleResult]:
        locale = _get_locale(context)
        data = context.data if isinstance(context.data, dict) else {}
        positions = _get_positions(context)
        results: list[RuleResult] = []

        # Currency check (BOQ-level)
        ccy = (data.get("currency") or "").strip().upper() if isinstance(data.get("currency"), str) else ""
        if not ccy and isinstance(data.get("metadata"), dict):
            ccy = (data["metadata"].get("currency") or "").strip().upper()
        # Scan position currencies too
        position_ccys = {str(p.get("currency", "")).strip().upper() for p in positions if p.get("currency")}
        if ccy and ccy != "DZD":
            results.append(RuleResult(rule_id=self.rule_id, rule_name=self.name, severity=self.severity, category=self.category, passed=False, message=translate("dz_btph.bpu_structure.currency_fail", locale=locale, currency=ccy), details={"given_currency": ccy}, suggestion=translate("dz_btph.bpu_structure.currency_suggestion", locale=locale)))
        elif position_ccys and not position_ccys.issubset({"", "DZD"}):
            bad = ", ".join(sorted(c for c in position_ccys if c not in ("", "DZD")))
            results.append(RuleResult(rule_id=self.rule_id, rule_name=self.name, severity=self.severity, category=self.category, passed=False, message=translate("dz_btph.bpu_structure.currency_fail", locale=locale, currency=bad), details={"currencies": sorted(position_ccys)}, suggestion=translate("dz_btph.bpu_structure.currency_suggestion", locale=locale)))

        # Ordinal structure
        for pos in positions:
            ordinal = str(pos.get("ordinal") or "").strip()
            if not ordinal:
                continue
            # Accept Lot-prefixed or simple numeric — only warn if it starts with 01-08 but malformed
            if re.match(r"^[0-8]", ordinal):
                passed = bool(_BPU_ORDINAL_RE.match(ordinal)) or bool(re.match(r"^[1-8](\.[0-9]+)+$", ordinal))
                # Be permissive: any dotted numeric with Lot prefix 1-8 is valid
                if not passed and ordinal[0] in "12345678":
                    # Very loose fallback: must start with Lot digit
                    passed = bool(re.match(r"^[1-8]\b", ordinal))
                if not passed:
                    # Keep message consistent: warn to use Lot-prefixed scheme
                    results.append(RuleResult(rule_id=self.rule_id, rule_name=self.name, severity=self.severity, category=self.category, passed=False, message=translate("dz_btph.bpu_structure.ordinal_fail", locale=locale, ordinal=ordinal), element_ref=pos.get("id"), details={"ordinal": ordinal}, suggestion=translate("dz_btph.bpu_structure.ordinal_suggestion", locale=locale)))
                else:
                    results.append(RuleResult(rule_id=self.rule_id, rule_name=self.name, severity=self.severity, category=self.category, passed=True, message=_ok(locale), element_ref=pos.get("id")))
            else:
                # Non-Lot ordinal — also warn gently (DZ pack prefers Lot scheme)
                results.append(RuleResult(rule_id=self.rule_id, rule_name=self.name, severity=Severity.INFO, category=self.category, passed=True, message=_ok(locale), element_ref=pos.get("id"), details={"note": "ordinal sans préfixe Lot — recommandé 01.xx"}))

        if not results:
            # No currency issue and no ordinal issue → single passing signal
            results.append(RuleResult(rule_id=self.rule_id, rule_name=self.name, severity=self.severity, category=self.category, passed=True, message=_ok(locale)))
        return results


class DZCacobatphInfo(ValidationRule):
    """Informational reminder for CACOBATPH 12.21% when masse salariale is present."""

    rule_id = "dz_btph.cacobatph"
    name = "DZ CACOBATPH 12.21%"
    standard = "dz_btph"
    severity = Severity.INFO
    category = RuleCategory.COMPLIANCE
    description = "CACOBATPH 12,21% (congés payés + intempéries BTP) — rappel informatif lorsque la masse salariale est déclarée."

    async def validate(self, context: ValidationContext) -> list[RuleResult]:
        locale = _get_locale(context)
        data = context.data if isinstance(context.data, dict) else {}
        masse_keys = ("masse_salariale", "masse_salariale_da", "payroll", "salaire_total")
        masse = None
        for k in masse_keys:
            if k in data and data[k] not in (None, "", 0):
                masse = data[k]
                break
            if isinstance(data.get("metadata"), dict) and k in data["metadata"]:
                masse = data["metadata"][k]
                break
        if masse is None:
            # Also scan finance-like context
            for pos in _get_positions(context):
                for k in masse_keys:
                    if k in pos:
                        masse = pos[k]
                        break
                if masse is not None:
                    break
        if masse is None:
            return []  # nothing to remind about
        try:
            masse_dec = Decimal(str(masse))
            cot = (masse_dec * CACOBATPH_RATE).quantize(Decimal("0.01"))
            return [RuleResult(rule_id=self.rule_id, rule_name=self.name, severity=self.severity, category=self.category, passed=True, message=translate("dz_btph.cacobatph.info", locale=locale, masse=str(masse_dec), cot=str(cot), rate="12,21%"), details={"masse_salariale": str(masse_dec), "cacobatph": str(cot), "rate": str(CACOBATPH_RATE)})]
        except (InvalidOperation, ValueError, TypeError):
            return []


# ── Registration ──────────────────────────────────────────────────────────────

_DZ_RULES: list[tuple[ValidationRule, list[str] | None]] = [
    (DZTvaRate(), None),
    (DZRetunueGarantie(), None),
    (DZTAPSupprimee(), None),
    (DZLotBTPH(), None),
    (DZBPUStructure(), None),
    (DZCacobatphInfo(), None),
]


def register_dz_rules() -> None:
    for rule, sets in _DZ_RULES:
        rule_registry.register(rule, sets)
    logger.info("Registered %d DZ BTPH validation rules (standard=dz_btph)", len(_DZ_RULES))


# Auto-register on import (module_loader imports this file on startup)
register_dz_rules()
