/**
 * DUAT Physics + Light + Mechanics Engine v1.3.0
 * Fingerprint: DUAT-v1.3.0-PHYSICS-LIGHT-MECHANICS-CPU
 * 
 * Tipos unificados basados en MEDIOEVO/OSIT
 */

// Q-State unificado para audio, luz, física y mecánicas
export type QState = '00' | '01' | '10' | '11';

// Estado OSIT del observador (celda, NPC, agente)
export interface OSITState {
  state: QState;
  memory: Float32Array;      // memoria de estado previo
  calibration: number;       // factor de calibración 0-1
  noise: number;             // ruido estimado
  goal: string;              // objetivo operativo
  gate: 'APPROVE' | 'REVIEW' | 'BLOCK';
  lastUpdate: number;        // timestamp/frame
}

// Métricas de salud del sistema
export interface SystemMetrics {
  R: number;           // residuo 0-1
  Phi_eff: number;     // eficiencia 0-1
  J_c: number;         // umbral de jamming
  regime: 'OPTIMO' | 'SATURADO' | 'JAMMED' | 'CRITICO';
}

// Celda del mundo (física + luz + material)
export interface WorldCell {
  x: number;
  y: number;
  z?: number;
  material: MaterialType;
  osit: OSITState;
  physics: PhysicsState;
  light: LightState;
  audio?: AudioState;
}

// Materiales tipo Conway (estados discretos con reglas locales)
export type MaterialType = 
  | 'VOID' | 'STONE' | 'WATER' | 'FIRE' | 'SMOKE' 
  | 'METAL' | 'GLASS' | 'NEON' | 'STEAM' | 'ORGANIC';

// Estado físico de una celda
export interface PhysicsState {
  position: Vec2;
  prevPosition: Vec2;      // para Verlet
  velocity: Vec2;
  mass: number;
  restitution: number;     // coeficiente de restitución
  friction: number;
  solid: boolean;
  pressure: number;        // para fluidos
  temperature: number;     // para fuego/vapor
  active: boolean;         // si participa en sim este frame
}

export interface Vec2 {
  x: number;
  y: number;
}

// Estado lumínico
export interface LightState {
  emissive: number;        // 0-1, emite luz propia
  absorbtion: number;      // 0-1, absorbe luz
  transmission: number;    // 0-1, transmite luz
  receivedLux: number;     // lux recibido (acumulado)
  qLight: QState;          // estado lumínico Q
  color: RGB;              // color de emisión/absorción
}

export interface RGB {
  r: number; g: number; b: number;
}

// Estado de audio (bridge)
export interface AudioState {
  eventQueue: AudioEvent[];
  materialResonance: number;
}

export interface AudioEvent {
  type: string;
  intensity: number;
  qSource: QState;
  timestamp: number;
}

// Configuración del motor
export interface EngineConfig {
  gridSize: number;        // tamaño de celda en píxeles/unidades
  gridWidth: number;
  gridHeight: number;
  maxSubsteps: number;
  emlThreshold: number;    // umbral EML para cambio de régimen
  jammingThreshold: number; // J_c
  enableAudioBridge: boolean;
  enableLightBridge: boolean;
}
