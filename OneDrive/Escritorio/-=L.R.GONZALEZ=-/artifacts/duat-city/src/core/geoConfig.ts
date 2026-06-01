export type PlaneType = "base" | "medio" | "astral" | "nexus";

export type RegionType = 
  | "entrernia" 
  | "sanguisburg" 
  | "control" 
  | "farming_coast" 
  | "astral_central" 
  | "viking_north"
  | "nexus_cafe";

export type GeoProperties = {
  name: string;
  loreDescription: string;
  technologicalLevel: number; // 0-10
  hazardLevel: number; // 0-10
  plane: PlaneType;
};

export const GEO_CONFIG: Record<RegionType, GeoProperties> = {
  // Plano Medio (Ciclo 3)
  entrernia: { name: "Entrernia", loreDescription: "Futurista, superplaneada.", technologicalLevel: 9, hazardLevel: 2, plane: "medio" },
  sanguisburg: { name: "Sanguisburg", loreDescription: "Colina, valle de montañas.", technologicalLevel: 5, hazardLevel: 6, plane: "medio" },
  control: { name: "Ciudad Control", loreDescription: "Estética industrial latina.", technologicalLevel: 6, hazardLevel: 7, plane: "medio" },
  farming_coast: { name: "Costa y Granjas", loreDescription: "Granjas y pescadores.", technologicalLevel: 3, hazardLevel: 4, plane: "medio" },
  bunker_4444: { name: "Búnker 4444", loreDescription: "Conexión Plano Base.", technologicalLevel: 8, hazardLevel: 9, plane: "medio" },
  // Plano Astral
  astral_central: { name: "Ciudad Central (Astral)", loreDescription: "Núcleo tecnológico/cosmológico.", technologicalLevel: 10, hazardLevel: 1, plane: "astral" },
  viking_north: { name: "Norte Vikingo", loreDescription: "Castillos, resistencia.", technologicalLevel: 4, hazardLevel: 8, plane: "astral" },
  vaquero_south: { name: "Sur Vaquero", loreDescription: "Tierra de forajidos.", technologicalLevel: 3, hazardLevel: 7, plane: "astral" },
  samurai_east: { name: "Este Samurai", loreDescription: "Honor y dragones.", technologicalLevel: 5, hazardLevel: 6, plane: "astral" },
  wolf_west: { name: "Oeste Lobos", loreDescription: "Ninjas y naturaleza.", technologicalLevel: 4, hazardLevel: 6, plane: "astral" },
  // Nexus
  nexus_cafe: { name: "Le Jardin (Nexus)", loreDescription: "Convergencia fuera del tiempo.", technologicalLevel: 0, hazardLevel: 0, plane: "nexus" },
};
