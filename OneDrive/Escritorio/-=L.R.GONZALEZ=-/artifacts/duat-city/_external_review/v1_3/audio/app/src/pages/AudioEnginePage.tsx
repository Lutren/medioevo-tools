// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Audio Engine Page — Página principal del motor
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

import { AudioEnginePanel } from '@/components/AudioEnginePanel';
import { AudioMixerPanel } from '@/components/AudioMixerPanel';
import { AudioVibePanel } from '@/components/AudioVibePanel';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Activity, Cpu, Shield, Music } from 'lucide-react';

export default function AudioEnginePage() {
  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 p-6">
      {/* Header */}
      <header className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <Activity className="w-8 h-8 text-amber-400" />
          <h1 className="text-3xl font-bold tracking-tight">
            MEDIOEVO Procedural Audio Engine
          </h1>
        </div>
        <p className="text-zinc-400 text-sm mb-3">
          Motor de audio procedural para DUAT — WebAudio API — CPU-first — Local only
        </p>
        <div className="flex flex-wrap gap-2">
          <Badge variant="outline" className="border-amber-600 text-amber-400 text-xs">
            <Cpu className="w-3 h-3 mr-1" /> CPU-first
          </Badge>
          <Badge variant="outline" className="border-emerald-600 text-emerald-400 text-xs">
            <Shield className="w-3 h-3 mr-1" /> Local only
          </Badge>
          <Badge variant="outline" className="border-purple-600 text-purple-400 text-xs">
            <Music className="w-3 h-3 mr-1" /> Procedural
          </Badge>
          <Badge variant="outline" className="border-cyan-600 text-cyan-400 text-xs">
            v1.2.1
          </Badge>
          <Badge variant="outline" className="border-zinc-600 text-zinc-400 text-xs">
            Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
          </Badge>
        </div>
      </header>

      <Separator className="bg-zinc-800 mb-8" />

      {/* Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 max-w-6xl">
        <div className="space-y-6">
          <AudioEnginePanel />
        </div>
        <div className="space-y-6">
          <AudioMixerPanel />
          <AudioVibePanel />
        </div>
      </div>

      {/* Footer */}
      <footer className="mt-12 text-center text-xs text-zinc-600">
        <Separator className="bg-zinc-800 mb-4" />
        <p>DUAT Procedural Audio Engine v1.2.1 — INTERNO_LOCAL — NO_PUBLICAR_SIN_GATE</p>
        <p className="mt-1">MEDIOEVO / OSIT — Wabi execution: false — No cloud — No IA externa</p>
      </footer>
    </div>
  );
}
