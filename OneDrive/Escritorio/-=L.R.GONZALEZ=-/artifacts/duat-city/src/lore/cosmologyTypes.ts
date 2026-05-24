export type CosmologyBoundary = "IN_WORLD_COSMOLOGY" | "FORMAL_LAB" | "PUBLIC_CLAIM_BLOCKED";

export interface CosmologyConcept {
  id: string;
  label: string;
  mechanicUse: string[];
  loreText: string;
  boundary: CosmologyBoundary[];
}

export interface CosmologyProfile {
  schema: "duat/medioevo-cosmology/v1.3";
  concepts: CosmologyConcept[];
  publicClaimAllowed: false;
  scienceBoundaryNote: string;
}

export interface CosmologyQuestHook {
  id: string;
  title: string;
  mechanic: string;
  boundary: CosmologyBoundary[];
}
