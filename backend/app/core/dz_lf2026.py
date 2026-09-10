"""Algeria — Loi de Finances 2026 (Loi n°25-17 du 14/12/2025) — Fiscal reference.

Single source of truth for every DZ-specific fiscal constant.
Used by:
  • oe_algeria pack (config, validation rules, finance service)
  • BOQ markups (TVA, Retenue de Garantie)
  • Finance / Budget / EVM
  • Validation engine (dz_* rules)

All rates are Decimal strings — never floats — so that DB and API layers
can pass them straight to ``Decimal()`` without binary-float artefacts.

References
----------
- JORADP 2026-001 — Loi n°25-17 (14/12/2025)
- Deloitte Algérie — Loi de Finances 2026 (09/04/2026)
- MFDGI — Nouvelles modalités Jibayatic Art.111 (21/01/2026)
- Almawarid — Résumé LF2026 (17/04/2026)
- EY Tax News 2026-0245

Key LF2026 changes vs LF2024
------------------------------
- TAP 0% — supprimée définitivement depuis LF2024, confirmée LF2026
  (ne figure plus sur la G50)
- IBS différencié inchangé mais confirmé: 19% BTP/Production
- TVA taux réduit 9% — étendu à 4 opérations (réhabilitation habitat ancien,
  restauration/hébergement patients, formation professionnelle agréée, transport bus)
- Retenue à la source dividendes PP résidentes: 15% → 10%
- Taxe formation/apprentissage: déclaration semestrielle (20 du mois suivant)
- Amnistie fiscale volontaire 8% jusqu'au 31/12/2026
- Obligation déclaration en ligne via Jibayatic (G50, G29 avec NIN)
- Amendes BTP relevées: 50 000 DA défaut identification chantier/sous-traitants
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any, Final

# ── TVA ────────────────────────────────────────────────────────────────────

TVA_NORMAL: Final[Decimal] = Decimal("0.19")  # 19% — travaux BTP courants
TVA_REDUIT: Final[Decimal] = Decimal("0.09")  # 9% — logement social + 4 cas LF2026
TVA_REDUIT_OPERATIONS_LF2026: Final[list[str]] = [
    "Réhabilitation et viabilisation des anciens biens immeubles à usage d'habitation",
    "Restauration et hébergement fournis aux patients par les établissements de santé",
    "Prestations de formation professionnelle (établissements agréés) + hébergement/restauration directe",
    "Transport de voyageurs par bus (aligné sur le ferroviaire)",
]

TVA_RATES: Final[dict[str, Decimal]] = {
    "normal": TVA_NORMAL,
    "reduit": TVA_REDUIT,
    "exonere": Decimal("0"),
}

# ── IBS / IS — Taux différenciés (inchangés LF2026) ────────────────────────

IBS_PRODUCTION_BTP_TOURISME: Final[Decimal] = Decimal("0.19")  # 19%
IBS_SERVICES_LIBERAL: Final[Decimal] = Decimal("0.23")  # 23%
IBS_COMMERCE_IMPORT_REVENTE: Final[Decimal] = Decimal("0.26")  # 26%

IBS_RATES: Final[dict[str, Decimal]] = {
    "production_btp_tourisme_artisanat": IBS_PRODUCTION_BTP_TOURISME,
    "services_professions_liberales": IBS_SERVICES_LIBERAL,
    "commerce_import_revente_negoce": IBS_COMMERCE_IMPORT_REVENTE,
}

# BTP = 19% — c'est le taux applicable à une ETB / SARL BTPH
IBS_BTP: Final[Decimal] = IBS_PRODUCTION_BTP_TOURISME

# Retenue à la source sur dividendes — LF2026: 15% → 10% (PP résidentes)
RETENUE_DIVIDENDES_PP_RESIDENTE: Final[Decimal] = Decimal("0.10")

# IFU
IFU_SEUIL_CA: Final[int] = 15_000_000  # DA — au-delà → régime réel automatique

# TAP — supprimée
TAP_RATE: Final[Decimal] = Decimal("0")  # 0% — supprimée LF2024, confirmée LF2026

# ── Social — CNAS / CACOBATPH / SNMG ───────────────────────────────────────

SNMG_MENSUEL_DA: Final[int] = 24_000  # Décret 26-01 du 07/01/2026 — brut/mois
CNAS_SALARIE: Final[Decimal] = Decimal("0.09")  # 9%
CNAS_PATRONALE: Final[Decimal] = Decimal("0.26")  # 26% → total 35%
CNAS_TOTAL: Final[Decimal] = CNAS_SALARIE + CNAS_PATRONALE

# CACOBATPH — congé payé + chômage-intempéries (spécifique BTP)
CACOBATPH_RATE: Final[Decimal] = Decimal("0.1221")  # 12,21%

# Taxes formation & apprentissage (LF2026: semestrielle)
TAXE_FORMATION_RATE: Final[Decimal] = Decimal("0.01")  # 1%
TAXE_APPRENTISSAGE_RATE: Final[Decimal] = Decimal("0.01")  # 1%
TAXES_FORMATION_APPRENTISSAGE_TOTAL: Final[Decimal] = TAXE_FORMATION_RATE + TAXE_APPRENTISSAGE_RATE

# ── BTP spécifique (CCAG / Décret 15-247) ──────────────────────────────────

RETENUE_GARANTIE_PCT: Final[Decimal] = Decimal("0.05")  # 5% jusqu'à réception définitive
AVANCE_FORFAITAIRE_PCT: Final[Decimal] = Decimal("0.15")  # 15% avec caution bancaire
AVANCE_FORFAITAIRE_PLAFOND_PCT: Final[Decimal] = Decimal("0.15")
TIMBRE_MARCHE_DA: Final[int] = 1_000

# Pénalités de retard — 10% plafond (Art. 147 du 15-247)
PENALITES_RETARD_PLAFOND_PCT: Final[Decimal] = Decimal("0.10")

# ── Amendes LF2026 relevées (TVA / chantier) ────────────────────────────────

AMENDES_LF2026: Final[dict[str, int]] = {
    "infraction_generale_tva": 25_000,  # contre 500-2 500 avant
    "manoeuvre_frauduleuse_tva": 100_000,  # contre 1 000-5 000
    "defaut_plaque_identification": 10_000,  # contre 1 000
    "defaut_identification_chantier_sous_traitant": 50_000,  # BTP — contre 1 000-5 000
}

# ── Obligations déclaratives LF2026 (Jibayatic) ────────────────────────────

OBLIGATIONS_LF2026: Final[dict[str, str]] = {
    "G50": "Mensuelle obligatoire via Jibayatic (réel / simplifié)",
    "G29_salaires": "Électronique obligatoire + NIN par salarié",
    "G29_format": "Série G n°29",
    "DAS_CNAS": "Avant le 31 janvier",
    "liasse_fiscale_G4_G5": "Avant le 30 avril",
    "ISF_declaration": "Électronique tous les 4 ans avant le 30 avril",
    "ISF_paiement": "Annuel par rôle individuel (recette du domicile)",
}

# ── Amnistie 2026 ───────────────────────────────────────────────────────────

AMNISTIE_LF2026: Final[dict[str, Any]] = {
    "regularisation_volontaire_taux": Decimal("0.08"),  # 8% libératoire sans pénalités
    "regularisation_limite": "2026-12-31",
    "annulation_dettes_2011_et_avant": True,  # sauf manœuvres frauduleuses
    "dettes_31_12_2025_si_paiement_avant_31_12_2026": {
        "annulation_penalites_assiette_recouvrement": True,
        "abattement_droits_simples_pct": Decimal("0.30"),  # 30%
        "paiement_comptant_ou_echelonne": True,
    },
}

# ── Nouveau: contribution R&D obligatoire (LF2026) ──────────────────────────

# Établissements CA >= 2 Mds DA → 1% du bénéfice imposable en R&D / innovation
SEUIL_RD_OBLIGATOIRE_CA: Final[int] = 2_000_000_000
TAUX_RD_OBLIGATOIRE: Final[Decimal] = Decimal("0.01")  # 1%

# ── Fraude aggravée ─────────────────────────────────────────────────────────

PEINE_FRAUDE_AGGRAVEE: Final[dict[str, Any]] = {
    "emprisonnement_ans": (5, 10),
    "amende_da": (5_000_000, 10_000_000),
    "criteres": [
        "Organisation structurée / pluralité de complices",
        "Usage des technologies de l'information (cyberfraude)",
        "Ampleur nationale, transnationale ou large couverture",
        "Préjudice grave aux finances publiques",
    ],
}

# ── Agrégat exporté (consommé par oe_algeria / finance / validation) ────────

ALGERIA_LF2026: Final[dict[str, Any]] = {
    "loi": "Loi n°25-17 du 14/12/2025 (LF 2026)",
    "JORADP": "2026-001",
    "devise": "DZD",
    "TVA": {
        "taux_normal": str(TVA_NORMAL),
        "taux_reduit": str(TVA_REDUIT),
        "taux_reduit_elargi_LF2026": TVA_REDUIT_OPERATIONS_LF2026,
        "facturation_electronique": "progressive, obligatoire (Jibayatic)",
    },
    "IBS": {
        "production_btp_tourisme_artisanat": str(IBS_PRODUCTION_BTP_TOURISME),
        "services_professions_liberales": str(IBS_SERVICES_LIBERAL),
        "commerce_import_revente": str(IBS_COMMERCE_IMPORT_REVENTE),
        "retenue_dividendes_PP_residente": str(RETENUE_DIVIDENDES_PP_RESIDENTE),
        "acomptes_remboursement_delai_ans": 4,
        "BTP_applicable": str(IBS_BTP),
    },
    "TAP": str(TAP_RATE),  # "0" — supprimée
    "IFU": {"seuil_da": IFU_SEUIL_CA, "note": "Au-delà → régime réel automatique"},
    "SOCIAL": {
        "SNMG_da_mois": SNMG_MENSUEL_DA,
        "CNAS_salarie": str(CNAS_SALARIE),
        "CNAS_patronale": str(CNAS_PATRONALE),
        "CNAS_total": str(CNAS_TOTAL),
        "CACOBATPH": str(CACOBATPH_RATE),
        "taxe_formation": str(TAXE_FORMATION_RATE),
        "taxe_apprentissage": str(TAXE_APPRENTISSAGE_RATE),
        "taxes_formation_apprentissage_total": str(TAXES_FORMATION_APPRENTISSAGE_TOTAL),
        "declaration_taxes_formation_semestrielle": "20 du mois suivant le semestre clos",
    },
    "BTP_SPECIFIQUE": {
        "Retenue_Garantie_pct": str(RETENUE_GARANTIE_PCT),
        "Avance_Forfaitaire_pct": str(AVANCE_FORFAITAIRE_PCT),
        "Avance_plafond_pct": str(AVANCE_FORFAITAIRE_PLAFOND_PCT),
        "Timbre_marche_da": TIMBRE_MARCHE_DA,
        "Penalites_retard_plafond_pct": str(PENALITES_RETARD_PLAFOND_PCT),
    },
    "AMENDES_LF2026": AMENDES_LF2026,
    "OBLIGATIONS": OBLIGATIONS_LF2026,
    "AMNISTIE": AMNISTIE_LF2026,
    "RD_OBLIGATOIRE": {
        "seuil_ca_da": SEUIL_RD_OBLIGATOIRE_CA,
        "taux_pct": str(TAUX_RD_OBLIGATOIRE),
        "note": "1% du bénéfice imposable si CA >= 2 Mds DA (interne ou open innovation avec startups labellisées)",
    },
}


# ── Helpers ─────────────────────────────────────────────────────────────────

def get_tva_rate(operation_type: str = "normal") -> Decimal:
    """Return the applicable TVA rate for an operation type.

    Args:
        operation_type: "normal" | "reduit" | "exonere" | any alias.
    """
    key = operation_type.lower().strip()
    if key in ("reduit", "réduit", "9", "9%"):
        return TVA_REDUIT
    if key in ("exonere", "exonéré", "0", "0%"):
        return Decimal("0")
    return TVA_NORMAL


def get_ibs_rate(activite: str = "btp") -> Decimal:
    """Return the IBS rate for an activity type.

    Args:
        activite: "btp" | "production" | "service" | "commerce" / aliases
    """
    key = activite.lower().strip()
    if key in ("btp", "production", "tourisme", "artisanat", "etb", "btph"):
        return IBS_PRODUCTION_BTP_TOURISME
    if key in ("service", "services", "liberal", "libérale", "profession"):
        return IBS_SERVICES_LIBERAL
    if key in ("commerce", "import", "revente", "negoce", "négoce"):
        return IBS_COMMERCE_IMPORT_REVENTE
    return IBS_BTP  # default prudent = BTP


def calc_tva(montant_ht: Decimal | str | int | float, tva_rate: Decimal | None = None) -> Decimal:
    """TVA = HT × taux."""
    ht = Decimal(str(montant_ht))
    rate = tva_rate if tva_rate is not None else TVA_NORMAL
    return (ht * rate).quantize(Decimal("0.01"))


def calc_ttc(montant_ht: Decimal | str | int | float, tva_rate: Decimal | None = None) -> Decimal:
    """TTC = HT + TVA."""
    ht = Decimal(str(montant_ht))
    return ht + calc_tva(ht, tva_rate)


def calc_retenue_garantie(montant_ht: Decimal | str | int | float) -> Decimal:
    """Retenue de garantie 5% sur HT."""
    return (Decimal(str(montant_ht)) * RETENUE_GARANTIE_PCT).quantize(Decimal("0.01"))


def calc_cacobatph(masse_salariale: Decimal | str | int | float) -> Decimal:
    """CACOBATPH 12,21% sur masse salariale."""
    return (Decimal(str(masse_salariale)) * CACOBATPH_RATE).quantize(Decimal("0.01"))


def calc_rd_obligatoire(benefice_imposable: Decimal | str | int | float, ca_annuel: Decimal | str | int | float) -> Decimal:
    """1% R&D obligatoire si CA >= 2 Mds DA, sinon 0."""
    ca = Decimal(str(ca_annuel))
    if ca < SEUIL_RD_OBLIGATOIRE_CA:
        return Decimal("0")
    return (Decimal(str(benefice_imposable)) * TAUX_RD_OBLIGATOIRE).quantize(Decimal("0.01"))
