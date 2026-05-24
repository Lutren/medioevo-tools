// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Sample Manifest — Manifesto de samples revisados
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

import { type SampleManifest, type SampleDescriptor } from './sampleTypes';

/** Versión del manifest */
const MANIFEST_VERSION = 'v1_2_1';

/** Crea manifest vacío */
export function createEmptyManifest(): SampleManifest {
  return {
    version: MANIFEST_VERSION,
    samples: [],
    lastUpdated: new Date().toISOString(),
    publicationAllowed: false,
  };
}

/** Crea manifest con placeholders de ejemplo */
export function createPlaceholderManifest(): SampleManifest {
  return {
    version: MANIFEST_VERSION,
    samples: [
      createPlaceholder('water_drip_01', 'Water drip', ['water', 'ambient']),
      createPlaceholder('fire_crackle_01', 'Fire crackle', ['fire', 'ambient']),
      createPlaceholder('metal_hit_01', 'Metal hit', ['metal', 'impact']),
      createPlaceholder('glass_break_01', 'Glass break', ['glass', 'impact']),
      createPlaceholder('step_stone_01', 'Stone step', ['footstep', 'stone']),
    ],
    lastUpdated: new Date().toISOString(),
    publicationAllowed: false,
  };
}

function createPlaceholder(id: string, name: string, tags: string[]): SampleDescriptor {
  return {
    id,
    name,
    sourceUrl: 'https://example.com/placeholder',
    author: 'PLACEHOLDER',
    license: 'UNKNOWN',
    sha256: '0000000000000000000000000000000000000000000000000000000000000000',
    tags,
    duration: 1.0,
    approved: false,
  };
}

/** Valida un manifest */
export function validateManifest(manifest: SampleManifest): {
  valid: boolean;
  errors: string[];
} {
  const errors: string[] = [];

  if (!manifest.version) {
    errors.push('Missing version');
  }

  if (!manifest.lastUpdated) {
    errors.push('Missing lastUpdated');
  }

  for (const sample of manifest.samples) {
    if (!sample.id) errors.push(`Sample missing id`);
    if (!sample.sourceUrl) errors.push(`Sample ${sample.id} missing sourceUrl`);
    if (!sample.author) errors.push(`Sample ${sample.id} missing author`);
    if (!sample.license) errors.push(`Sample ${sample.id} missing license`);
    if (!sample.sha256 || sample.sha256.length !== 64) {
      errors.push(`Sample ${sample.id} invalid sha256`);
    }
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}

/** Exporta manifest a JSON */
export function exportManifestToJSON(manifest: SampleManifest): string {
  return JSON.stringify(manifest, null, 2);
}
