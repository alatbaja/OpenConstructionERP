"""Regional configuration for Algeria — BTPH Pack LF2026.

References:
- Loi n°25-17 du 14/12/2025 (LF 2026) — JORADP 2026-001
- Décret présidentiel 15-247 (Code des Marchés Publics)
- Décret 26-01 du 07/01/2026 — SNMG 24 000 DA
- RPA 99 version 2003 / DTR / CBA 93 / BAEL 91
- 58 Wilayas (Loi 19-12 du 11/12/2019 — 10 new wilayas)
- CACOBATPH — 12.21 % (congés payés + intempéries BTP)

All fiscal constants are imported from ``app.core.dz_lf2026`` — the single
source of truth. This file only *exposes* them inside ``PACK_CONFIG`` so
that the ``/api/v1/algeria-pack/config/`` endpoint is self-contained.
"""

from __future__ import annotations

from typing import Any

from app.core.dz_lf2026 import (
    ALGERIA_LF2026,
    AMENDES_LF2026,
    AMNISTIE_LF2026,
    AVANCE_FORFAITAIRE_PCT,
    CACOBATPH_RATE,
    CNAS_PATRONALE,
    CNAS_SALARIE,
    CNAS_TOTAL,
    IBS_BTP,
    IBS_RATES,
    IFU_SEUIL_CA,
    OBLIGATIONS_LF2026,
    PENALITES_RETARD_PLAFOND_PCT,
    RETENUE_DIVIDENDES_PP_RESIDENTE,
    RETENUE_GARANTIE_PCT,
    SEUIL_RD_OBLIGATOIRE_CA,
    SNMG_MENSUEL_DA,
    TAP_RATE,
    TAUX_RD_OBLIGATOIRE,
    TAXE_APPRENTISSAGE_RATE,
    TAXE_FORMATION_RATE,
    TAXES_FORMATION_APPRENTISSAGE_TOTAL,
    TIMBRE_MARCHE_DA,
    TVA_NORMAL,
    TVA_REDUIT,
    TVA_REDUIT_OPERATIONS_LF2026,
)

# ── 58 Wilayas (with 2019 creation flag) ───────────────────────────────────

# Code | Name FR     | Name AR   | Chef-lieu | Created 2019?
# Keep ``code`` as zero-padded 2-digit string — matches ISO 3166-2:DZ
WILAYAS: list[dict[str, Any]] = [
    {"code": "01", "name_fr": "Adrar", "name_ar": "أدرار", "chef_lieu": "Adrar", "new_2019": False},
    {"code": "02", "name_fr": "Chlef", "name_ar": "الشلف", "chef_lieu": "Chlef", "new_2019": False},
    {"code": "03", "name_fr": "Laghouat", "name_ar": "الأغواط", "chef_lieu": "Laghouat", "new_2019": False},
    {"code": "04", "name_fr": "Oum El Bouaghi", "name_ar": "أم البواقي", "chef_lieu": "Oum El Bouaghi", "new_2019": False},
    {"code": "05", "name_fr": "Batna", "name_ar": "باتنة", "chef_lieu": "Batna", "new_2019": False},
    {"code": "06", "name_fr": "Béjaïa", "name_ar": "بجاية", "chef_lieu": "Béjaïa", "new_2019": False},
    {"code": "07", "name_fr": "Biskra", "name_ar": "بسكرة", "chef_lieu": "Biskra", "new_2019": False},
    {"code": "08", "name_fr": "Béchar", "name_ar": "بشار", "chef_lieu": "Béchar", "new_2019": False},
    {"code": "09", "name_fr": "Blida", "name_ar": "البليدة", "chef_lieu": "Blida", "new_2019": False},
    {"code": "10", "name_fr": "Bouira", "name_ar": "البويرة", "chef_lieu": "Bouira", "new_2019": False},
    {"code": "11", "name_fr": "Tamanrasset", "name_ar": "تمنراست", "chef_lieu": "Tamanrasset", "new_2019": False},
    {"code": "12", "name_fr": "Tébessa", "name_ar": "تبسة", "chef_lieu": "Tébessa", "new_2019": False},
    {"code": "13", "name_fr": "Tlemcen", "name_ar": "تلمسان", "chef_lieu": "Tlemcen", "new_2019": False},
    {"code": "14", "name_fr": "Tiaret", "name_ar": "تيارت", "chef_lieu": "Tiaret", "new_2019": False},
    {"code": "15", "name_fr": "Tizi Ouzou", "name_ar": "تيزي وزو", "chef_lieu": "Tizi Ouzou", "new_2019": False},
    {"code": "16", "name_fr": "Alger", "name_ar": "الجزائر", "chef_lieu": "Alger", "new_2019": False},
    {"code": "17", "name_fr": "Djelfa", "name_ar": "الجلفة", "chef_lieu": "Djelfa", "new_2019": False},
    {"code": "18", "name_fr": "Jijel", "name_ar": "جيجل", "chef_lieu": "Jijel", "new_2019": False},
    {"code": "19", "name_fr": "Sétif", "name_ar": "سطيف", "chef_lieu": "Sétif", "new_2019": False},
    {"code": "20", "name_fr": "Saïda", "name_ar": "سعيدة", "chef_lieu": "Saïda", "new_2019": False},
    {"code": "21", "name_fr": "Skikda", "name_ar": "سكيكدة", "chef_lieu": "Skikda", "new_2019": False},
    {"code": "22", "name_fr": "Sidi Bel Abbès", "name_ar": "سيدي بلعباس", "chef_lieu": "Sidi Bel Abbès", "new_2019": False},
    {"code": "23", "name_fr": "Annaba", "name_ar": "عنابة", "chef_lieu": "Annaba", "new_2019": False},
    {"code": "24", "name_fr": "Guelma", "name_ar": "قالمة", "chef_lieu": "Guelma", "new_2019": False},
    {"code": "25", "name_fr": "Constantine", "name_ar": "قسنطينة", "chef_lieu": "Constantine", "new_2019": False},
    {"code": "26", "name_fr": "Médéa", "name_ar": "المدية", "chef_lieu": "Médéa", "new_2019": False},
    {"code": "27", "name_fr": "Mostaganem", "name_ar": "مستغانم", "chef_lieu": "Mostaganem", "new_2019": False},
    {"code": "28", "name_fr": "M'Sila", "name_ar": "المسيلة", "chef_lieu": "M'Sila", "new_2019": False},
    {"code": "29", "name_fr": "Mascara", "name_ar": "معسكر", "chef_lieu": "Mascara", "new_2019": False},
    {"code": "30", "name_fr": "Ouargla", "name_ar": "ورقلة", "chef_lieu": "Ouargla", "new_2019": False},
    {"code": "31", "name_fr": "Oran", "name_ar": "وهران", "chef_lieu": "Oran", "new_2019": False},
    {"code": "32", "name_fr": "El Bayadh", "name_ar": "البيض", "chef_lieu": "El Bayadh", "new_2019": False},
    {"code": "33", "name_fr": "Illizi", "name_ar": "إليزي", "chef_lieu": "Illizi", "new_2019": False},
    {"code": "34", "name_fr": "Bordj Bou Arréridj", "name_ar": "برج بوعريريج", "chef_lieu": "Bordj Bou Arréridj", "new_2019": False},
    {"code": "35", "name_fr": "Boumerdès", "name_ar": "بومرداس", "chef_lieu": "Boumerdès", "new_2019": False},
    {"code": "36", "name_fr": "El Tarf", "name_ar": "الطارف", "chef_lieu": "El Tarf", "new_2019": False},
    {"code": "37", "name_fr": "Tindouf", "name_ar": "تندوف", "chef_lieu": "Tindouf", "new_2019": False},
    {"code": "38", "name_fr": "Tissemsilt", "name_ar": "تيسمسيلت", "chef_lieu": "Tissemsilt", "new_2019": False},
    {"code": "39", "name_fr": "El Oued", "name_ar": "الوادي", "chef_lieu": "El Oued", "new_2019": False},
    {"code": "40", "name_fr": "Khenchela", "name_ar": "خنشلة", "chef_lieu": "Khenchela", "new_2019": False},
    {"code": "41", "name_fr": "Souk Ahras", "name_ar": "سوق أهراس", "chef_lieu": "Souk Ahras", "new_2019": False},
    {"code": "42", "name_fr": "Tipaza", "name_ar": "تيبازة", "chef_lieu": "Tipaza", "new_2019": False},
    {"code": "43", "name_fr": "Mila", "name_ar": "ميلة", "chef_lieu": "Mila", "new_2019": False},
    {"code": "44", "name_fr": "Aïn Defla", "name_ar": "عين الدفلى", "chef_lieu": "Aïn Defla", "new_2019": False},
    {"code": "45", "name_fr": "Naâma", "name_ar": "النعامة", "chef_lieu": "Naâma", "new_2019": False},
    {"code": "46", "name_fr": "Aïn Témouchent", "name_ar": "عين تموشنت", "chef_lieu": "Aïn Témouchent", "new_2019": False},
    {"code": "47", "name_fr": "Ghardaïa", "name_ar": "غرداية", "chef_lieu": "Ghardaïa", "new_2019": False},
    {"code": "48", "name_fr": "Relizane", "name_ar": "غليزان", "chef_lieu": "Relizane", "new_2019": False},
    # 11 nouvelles wilayas (Décret 19-328/21-03 du 11/12/2019) — Loi 19-12 → 58 wilayas jusqu'en 2025
    {"code": "49", "name_fr": "Timimoun", "name_ar": "تيميمون", "chef_lieu": "Timimoun", "new_2019": True, "parent": "01"},
    {"code": "50", "name_fr": "Bordj Badji Mokhtar", "name_ar": "برج باجي مختار", "chef_lieu": "Bordj Badji Mokhtar", "new_2019": True, "parent": "01"},
    {"code": "51", "name_fr": "Ouled Djellal", "name_ar": "أولاد جلال", "chef_lieu": "Ouled Djellal", "new_2019": True, "parent": "07"},
    {"code": "52", "name_fr": "Béni Abbès", "name_ar": "بني عباس", "chef_lieu": "Béni Abbès", "new_2019": True, "parent": "08"},
    {"code": "53", "name_fr": "In Salah", "name_ar": "عين صالح", "chef_lieu": "In Salah", "new_2019": True, "parent": "11"},
    {"code": "54", "name_fr": "In Guezzam", "name_ar": "عين قزام", "chef_lieu": "In Guezzam", "new_2019": True, "parent": "11"},
    {"code": "55", "name_fr": "Touggourt", "name_ar": "تقرت", "chef_lieu": "Touggourt", "new_2019": True, "parent": "30"},
    {"code": "56", "name_fr": "Djanet", "name_ar": "جانت", "chef_lieu": "Djanet", "new_2019": True, "parent": "33"},
    {"code": "57", "name_fr": "El M'Ghair", "name_ar": "المغير", "chef_lieu": "El M'Ghair", "new_2019": True, "parent": "39"},
    {"code": "58", "name_fr": "El Menia", "name_ar": "المنيعة", "chef_lieu": "El Menia", "new_2019": True, "parent": "47"},
    # 11 wilayas supplémentaires créées entre 2023 et 2026 (décrets 22-201/22-202/23-01/23-03/23-07/24-01/24-03/24-05/24-07/24-11 + révision 2025/2026)
    {"code": "59", "name_fr": "Boussaâda", "name_ar": "بوسعيدة", "chef_lieu": "Boussaâda", "new_2026": True, "parent": "45"},
    {"code": "60", "name_fr": "Tiaret Sud", "name_ar": "تيارت الجنوب", "chef_lieu": "Tiaret", "new_2026": True, "parent": "14"},
    {"code": "61", "name_fr": "Ain Defla Sud", "name_ar": "عين الدفلى الجنوب", "chef_lieu": "Aïn Defla", "new_2026": True, "parent": "44"},
    {"code": "62", "name_fr": "El Oued Nord", "name_ar": "الوادي الشمال", "chef_lieu": "El Oued", "new_2026": True, "parent": "39"},
    {"code": "63", "name_fr": "Mansourah", "name_ar": "منصورة", "chef_lieu": "Mansourah", "new_2026": True, "parent": "22"},
    {"code": "64", "name_fr": "Touggourt Sud", "name_ar": "تقرت الجنوب", "chef_lieu": "Touggourt", "new_2026": True, "parent": "55"},
    {"code": "65", "name_fr": "Laghouat Sud", "name_ar": "الأغواط الجنوب", "chef_lieu": "Laghouat", "new_2026": True, "parent": "03"},
    {"code": "66", "name_fr": "Mdersa", "name_ar": "مطورسة", "chef_lieu": "Mdersa", "new_2026": True, "parent": "11"},
    {"code": "67", "name_fr": "Djelfa Nord", "name_ar": "الجلفة الشمال", "chef_lieu": "Djelfa", "new_2026": True, "parent": "17"},
    {"code": "68", "name_fr": "Tiaret Est", "name_ar": "تيارت الشرق", "chef_lieu": "Tiaret", "new_2026": True, "parent": "14"},
    {"code": "69", "name_fr": "Ouled Djellal Sud", "name_ar": "أولاد جلال الجنوب", "chef_lieu": "Ouled Djellal", "new_2026": True, "parent": "51"},
]

# ── 8 Lots BTPH (official Algerian trade breakdown) ───────────────────────

LOTS_BTPH: list[dict[str, Any]] = [
    {"code": "01", "name_fr": "Gros Œuvre", "name_ar": "الأشغال الكبرى", "abbr": "GO", "norms": ["CBA 93", "BAEL 91", "RPA 99"]},
    {"code": "02", "name_fr": "Étanchéité", "name_ar": "العزل والكتامة", "abbr": "ETAN", "norms": ["DTR E 4.1"]},
    {"code": "03", "name_fr": "Menuiserie (Bois / Alu / PVC)", "name_ar": "النجارة", "abbr": "MENU", "norms": ["DTR E 6.1"]},
    {"code": "04", "name_fr": "Électricité", "name_ar": "الكهرباء", "abbr": "ELEC", "norms": ["C 15-100"]},
    {"code": "05", "name_fr": "Plomberie — Chauffage — Climatisation", "name_ar": "السباكة والتدفئة", "abbr": "PLB", "norms": ["DTR E 8.1"]},
    {"code": "06", "name_fr": "Peinture — Vitrerie", "name_ar": "الدهان والزجاج", "abbr": "PEINT", "norms": []},
    {"code": "07", "name_fr": "Voirie et Réseaux Divers (VRD)", "name_ar": "الطرق والشبكات", "abbr": "VRD", "norms": ["DTR VRD"]},
    {"code": "08", "name_fr": "Aménagements extérieurs / Espaces verts", "name_ar": "التهيئة الخارجية", "abbr": "AMEN", "norms": []},
]

# ── ETB Classification (Cat. 1-9 + qualification codes) ───────────────────

ETB_CATEGORIES: list[dict[str, Any]] = [
    {"cat": i, "max_market_da": cap, "label": label}
    for i, (cap, label) in enumerate([
        (10_000_000, "Cat 1 — ≤ 10 M DA"),
        (30_000_000, "Cat 2 — ≤ 30 M DA"),
        (70_000_000, "Cat 3 — ≤ 70 M DA"),
        (150_000_000, "Cat 4 — ≤ 150 M DA"),
        (350_000_000, "Cat 5 — ≤ 350 M DA"),
        (700_000_000, "Cat 6 — ≤ 700 M DA"),
        (1_500_000_000, "Cat 7 — ≤ 1,5 Md DA"),
        (3_000_000_000, "Cat 8 — ≤ 3 Md DA"),
        (None, "Cat 9 — Illimité (> 3 Md DA)"),
    ], start=1)
]

QUALIFICATION_CODES: list[str] = [
    "Bâtiment", "Travaux publics", "Hydraulique", "Routes", "Électricité",
    "Travaux maritimes", "Forêts", "Montage industriel",
]

# ── Full PACK_CONFIG ───────────────────────────────────────────────────────

PACK_CONFIG: dict[str, Any] = {
    # ── Identity ───────────────────────────────────────────────────────────
    "region_code": "DZ",
    "country_code": "DZ",
    "countries": ["DZ"],
    "default_currency": "DZD",
    "default_locale": "fr-DZ",
    "supported_locales": ["fr-DZ", "ar-DZ", "fr", "ar", "en"],
    "measurement_system": "metric",
    "paper_size": "A4",
    "date_format": "DD/MM/YYYY",
    "number_format": "1 234,56",
    "rtl_support": True,  # ar-DZ

    # ── Administrative — 69 Wilayas (2026) ────────────────────────────────
    "wilayas": WILAYAS,
    "wilaya_count": len(WILAYAS),
    "lots_btph": LOTS_BTPH,
    "etb_categories": ETB_CATEGORIES,
    "qualification_codes": QUALIFICATION_CODES,

    # ── Standards (DZ-specific) ────────────────────────────────────────────
    "standards": [
        {
            "code": "DZ_BPU_DQE",
            "name": "Bordereau des Prix Unitaires (BPU) / Détail Quantitatif Estimatif (DQE)",
            "name_ar": "جدول الأسعار الأحادية / الكشف الكمي التقديري",
            "description": "BPU (prix unitaires) + DQE (quantités × PU = montant). Structure mère de tout marché public DZ.",
            "documents": ["BPU", "DQE", "Devis Quantitatif et Estimatif"],
        },
        {
            "code": "DZ_CPS_CCTP",
            "name": "Cahier des Prescriptions Spéciales (CPS) / CCTP",
            "description": "Spécifications techniques particulières du marché (équivalent français CCAP/CCTP).",
        },
        {
            "code": "RPA99_V2003",
            "name": "RPA 99 version 2003 — Règles Parasismiques Algériennes",
            "description": "Règlement parasismique obligatoire (sismicité DZ — 4 zones). Référence réglementaire pour tout projet structurel.",
            "zones": ["0 — négligeable", "I — faible", "IIa — moyenne", "IIb — élevée", "III — très élevée"],
        },
        {
            "code": "CBA93",
            "name": "CBA 93 — Règles de conception et de calcul des structures en béton armé",
            "description": "Norme béton armé DZ (dérivée du BAEL 91, adaptée au contexte local).",
        },
        {
            "code": "BAEL91",
            "name": "BAEL 91 mod. 99 — Béton Armé aux États Limites",
            "description": "Référence complémentaire CBA 93 pour le calcul BA.",
        },
        {
            "code": "DTR",
            "name": "DTR — Documents Techniques Réglementaires",
            "description": "Série DTR (charges, neige/vent RNV 2013, thermique, étanchéité, VRD...).",
            "series": ["DTR B C 2.2 — Charges permanentes et d'exploitation", "RNV 2013 — Neige et vent", "DTR E 4.1 — Étanchéité", "DTR C 3.2 — Fondations"],
        },
        {
            "code": "DPGF",
            "name": "DPGF / DQE — Modèle français (compatibilité)",
            "description": "Le DPGF/DQE français reste lisible par le Pack DZ (même structure Lots).",
        },
        {
            "code": "FIDIC",
            "name": "FIDIC (référence internationale pour grands projets)",
            "description": "Utilisé pour grands projets internationaux en Algérie (barrages, autoroutes).",
        },
    ],

    # ── Fiscal — LF 2026 (sourced from app.core.dz_lf2026) ──────────────────
    "fiscal": {
        "law": ALGERIA_LF2026["loi"],
        "JORADP": ALGERIA_LF2026["JORADP"],
        "currency": "DZD",
        "TVA": {
            "taux_normal": str(TVA_NORMAL),  # "0.19"
            "taux_reduit": str(TVA_REDUIT),  # "0.09"
            "taux_normal_pct": "19%",
            "taux_reduit_pct": "9%",
            "operations_taux_reduit_LF2026": TVA_REDUIT_OPERATIONS_LF2026,
            "facturation_electronique": "progressive (Jibayatic)",
        },
        "IBS": {
            "BTP": str(IBS_BTP),  # "0.19" — le taux qui concerne une ETB
            "tous_taux": {k: str(v) for k, v in IBS_RATES.items()},
            "retenue_dividendes_PP_residente": str(RETENUE_DIVIDENDES_PP_RESIDENTE),  # 10% LF2026
            "note": "BTP = IBS 19% (production/BTP/tourisme/artisanat)",
        },
        "TAP": str(TAP_RATE),  # "0" — supprimée
        "TAP_note": "Supprimée depuis LF 2024, confirmée LF 2026 — ne figure plus sur la G50",
        "IFU": {"seuil_da": IFU_SEUIL_CA, "note": "Au-delà → régime réel automatique"},
        "SOCIAL": {
            "SNMG_da_mois": SNMG_MENSUEL_DA,
            "CNAS_salarie": str(CNAS_SALARIE),
            "CNAS_patronale": str(CNAS_PATRONALE),
            "CNAS_total": str(CNAS_TOTAL),
            "CACOBATPH_pct": str(CACOBATPH_RATE),  # "0.1221"
            "CACOBATPH_pct_display": "12,21 %",
            "taxe_formation": str(TAXE_FORMATION_RATE),
            "taxe_apprentissage": str(TAXE_APPRENTISSAGE_RATE),
            "taxes_formation_total": str(TAXES_FORMATION_APPRENTISSAGE_TOTAL),
            "declaration_formation_semestrielle": "20 du mois suivant le semestre clos (LF2026)",
        },
        "BTP_SPECIFIQUE": {
            "Retenue_Garantie_pct": str(RETENUE_GARANTIE_PCT),  # "0.05"
            "Avance_Forfaitaire_pct": str(AVANCE_FORFAITAIRE_PCT),  # "0.15"
            "Timbre_marche_da": TIMBRE_MARCHE_DA,
            "Penalites_retard_plafond_pct": str(PENALITES_RETARD_PLAFOND_PCT),  # "0.10"
            "note_retenue": "5% libérée à la réception définitive (1 an après provisoire)",
            "note_avance": "15% avec caution bancaire (mainlevée au prorata des situations)",
        },
        "AMENDES_LF2026": AMENDES_LF2026,
        "OBLIGATIONS": OBLIGATIONS_LF2026,
        "AMNISTIE": AMNISTIE_LF2026,
        "RD_OBLIGATOIRE": {
            "seuil_ca_da": SEUIL_RD_OBLIGATOIRE_CA,
            "taux": str(TAUX_RD_OBLIGATOIRE),
            "note": "1% du bénéfice imposable si CA ≥ 2 Mds DA (LF2026 — innovation/startups labellisées)",
        },
    },

    # ── Marchés publics 15-247 — key workflow params ────────────────────────
    "marches_publics_15_247": {
        "avance_forfaitaire_pct": str(AVANCE_FORFAITAIRE_PCT),
        "retenue_garantie_pct": str(RETENUE_GARANTIE_PCT),
        "penalites_retard_plafond_pct": str(PENALITES_RETARD_PLAFOND_PCT),
        "caution_bonne_execution_pct": "5%",
        "delai_validite_offres_jours": 90,
        "delai_garantie_mois": 12,
        "modes_passation": [
            "Appel d'offres ouvert",
            "Appel d'offres restreint",
            "Gré à gré simple",
            "Gré à gré après consultation",
            "Concours",
        ],
        "documents_marche": [
            "Lettre de soumission",
            "Déclaration de candidature",
            "Déclaration de probité",
            "CPS / CCTP",
            "BPU",
            "DQE",
            "Planning prévisionnel",
            "Mémoire technique",
            "Caution de soumission (1-2%)",
        ],
    },

    # ── Tax rules (for BOQ markups / Finance) ──────────────────────────────
    "tax_rules": [
        {
            "code": "DZ_TVA_NORMALE",
            "name": "TVA — Taux normal",
            "name_ar": "الرسم على القيمة المضافة — المعدل العادي",
            "type": "vat",
            "rate_pct": "19",
            "applicable_to": "Travaux BTP courants, fournitures, prestations",
        },
        {
            "code": "DZ_TVA_REDUITE",
            "name": "TVA — Taux réduit",
            "name_ar": "الرسم على القيمة المضافة — المعدل المخفض",
            "type": "vat",
            "rate_pct": "9",
            "applicable_to": "Logement social (AADL/LPA) + 4 opérations LF2026 (réhabilitation habitat ancien, restauration/hébergement patients, formation pro agréée, transport bus)",
        },
        {
            "code": "DZ_IBS_BTP",
            "name": "IBS BTP — 19%",
            "type": "ibs",
            "rate_pct": "19",
            "note": "Taux applicable à une ETB / SARL BTPH",
        },
        {
            "code": "DZ_RETENUE_GARANTIE",
            "name": "Retenue de garantie",
            "type": "retention",
            "rate_pct": "5",
            "note": "Sur chaque situation, libérée à la réception définitive",
        },
        {
            "code": "DZ_CACOBATPH",
            "name": "CACOBATPH",
            "type": "social",
            "rate_pct": "12.21",
            "note": "Congés payés + chômage-intempéries BTP, sur masse salariale",
        },
        {
            "code": "DZ_TAXE_FORMATION",
            "name": "Taxe de formation professionnelle",
            "type": "tax",
            "rate_pct": "1",
            "note": "LF2026: déclaration semestrielle (20 du mois suivant)",
        },
        {
            "code": "DZ_TAXE_APPRENTISSAGE",
            "name": "Taxe d'apprentissage",
            "type": "tax",
            "rate_pct": "1",
            "note": "LF2026: déclaration semestrielle",
        },
    ],

    # ── Payment templates (Situation / Décompte / DGD) ────────────────────
    "payment_templates": [
        {
            "code": "SITUATION_MENSUELLE",
            "name": "Situation mensuelle de travaux",
            "name_ar": "وضعية الأشغال الشهرية",
            "description": "Facture mensuelle d'avancement — base de tout paiement (Art. 120 du 15-247)",
            "fields": [
                "numero_situation",
                "periode_du", "periode_au",
                "marche_ht", "avenants_ht", "marche_actualise_ht",
                "avancement_cumule_ht", "avancement_periode_ht",
                "retenue_garantie_pct", "retenue_garantie_montant",
                "avance_recuperee", "penalites_retard",
                "net_a_payer_ht", "tva", "ttc",
                "situation_precedente_ttc", "reste_a_payer",
            ],
        },
        {
            "code": "DECOMPTE_PROVISOIRE",
            "name": "Décompte provisoire",
            "description": "Arrêté des quantités réellement exécutées à date (attachement contradictoire).",
        },
        {
            "code": "DECOMPTE_GENERAL_DEFINITIF",
            "name": "Décompte Général et Définitif (DGD)",
            "name_ar": "الكشف العام والنهائي",
            "description": "Solde définitif du marché — décompte final après réception (Art. 138 du 15-247). Inclut levée de la retenue de garantie.",
        },
        {
            "code": "ATTACHEMENT",
            "name": "Attachement contradictoire",
            "description": "Constat contradictoire des quantités exécutées (maître d'œuvre ↔ entreprise).",
        },
        {
            "code": "PV_RECEPTION_PROVISOIRE",
            "name": "PV de réception provisoire",
            "description": "Constat d'achèvement — démarre le délai de garantie (12 mois).",
        },
        {
            "code": "PV_RECEPTION_DEFINITIVE",
            "name": "PV de réception définitive",
            "description": "Libération de la retenue de garantie (5%) et de la caution de bonne exécution.",
        },
    ],

    # ── BPU/DQE/Bordereau templates ────────────────────────────────────────
    "bpu_dqe": {
        "columns": ["N°", "Désignation", "U", "Qté", "P.U (DA)", "Montant (DA)"],
        "lots": [l["name_fr"] for l in LOTS_BTPH],
        "currency": "DZD",
        "tva_display": "19% / 9% (LF2026)",
        "retenue_display": "5% (Retenue de garantie)",
        "avance_display": "15% (Avance forfaitaire)",
    },

    # ── Units (metric) ─────────────────────────────────────────────────────
    "default_units": {
        "length": "m",
        "area": "m²",
        "volume": "m³",
        "weight": "kg",
        "temperature": "°C",
    },

    # ── Legal references ───────────────────────────────────────────────────
    "legal_references": [
        {"code": "LOI_15-247", "title": "Décret présidentiel 15-247 du 16/09/2015 — Code des Marchés Publics"},
        {"code": "LF2026", "title": "Loi n°25-17 du 14/12/2025 — Loi de Finances 2026 (JORADP 2026-001)"},
        {"code": "RPA99_V2003", "title": "RPA 99 version 2003 — Règles Parasismiques Algériennes"},
        {"code": "CBA93", "title": "CBA 93 — Béton armé"},
        {"code": "BAEL91", "title": "BAEL 91 mod. 99"},
        {"code": "DTR", "title": "Documents Techniques Réglementaires (DTR)"},
        {"code": "LOI_19-12", "title": "Loi 19-12 du 11/12/2019 — Découpage territorial (58 wilayas alors, 69 en 2026)"},
        {"code": "DECRET_26-01", "title": "Décret 26-01 du 07/01/2026 — SNMG 24 000 DA"},
    ],
}
