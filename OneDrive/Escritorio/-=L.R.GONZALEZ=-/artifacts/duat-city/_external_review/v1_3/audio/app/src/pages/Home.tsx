// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Home Page — Landing de MEDIOEVO Audio
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

import { useNavigate } from 'react-router';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Activity, Cpu, Shield, Music, ArrowRight, Radio, Zap, Volume2 } from 'lucide-react';

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      {/* Hero */}
      <div className="relative overflow-hidden py-20 px-6">
        <div className="absolute inset-0 bg-gradient-to-br from-amber-950/20 via-zinc-950 to-zinc-950" />
        <div className="relative max-w-4xl mx-auto text-center">
          <div className="flex justify-center mb-4">
            <Activity className="w-16 h-16 text-amber-400" />
          </div>
          <h1 className="text-5xl font-bold tracking-tight mb-4">
            MEDIOEVO
          </h1>
          <p className="text-xl text-zinc-400 mb-2">
            Procedural Audio Engine
          </p>
          <p className="text-sm text-zinc-500 mb-8">
            v1.2.1 — DUAT — INTERNO_LOCAL — NO_PUBLICAR_SIN_GATE
          </p>
          <div className="flex justify-center gap-3">
            <Button
              onClick={() => navigate('/audio-engine')}
              className="bg-amber-600 hover:bg-amber-700 text-white px-6"
            >
              <Volume2 className="w-4 h-4 mr-2" />
              Open Audio Engine
              <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
          </div>
        </div>
      </div>

      <Separator className="bg-zinc-800" />

      {/* Features */}
      <div className="py-16 px-6">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-2xl font-semibold text-center mb-10">Arquitectura del Motor</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card className="border-zinc-800 bg-zinc-900">
              <CardHeader>
                <Cpu className="w-8 h-8 text-cyan-400 mb-2" />
                <CardTitle className="text-lg">CPU-First</CardTitle>
              </CardHeader>
              <CardContent className="text-sm text-zinc-400">
                Motor diseñado para correr en CPU sin depender de GPU/VRAM.
                Ideal para hardware limitado y FibMob LOD.
              </CardContent>
            </Card>

            <Card className="border-zinc-800 bg-zinc-900">
              <CardHeader>
                <Music className="w-8 h-8 text-purple-400 mb-2" />
                <CardTitle className="text-lg">Procedural 70%</CardTitle>
              </CardHeader>
              <CardContent className="text-sm text-zinc-400">
                70% sonido procedural en tiempo real desde materiales, física,
                luz, NPCs y estado del mundo.
              </CardContent>
            </Card>

            <Card className="border-zinc-800 bg-zinc-900">
              <CardHeader>
                <Shield className="w-8 h-8 text-emerald-400 mb-2" />
                <CardTitle className="text-lg">Local Only</CardTitle>
              </CardHeader>
              <CardContent className="text-sm text-zinc-400">
                Sin cloud, sin IA externa, sin descarga masiva de samples.
                WebAudio API puro con allowlist CC0/CC-BY.
              </CardContent>
            </Card>

            <Card className="border-zinc-800 bg-zinc-900">
              <CardHeader>
                <Radio className="w-8 h-8 text-amber-400 mb-2" />
                <CardTitle className="text-lg">12 Sonidos Base</CardTitle>
              </CardHeader>
              <CardContent className="text-sm text-zinc-400">
                Water, fire, smoke, neon, metal, glass, steam, archive,
                y 3 gates: approve, review, block.
              </CardContent>
            </Card>

            <Card className="border-zinc-800 bg-zinc-900">
              <CardHeader>
                <Zap className="w-8 h-8 text-orange-400 mb-2" />
                <CardTitle className="text-lg">Orchestral Engine</CardTitle>
              </CardHeader>
              <CardContent className="text-sm text-zinc-400">
                Cuerdas, bronces, coro, percusión sintética con motor
                de motivos, armonía y tensión procedural.
              </CardContent>
            </Card>

            <Card className="border-zinc-800 bg-zinc-900">
              <CardHeader>
                <Activity className="w-8 h-8 text-red-400 mb-2" />
                <CardTitle className="text-lg">OSIT Integration</CardTitle>
              </CardHeader>
              <CardContent className="text-sm text-zinc-400">
                Audio desde métricas R/Phi_eff, Q-state glyphs,
                y world state adapters para materiales y NPCs.
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      <Separator className="bg-zinc-800" />

      {/* Status */}
      <div className="py-8 px-6 text-center">
        <div className="flex justify-center gap-4 text-xs text-zinc-500">
          <Badge variant="outline" className="border-zinc-700 text-zinc-500">
            Wabi: execution_allowed=false
          </Badge>
          <Badge variant="outline" className="border-zinc-700 text-zinc-500">
            sandbox_execution_allowed=false
          </Badge>
          <Badge variant="outline" className="border-zinc-700 text-zinc-500">
            real_apply_allowed=false
          </Badge>
        </div>
      </div>

      {/* Footer */}
      <footer className="py-6 text-center text-xs text-zinc-700">
        <p>MEDIOEVO / OSIT — Lutren (tyr) — INTERNO_LOCAL</p>
        <p className="mt-1">Los datos persisten. El operador no. La continuidad se logra con estado externo.</p>
      </footer>
    </div>
  );
}
