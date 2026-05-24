import type { AudioCue, AudioGameFeelConfig, ProceduralTonePlan } from "./audioTypes";
import { DEFAULT_AUDIO_GAMEFEEL_CONFIG } from "./audioTypes";
import { normalizeCue } from "./audioEventMapper";

export interface BrowserProceduralAudioAdapter {
  readonly enabled: boolean;
  readonly available: boolean;
  enable: () => Promise<boolean>;
  disable: () => void;
  playCue: (cue: AudioCue) => boolean;
  playCues: (cues: AudioCue[]) => number;
}

const OSCILLATOR_BY_SOURCE: Record<string, OscillatorType> = {
  material: "triangle",
  light: "sine",
  agent: "square",
  language: "sine",
  cosmology: "sawtooth",
  rpg: "triangle",
  ui: "sine",
  system: "sine",
};

export function createProceduralTonePlan(cue: AudioCue, seed = DEFAULT_AUDIO_GAMEFEEL_CONFIG.seed): ProceduralTonePlan {
  const safe = normalizeCue(cue);
  const hot = safe.kind.includes("fire") || safe.kind.includes("neon") || safe.kind.includes("block");
  const slow = safe.kind.includes("smoke") || safe.kind.includes("ruin") || safe.kind.includes("cosmology");
  const jitter = deterministicJitter(`${safe.id}:${seed}`);
  return {
    cueId: safe.id,
    oscillatorType: OSCILLATOR_BY_SOURCE[safe.source] ?? "sine",
    frequencyHz: round3(Math.max(20, Math.min(16000, safe.frequencyHz + jitter))),
    durationMs: safe.durationMs,
    gain: safe.gain,
    pan: safe.pan,
    attackMs: hot ? 4 : 12,
    decayMs: slow ? 90 : 40,
    releaseMs: slow ? 140 : 60,
    filterHz: round3(Math.max(80, Math.min(8200, safe.frequencyHz * (hot ? 5 : 3)))),
    deterministic: true,
  };
}

export function createBrowserProceduralAudioAdapter(config: AudioGameFeelConfig = DEFAULT_AUDIO_GAMEFEEL_CONFIG): BrowserProceduralAudioAdapter {
  let ctx: AudioContext | undefined;
  let enabled = false;

  const getAudioContextCtor = (): typeof AudioContext | undefined => {
    if (typeof window === "undefined") return undefined;
    return window.AudioContext ?? (window as Window & { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
  };

  const adapter: BrowserProceduralAudioAdapter = {
    get enabled() {
      return enabled;
    },
    get available() {
      return Boolean(getAudioContextCtor());
    },
    async enable() {
      const Ctor = getAudioContextCtor();
      if (!Ctor) return false;
      ctx = ctx ?? new Ctor();
      if (ctx.state === "suspended") await ctx.resume();
      enabled = true;
      return true;
    },
    disable() {
      enabled = false;
    },
    playCue(cue: AudioCue) {
      if (!enabled || !ctx) return false;
      scheduleCue(ctx, cue, config);
      return true;
    },
    playCues(cues: AudioCue[]) {
      let played = 0;
      for (const cue of cues.slice(0, config.maxCues)) {
        if (adapter.playCue(cue)) played++;
      }
      return played;
    },
  };
  return adapter;
}

function scheduleCue(ctx: AudioContext, cue: AudioCue, config: AudioGameFeelConfig): void {
  const plan = createProceduralTonePlan(cue, config.seed);
  const now = ctx.currentTime;
  const duration = plan.durationMs / 1000;
  const oscillator = ctx.createOscillator();
  const gain = ctx.createGain();
  const filter = ctx.createBiquadFilter();
  const panner = typeof ctx.createStereoPanner === "function" ? ctx.createStereoPanner() : undefined;

  oscillator.type = plan.oscillatorType;
  oscillator.frequency.setValueAtTime(plan.frequencyHz, now);
  filter.type = "lowpass";
  filter.frequency.setValueAtTime(plan.filterHz, now);
  gain.gain.setValueAtTime(0.0001, now);
  gain.gain.linearRampToValueAtTime(plan.gain * config.masterGain, now + plan.attackMs / 1000);
  gain.gain.exponentialRampToValueAtTime(Math.max(0.0001, plan.gain * config.masterGain * 0.3), now + Math.max(plan.attackMs, plan.decayMs) / 1000);
  gain.gain.exponentialRampToValueAtTime(0.0001, now + duration + plan.releaseMs / 1000);

  if (panner) {
    panner.pan.setValueAtTime(plan.pan, now);
    oscillator.connect(filter);
    filter.connect(gain);
    gain.connect(panner);
    panner.connect(ctx.destination);
  } else {
    oscillator.connect(filter);
    filter.connect(gain);
    gain.connect(ctx.destination);
  }
  oscillator.start(now);
  oscillator.stop(now + duration + plan.releaseMs / 1000 + 0.03);
}

function deterministicJitter(input: string): number {
  let hash = 0;
  for (let i = 0; i < input.length; i++) hash = (hash * 31 + input.charCodeAt(i)) | 0;
  return ((Math.abs(hash) % 17) - 8) * 0.125;
}

function round3(value: number): number {
  return Number(Number.isFinite(value) ? value.toFixed(3) : "0");
}
