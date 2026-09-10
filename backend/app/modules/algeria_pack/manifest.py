"""Module manifest for oe_algeria_pack — Algérie BTPH."""

from app.core.module_loader import ModuleManifest

manifest = ModuleManifest(
    name="oe_algeria_pack",
    version="1.0.0",
    display_name="Algérie BTPH Pack — DZ LF2026",
    display_name_i18n={
        "fr": "Pack Régional — Algérie BTPH (LF 2026)",
        "ar": "حزمة الجزائر BTPH — قانون المالية 2026",
        "de": "Regionalpaket — Algerien BTPH (LF 2026)",
        "ru": "Региональный пакет — Алжир BTPH",
    },
    description=(
        "Algérie BTPH standards: Loi 15-247 (Marchés publics), "
        "Loi de Finances 2026 (TVA 19%/9%, IBS 19%, TAP 0%, Retenue 5%, "
        "Avance 15%, CACOBATPH 12.21%), 58 Wilayas, 8 Lots BTPH, "
        "BPU/DQE/Bordereau CNTC templates, Situation/Décompte/DGD workflow, "
        "RPA 99 v2003 / CBA 93 references, and DZD currency."
    ),
    author="OpenConstructionERP Core Team",
    category="regional",
    depends=[],
    auto_install=False,
    enabled=True,
)
