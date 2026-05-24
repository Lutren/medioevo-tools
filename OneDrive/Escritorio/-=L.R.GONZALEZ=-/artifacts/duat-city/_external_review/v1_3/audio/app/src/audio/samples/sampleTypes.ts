// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Sample Types — Tipos para biblioteca de samples
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

import { type SampleDescriptor, type SampleManifest } from '../audioTypes';
export type { SampleDescriptor, SampleManifest };

/** Estado de aprobación de sample */
export type SampleApprovalStatus = 'APPROVED' | 'REVIEW' | 'BLOCKED';

/** Registro de sample en memoria */
export interface SampleRegistryEntry extends SampleDescriptor {
  status: SampleApprovalStatus;
  loaded: boolean;
  lastVerified: string;
}

/** Política de licencias */
export interface LicensePolicy {
  cc0Preferred: boolean;
  ccByAllowed: boolean;
  ccByNcBlocked: boolean;
  unknownRequiresReview: boolean;
  noModelTraining: boolean;
  attributionRequired: boolean;
  publicationAllowed: boolean;
}

/** Default policy */
export const DefaultLicensePolicy: LicensePolicy = {
  cc0Preferred: true,
  ccByAllowed: true,
  ccByNcBlocked: true,
  unknownRequiresReview: true,
  noModelTraining: true,
  attributionRequired: true,
  publicationAllowed: false,
};
