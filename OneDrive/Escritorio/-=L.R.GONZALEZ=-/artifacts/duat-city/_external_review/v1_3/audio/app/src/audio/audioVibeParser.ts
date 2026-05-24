// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Audio Vibe Parser — Parser determinista de frases vibe
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

import {
  type AudioSceneConfig,
  type MoodType,
  type ReverbProfile,
  type VibeParseResult,
} from './audioTypes';

/** Parser determinista de vibecoding para audio */
export class AudioVibeParser {
  private rules: Array<{
    patterns: string[];
    apply: () => Partial<AudioSceneConfig>;
  }> = [];

  constructor() {
    this.initRules();
  }

  private initRules(): void {
    // Volumen
    this.addRule(['mas silencioso', 'menos volumen', 'bajar'], () => ({
      mixLevels: { master: 0.3, music: 0.2, sfx: 0.2, ambience: 0.3 },
    }));
    this.addRule(['mas fuerte', 'mas volumen', 'subir'], () => ({
      mixLevels: { master: 0.9, music: 0.8, sfx: 0.9, ambience: 0.8 },
    }));

    // Orquestal
    this.addRule(['mas orquestal', 'orquesta', 'sinfonico'], () => ({
      musicTension: 0.6,
      instruments: ['strings', 'brass', 'choir', 'percussion'],
      mood: 'archive' as MoodType,
    }));

    // Ritual
    this.addRule(['mas ritual', 'ritual', 'sagrado', 'ceremonial'], () => ({
      musicTension: 0.7,
      instruments: ['choir', 'percussion', 'brass'],
      mood: 'ruin' as MoodType,
      reverbProfile: 'catacomb' as ReverbProfile,
    }));

    // Tensión
    this.addRule(['mas tension', 'tenso', 'suspenso', 'dramatico'], () => ({
      musicTension: 0.85,
      sfxDensity: 0.6,
      mood: 'gate_block' as MoodType,
    }));

    // Elementos naturales
    this.addRule(['mas lluvia', 'lluvia', 'agua'], () => ({
      ambience: ['waterFlow'],
      sfxDensity: 0.5,
      reverbProfile: 'water_surface' as ReverbProfile,
    }));
    this.addRule(['mas fuego', 'fuego', 'calor'], () => ({
      ambience: ['fireCrackle'],
      sfxDensity: 0.4,
      mood: 'forge' as MoodType,
      reverbProfile: 'stone_chamber' as ReverbProfile,
    }));

    // Locaciones
    this.addRule([
      'mas archivo prohibido', 'archivo', 'biblioteca', 'manuscrito',
    ], () => ({
      mood: 'archive' as MoodType,
      instruments: ['choir', 'glass', 'strings'],
      ambience: ['archiveMachine'],
      reverbProfile: 'catacomb' as ReverbProfile,
    }));
    this.addRule([
      'mas mercado subterraneo', 'mercado', 'bazaar',
    ], () => ({
      mood: 'market' as MoodType,
      instruments: ['percussion'],
      ambience: ['neonHum'],
      sfxDensity: 0.7,
      reverbProfile: 'metal_tunnel' as ReverbProfile,
    }));
    this.addRule([
      'mas jardin bioluminiscente', 'jardin', 'bioluminiscente',
    ], () => ({
      mood: 'garden' as MoodType,
      instruments: ['strings', 'bells'],
      ambience: ['waterFlow'],
      musicTension: 0.15,
      reverbProfile: 'dense_forest' as ReverbProfile,
    }));

    // Balance música/ambiente
    this.addRule(['menos musica', 'mas ambiente'], () => ({
      mixLevels: { music: 0.1, ambience: 0.8, sfx: 0.6 },
    }));
    this.addRule(['mas musica', 'menos ambiente'], () => ({
      mixLevels: { music: 0.8, ambience: 0.2, sfx: 0.3 },
    }));

    // Estilos artísticos
    this.addRule(['mas vermeer', 'vermeer', 'silencioso'], () => ({
      musicTension: 0.05,
      mixLevels: { master: 0.3, music: 0.1, sfx: 0.1, ambience: 0.4 },
      mood: 'silence' as MoodType,
    }));
    this.addRule(['mas caravaggio', 'caravaggio', 'dramatico'], () => ({
      musicTension: 0.9,
      mixLevels: { master: 0.85, music: 0.8, sfx: 0.6 },
      mood: 'gate_block' as MoodType,
      instruments: ['brass', 'percussion', 'strings'],
    }));
    this.addRule(['mas van eyck', 'van eyck', 'detallado'], () => ({
      musicTension: 0.3,
      sfxDensity: 0.6,
      instruments: ['strings', 'bells', 'choir'],
      mood: 'garden' as MoodType,
    }));
  }

  private addRule(
    patterns: string[],
    apply: () => Partial<AudioSceneConfig>
  ): void {
    this.rules.push({ patterns, apply });
  }

  /** Parsea frase de vibe */
  parse(input: string): VibeParseResult {
    const normalized = input
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9\s]/g, '')
      .trim();

    let matched = false;
    const result: Partial<AudioSceneConfig> = {
      instruments: [],
      ambience: [],
      sfxDensity: 0.3,
      musicTension: 0.3,
      reverbProfile: 'catacomb' as ReverbProfile,
      mixLevels: {},
      proceduralSeed: Date.now(),
      mood: 'archive' as MoodType,
    };

    for (const rule of this.rules) {
      for (const pattern of rule.patterns) {
        if (normalized.includes(pattern)) {
          const changes = rule.apply();
          Object.assign(result, changes);
          matched = true;

          // Merge arrays
          if (changes.instruments && result.instruments) {
            result.instruments = [...new Set([...result.instruments, ...changes.instruments])];
          }
          if (changes.ambience && result.ambience) {
            result.ambience = [...new Set([...result.ambience, ...changes.ambience])];
          }
          if (changes.mixLevels && result.mixLevels) {
            result.mixLevels = { ...result.mixLevels, ...changes.mixLevels };
          }
          break;
        }
      }
    }

    // If no match but input is not empty, return partial with low confidence
    if (!matched && normalized.length > 0) {
      result.proceduralSeed = Date.now();
    }

    return {
      matched,
      config: result,
      confidence: matched ? 0.8 + Math.random() * 0.2 : 0.1,
    };
  }

  /** Parsea múltiples frases */
  parseMultiple(inputs: string[]): VibeParseResult {
    const combined: Partial<AudioSceneConfig> = {
      instruments: [],
      ambience: [],
      mixLevels: {},
      proceduralSeed: Date.now(),
      mood: 'archive' as MoodType,
      reverbProfile: 'catacomb' as ReverbProfile,
      sfxDensity: 0.3,
      musicTension: 0.3,
    };

    let anyMatch = false;

    for (const input of inputs) {
      const result = this.parse(input);
      if (result.matched) {
        anyMatch = true;
        Object.assign(combined, result.config);
        if (result.config.instruments) {
          combined.instruments = [...new Set([...(combined.instruments || []), ...result.config.instruments])];
        }
        if (result.config.ambience) {
          combined.ambience = [...new Set([...(combined.ambience || []), ...result.config.ambience])];
        }
        if (result.config.mixLevels) {
          combined.mixLevels = { ...(combined.mixLevels || {}), ...result.config.mixLevels };
        }
      }
    }

    return {
      matched: anyMatch,
      config: combined,
      confidence: anyMatch ? 0.75 : 0.1,
    };
  }
}

/** Singleton del parser */
let parserInstance: AudioVibeParser | null = null;

export function getVibeParser(): AudioVibeParser {
  if (!parserInstance) {
    parserInstance = new AudioVibeParser();
  }
  return parserInstance;
}
