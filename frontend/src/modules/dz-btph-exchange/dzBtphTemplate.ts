import type { CountryTemplate } from '../_shared/templateTypes';

/** DZ BTPH — BPU/DQE template (Algérie). */
export const DZ_BTPH_TEMPLATE: CountryTemplate = {
  id: 'dz-btph',
  name: 'Algérie BTPH — BPU / DQE',
  country: 'Algérie',
  countryCode: 'DZ',
  currency: 'DZD',
  currencySymbol: 'DA',
  classification: 'Lot BTPH',
  defaultColumns: {
    ordinal: '0',
    description: '1',
    unit: '2',
    quantity: '3',
    unitRate: '4',
    total: '5',
    section: '6',
  },
  requiredColumns: ['description', 'quantity'],
  acceptedExtensions: ['.csv', '.tsv', '.xlsx'],
};

/** 8 Lots BTPH — Algerian official breakdown (CCAG 15-247). */
export const LOTS_BTPH: { code: string; label: string; labelFr: string; labelAr: string }[] = [
  { code: '01', label: 'Structural Works', labelFr: 'Gros Œuvre', labelAr: 'الأشغال الكبرى' },
  { code: '02', label: 'Waterproofing', labelFr: 'Étanchéité', labelAr: 'العزل' },
  { code: '03', label: 'Joinery (Wood/Alu/PVC)', labelFr: 'Menuiserie (Bois/Alu/PVC)', labelAr: 'النجارة' },
  { code: '04', label: 'Electrical', labelFr: 'Électricité', labelAr: 'الكهرباء' },
  { code: '05', label: 'Plumbing / HVAC', labelFr: 'Plomberie — Chauffage — Climatisation', labelAr: 'السباكة والتدفئة' },
  { code: '06', label: 'Painting / Glazing', labelFr: 'Peinture — Vitrerie', labelAr: 'الدهان والزجاج' },
  { code: '07', label: 'Roads & Networks (VRD)', labelFr: 'Voirie et Réseaux Divers (VRD)', labelAr: 'الطرق والشبكات' },
  { code: '08', label: 'Exterior / Green Areas', labelFr: 'Aménagements extérieurs / Espaces verts', labelAr: 'التهيئة الخارجية' },
];

export function isValidLotCode(code: string): boolean {
  return LOTS_BTPH.some((l) => l.code === code.padStart(2, '0'));
}
