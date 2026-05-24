// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Audio Vibe Panel — Panel de vibecoding de audio
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

import { useState, useCallback } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Wand2, Sparkles, Music, CloudRain, Flame, BookOpen } from 'lucide-react';
import { getVibeParser } from '@/audio/audioVibeParser';
import { type AudioSceneConfig } from '@/audio/audioTypes';

const PRESETS = [
  { phrase: 'mas orquestal', icon: <Music className="w-4 h-4" /> },
  { phrase: 'mas lluvia', icon: <CloudRain className="w-4 h-4" /> },
  { phrase: 'mas fuego', icon: <Flame className="w-4 h-4" /> },
  { phrase: 'mas archivo prohibido', icon: <BookOpen className="w-4 h-4" /> },
  { phrase: 'menos musica mas ambiente', icon: <Sparkles className="w-4 h-4" /> },
  { phrase: 'mas jardin bioluminiscente', icon: <Sparkles className="w-4 h-4" /> },
  { phrase: 'mas vermeer silencioso', icon: <Music className="w-4 h-4" /> },
  { phrase: 'mas Caravaggio dramatico', icon: <Flame className="w-4 h-4" /> },
];

export function AudioVibePanel() {
  const [input, setInput] = useState('');
  const [lastResult, setLastResult] = useState<AudioSceneConfig | null>(null);
  const [history, setHistory] = useState<string[]>([]);

  const applyVibe = useCallback((phrase: string) => {
    const parser = getVibeParser();
    const result = parser.parse(phrase);

    if (result.matched) {
      setLastResult(result.config as AudioSceneConfig);
      setHistory(prev => [...prev.slice(-9), phrase]);
    }
  }, []);

  const handleSubmit = useCallback((e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    applyVibe(input);
    setInput('');
  }, [input, applyVibe]);

  const exportConfig = useCallback(() => {
    if (!lastResult) return;
    const json = JSON.stringify(lastResult, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'duat_audio_config.json';
    a.click();
    URL.revokeObjectURL(url);
  }, [lastResult]);

  return (
    <Card className="w-full max-w-md border border-zinc-700 bg-zinc-900 text-zinc-100">
      <CardHeader className="pb-3">
        <CardTitle className="text-lg font-semibold flex items-center gap-2">
          <Wand2 className="w-5 h-5 text-cyan-400" />
          Audio Vibecoding
        </CardTitle>
        <div className="text-xs text-zinc-400">
          Parser determinista — No IA externa — No cloud
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Input */}
        <form onSubmit={handleSubmit} className="flex gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="e.g., mas orquestal, mas lluvia..."
            className="bg-zinc-800 border-zinc-600 text-zinc-100"
          />
          <Button type="submit" className="bg-cyan-700 hover:bg-cyan-600">
            <Wand2 className="w-4 h-4" />
          </Button>
        </form>

        {/* Presets */}
        <div>
          <div className="text-xs text-zinc-400 mb-2">Presets</div>
          <div className="flex flex-wrap gap-1.5">
            {PRESETS.map((preset) => (
              <Button
                key={preset.phrase}
                variant="outline"
                size="sm"
                onClick={() => applyVibe(preset.phrase)}
                className="border-zinc-600 hover:bg-zinc-800 text-xs h-7"
              >
                {preset.icon}
                <span className="ml-1">{preset.phrase}</span>
              </Button>
            ))}
          </div>
        </div>

        <Separator className="bg-zinc-700" />

        {/* Result */}
        {lastResult && (
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-cyan-400">Configuración Generada</span>
              <Button variant="outline" size="sm" onClick={exportConfig} className="border-zinc-600 h-6 text-xs">
                Export JSON
              </Button>
            </div>
            <div className="bg-zinc-800 rounded p-2 text-xs space-y-1 font-mono">
              <div>Mood: <Badge variant="outline" className="text-xs">{lastResult.mood}</Badge></div>
              <div>Reverb: {lastResult.reverbProfile}</div>
              <div>Tension: {(lastResult.musicTension * 100).toFixed(0)}%</div>
              <div>SFX Density: {(lastResult.sfxDensity * 100).toFixed(0)}%</div>
              {lastResult.instruments && lastResult.instruments.length > 0 && (
                <div>Instr: {lastResult.instruments.join(', ')}</div>
              )}
              {lastResult.ambience && lastResult.ambience.length > 0 && (
                <div>Amb: {lastResult.ambience.join(', ')}</div>
              )}
            </div>
          </div>
        )}

        {/* History */}
        {history.length > 0 && (
          <>
            <Separator className="bg-zinc-700" />
            <div>
              <div className="text-xs text-zinc-400 mb-1">Historial</div>
              <div className="flex flex-wrap gap-1">
                {history.map((h, i) => (
                  <Badge key={i} variant="outline" className="text-xs border-zinc-600 cursor-pointer hover:bg-zinc-800"
                    onClick={() => applyVibe(h)}>
                    {h}
                  </Badge>
                ))}
              </div>
            </div>
          </>
        )}
      </CardContent>
    </Card>
  );
}
