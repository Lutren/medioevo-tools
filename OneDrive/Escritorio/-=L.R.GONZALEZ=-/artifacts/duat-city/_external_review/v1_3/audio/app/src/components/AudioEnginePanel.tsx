// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Audio Engine Panel — Panel principal del motor
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

import { useState, useEffect, useCallback } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Separator } from '@/components/ui/separator';
import { Volume2, VolumeX, Power, Activity, Gauge, AlertTriangle } from 'lucide-react';
import { getAudioEngine } from '@/audio/audioEngine';
import { type AudioMetrics, type AudioHealthReport } from '@/audio/audioTypes';

export function AudioEnginePanel() {
  const engine = getAudioEngine();
  const [enabled, setEnabled] = useState(false);
  const [metrics, setMetrics] = useState<AudioMetrics>(engine.getMetrics());
  const [health, setHealth] = useState<AudioHealthReport>(engine.getHealthReport());
  const [activeTest, setActiveTest] = useState<string | null>(null);

  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics(engine.getMetrics());
      setHealth(engine.getHealthReport());
    }, 100);
    return () => clearInterval(interval);
  }, [engine]);

  const handleEnable = useCallback(async () => {
    const ok = await engine.enable();
    if (ok) setEnabled(true);
  }, [engine]);

  const handleDisable = useCallback(() => {
    engine.disable();
    setEnabled(false);
    setActiveTest(null);
  }, [engine]);

  const playTestSound = useCallback(async (sound: string) => {
    if (!enabled) await handleEnable();
    setActiveTest(sound);

    const ctx = engine.getContext();
    if (!ctx) return;

    const synth = await import('@/audio/synthesis');
    const se = new synth.SynthesisEngine(ctx);

    let node: GainNode | null = null;
    switch (sound) {
      case 'water': node = se.waterFlow(0.3); break;
      case 'fire': node = se.fireCrackle(0.3); break;
      case 'neon': node = se.neonHum(0.2); break;
      case 'gate_approve': node = se.gateApprove(0.3); break;
      case 'gate_review': node = se.gateReview(0.3); break;
      case 'gate_block': node = se.gateBlock(0.3); break;
      case 'archive': {
        const orch = await import('@/audio/orchestra');
        const oe = new orch.OrchestraEngine(ctx);
        node = oe.playMood('archive', 0.3);
        break;
      }
      case 'forge': {
        const orch = await import('@/audio/orchestra');
        const oe = new orch.OrchestraEngine(ctx);
        node = oe.playMood('forge', 0.3);
        break;
      }
    }

    if (node) {
      node.connect(ctx.destination);
      setTimeout(() => {
        node?.disconnect();
        setActiveTest(null);
      }, 3000);
    }
  }, [enabled, engine, handleEnable]);

  return (
    <Card className="w-full max-w-2xl border border-zinc-700 bg-zinc-900 text-zinc-100">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg font-semibold flex items-center gap-2">
            <Activity className="w-5 h-5 text-amber-400" />
            DUAT Procedural Audio Engine
          </CardTitle>
          <Badge
            variant={enabled ? 'default' : 'secondary'}
            className={enabled ? 'bg-emerald-600' : 'bg-zinc-700'}
          >
            {enabled ? 'ACTIVE' : 'STANDBY'}
          </Badge>
        </div>
        <div className="text-xs text-zinc-400 mt-1">
          v1.2.1 — WebAudio API — CPU-first — Local only
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Enable/Disable */}
        <div className="flex gap-2">
          {!enabled ? (
            <Button
              onClick={handleEnable}
              className="bg-amber-600 hover:bg-amber-700 text-white"
            >
              <Power className="w-4 h-4 mr-2" />
              Enable Audio
            </Button>
          ) : (
            <Button
              onClick={handleDisable}
              variant="destructive"
            >
              <VolumeX className="w-4 h-4 mr-2" />
              Disable Audio
            </Button>
          )}
        </div>

        <Separator className="bg-zinc-700" />

        {/* Métricas */}
        <div className="space-y-3">
          <div className="flex items-center justify-between text-sm">
            <span className="text-zinc-400 flex items-center gap-1">
              <Activity className="w-4 h-4" /> Active Voices
            </span>
            <span className="font-mono">{metrics.activeVoices} / 32</span>
          </div>
          <Progress value={(metrics.activeVoices / 32) * 100} className="h-2" />

          <div className="grid grid-cols-2 gap-3">
            <div>
              <div className="text-xs text-zinc-400 flex items-center gap-1">
                <Gauge className="w-3 h-3" /> R_audio
              </div>
              <div className="font-mono text-lg">{metrics.R_audio.toFixed(3)}</div>
            </div>
            <div>
              <div className="text-xs text-zinc-400 flex items-center gap-1">
                <Gauge className="w-3 h-3" /> Phi_audio
              </div>
              <div className="font-mono text-lg">{metrics.Phi_audio.toFixed(3)}</div>
            </div>
            <div>
              <div className="text-xs text-zinc-400">CPU Estimate</div>
              <div className="font-mono text-sm">{(metrics.cpuEstimate * 100).toFixed(1)}%</div>
            </div>
            <div>
              <div className="text-xs text-zinc-400">Dropped Voices</div>
              <div className="font-mono text-sm">{metrics.droppedVoices}</div>
            </div>
          </div>

          {metrics.clippingDetected && (
            <div className="flex items-center gap-2 text-red-400 text-sm">
              <AlertTriangle className="w-4 h-4" />
              Clipping detected
            </div>
          )}
        </div>

        <Separator className="bg-zinc-700" />

        {/* Test Sounds */}
        <div>
          <div className="text-sm font-medium mb-2 text-zinc-300">Test Sounds</div>
          <div className="flex flex-wrap gap-2">
            {[
              { id: 'water', label: 'Water', icon: '💧' },
              { id: 'fire', label: 'Fire', icon: '🔥' },
              { id: 'neon', label: 'Neon', icon: '⚡' },
              { id: 'gate_approve', label: 'Gate OK', icon: '✓' },
              { id: 'gate_review', label: 'Gate Review', icon: '◐' },
              { id: 'gate_block', label: 'Gate Block', icon: '✕' },
              { id: 'archive', label: 'Archive', icon: '📜' },
              { id: 'forge', label: 'Forge', icon: '🔨' },
            ].map((s) => (
              <Button
                key={s.id}
                variant="outline"
                size="sm"
                disabled={!enabled && s.id !== 'water'}
                onClick={() => playTestSound(s.id)}
                className={`border-zinc-600 hover:bg-zinc-800 text-xs ${
                  activeTest === s.id ? 'bg-amber-900/50 border-amber-600' : ''
                }`}
              >
                <Volume2 className="w-3 h-3 mr-1" />
                {s.label}
              </Button>
            ))}
          </div>
        </div>

        <Separator className="bg-zinc-700" />

        {/* Health Report */}
        <div className="text-xs space-y-1">
          <div className="flex justify-between">
            <span className="text-zinc-400">Gate:</span>
            <Badge
              variant="outline"
              className={`text-xs ${
                health.gate === 'APPROVE' ? 'border-emerald-600 text-emerald-400' :
                health.gate === 'REVIEW' ? 'border-amber-600 text-amber-400' :
                'border-red-600 text-red-400'
              }`}
            >
              {health.gate}
            </Badge>
          </div>
          <div className="flex justify-between">
            <span className="text-zinc-400">User Gesture:</span>
            <span className={health.userGestureRequired ? 'text-red-400' : 'text-emerald-400'}>
              {health.userGestureRequired ? 'Required' : 'Received'}
            </span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
