// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Audio Mixer Panel — Panel de mezcla multi-bus
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

import { useState, useCallback } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Slider } from '@/components/ui/slider';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Volume2, VolumeX, Headphones } from 'lucide-react';
import { getAudioEngine } from '@/audio/audioEngine';
import { type AudioBusName } from '@/audio/audioTypes';

const BUSES: { name: AudioBusName; label: string; color: string }[] = [
  { name: 'master', label: 'Master', color: 'bg-amber-600' },
  { name: 'music', label: 'Music', color: 'bg-purple-600' },
  { name: 'ambience', label: 'Ambience', color: 'bg-cyan-600' },
  { name: 'sfx', label: 'SFX', color: 'bg-orange-600' },
  { name: 'ui', label: 'UI', color: 'bg-blue-600' },
  { name: 'npc', label: 'NPC', color: 'bg-emerald-600' },
  { name: 'material', label: 'Material', color: 'bg-yellow-600' },
  { name: 'danger', label: 'Danger', color: 'bg-red-600' },
];

export function AudioMixerPanel() {
  const engine = getAudioEngine();
  const [levels, setLevels] = useState<Record<string, number>>({
    master: 0.8, music: 0.6, ambience: 0.7, sfx: 0.9,
    ui: 1.0, npc: 0.75, material: 0.8, danger: 1.0,
  });
  const [mutes, setMutes] = useState<Record<string, boolean>>({});

  const handleLevelChange = useCallback((bus: AudioBusName, value: number[]) => {
    const v = value[0] / 100;
    setLevels(prev => ({ ...prev, [bus]: v }));
    engine.setBusGain(bus, v);
  }, [engine]);

  const toggleMute = useCallback((bus: AudioBusName) => {
    setMutes(prev => {
      const newMutes = { ...prev, [bus]: !prev[bus] };
      engine.setBusMute(bus, newMutes[bus]);
      return newMutes;
    });
  }, [engine]);

  const muteAll = useCallback(() => {
    engine.muteAll();
    setMutes(Object.fromEntries(BUSES.map(b => [b.name, true])));
  }, [engine]);

  const unmuteAll = useCallback(() => {
    engine.unmuteAll();
    setMutes({});
  }, [engine]);

  return (
    <Card className="w-full max-w-md border border-zinc-700 bg-zinc-900 text-zinc-100">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg font-semibold flex items-center gap-2">
            <Headphones className="w-5 h-5 text-purple-400" />
            Audio Mixer
          </CardTitle>
          <div className="flex gap-1">
            <Button variant="outline" size="sm" onClick={muteAll} className="border-zinc-600 h-7 px-2">
              <VolumeX className="w-3 h-3" />
            </Button>
            <Button variant="outline" size="sm" onClick={unmuteAll} className="border-zinc-600 h-7 px-2">
              <Volume2 className="w-3 h-3" />
            </Button>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-3">
        {BUSES.map((bus) => (
          <div key={bus.name} className="space-y-1">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${bus.color}`} />
                <span className="text-sm capitalize w-20">{bus.label}</span>
                <Badge variant="outline" className="text-xs border-zinc-600 font-mono">
                  {(levels[bus.name] * 100).toFixed(0)}%
                </Badge>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => toggleMute(bus.name)}
                className={`h-6 w-6 p-0 ${mutes[bus.name] ? 'text-red-400' : 'text-zinc-400'}`}
              >
                {mutes[bus.name] ? <VolumeX className="w-3 h-3" /> : <Volume2 className="w-3 h-3" />}
              </Button>
            </div>
            <Slider
              value={[levels[bus.name] * 100]}
              onValueChange={(v) => handleLevelChange(bus.name, v)}
              max={100}
              step={1}
              disabled={mutes[bus.name]}
              className="cursor-pointer"
            />
          </div>
        ))}

        <Separator className="bg-zinc-700" />

        {/* Master info */}
        <div className="flex justify-between text-xs text-zinc-400">
          <span>Buses: {BUSES.length}</span>
          <span>Compressor: ON</span>
        </div>
      </CardContent>
    </Card>
  );
}
