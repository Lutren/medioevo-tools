import type { CityState } from "../core/types";
import type { AudioGameFeelConfig, AudioGameFeelSnapshot } from "./audioTypes";
import { DEFAULT_AUDIO_GAMEFEEL_CONFIG } from "./audioTypes";
import { createAudioGameFeelSnapshot, createMutedAudioGameFeelConfig } from "./gameFeelAdapter";
import { createBrowserProceduralAudioAdapter } from "./proceduralSynth";

export interface WorldAudioAdapter {
  snapshot: (state: CityState) => AudioGameFeelSnapshot;
  enable: () => Promise<boolean>;
  disable: () => void;
  preview: (state: CityState) => number;
  isEnabled: () => boolean;
  isAvailable: () => boolean;
}

export function createWorldAudioAdapter(config: Partial<AudioGameFeelConfig> = {}): WorldAudioAdapter {
  let runtimeConfig = createMutedAudioGameFeelConfig(config);
  const browser = createBrowserProceduralAudioAdapter(runtimeConfig);
  return {
    snapshot(state) {
      return createAudioGameFeelSnapshot(state, runtimeConfig);
    },
    async enable() {
      const ok = await browser.enable();
      runtimeConfig = createMutedAudioGameFeelConfig({ ...runtimeConfig, enabled: ok, mode: ok ? "runtime" : "off" });
      return ok;
    },
    disable() {
      browser.disable();
      runtimeConfig = createMutedAudioGameFeelConfig({ ...runtimeConfig, enabled: false, mode: "off" });
    },
    preview(state) {
      const snapshot = createAudioGameFeelSnapshot(state, runtimeConfig);
      return browser.playCues(snapshot.cues.slice(0, 6));
    },
    isEnabled() {
      return browser.enabled;
    },
    isAvailable() {
      return browser.available;
    },
  };
}

export { DEFAULT_AUDIO_GAMEFEEL_CONFIG };
