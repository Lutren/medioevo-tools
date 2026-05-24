/**
 * Tests Light: LightFieldFM, QStateLight, LightBridge
 */

import { LightFieldFM } from '../src/light/lightFieldFM';
import { computeLightProfile } from '../src/light/qStateLight';
import { LightAudioBridge } from '../src/light/lightBridge';
import { WorldCell } from '../src/types';

function makeLightCell(x: number, y: number, material: string, emissive: number, q: any): WorldCell {
  return {
    x, y, material: material as any,
    osit: { state: '10', memory: new Float32Array(4), calibration: 0.5, noise: 0.1, goal: 'survive', gate: 'APPROVE', lastUpdate: 0 },
    physics: { position: {x, y}, prevPosition: {x, y}, velocity: {x:0, y:0}, mass: 1, restitution: 0.5, friction: 0.3, solid: true, pressure: 0, temperature: 20, active: true },
    light: { emissive, absorbtion: 0.3, transmission: 0.5, receivedLux: 0, qLight: q, color: {r:128,g:128,b:128} }
  };
}

describe('LightFieldFM', () => {
  test('propagate increases lux near emitter', () => {
    const field = new LightFieldFM(10, 10, 32, { maxPropagationSteps: 2, attenuationBase: 0.8, enableQState: true });
    const cells = [makeLightCell(160, 160, 'NEON', 1.0, '11')];
    field.propagate(cells);
    field.applyToCells(cells);
    expect(cells[0].light.receivedLux).toBeGreaterThan(0);
  });

  test('Q-state propagation changes with neighbors', () => {
    const field = new LightFieldFM(10, 10, 32, { maxPropagationSteps: 2, attenuationBase: 0.8, enableQState: true });
    const cells = [
      makeLightCell(160, 160, 'NEON', 1.0, '11'),
      makeLightCell(192, 160, 'STONE', 0, '00')
    ];
    field.propagate(cells);
    field.applyToCells(cells);
    expect(['00', '01', '10', '11']).toContain(cells[1].light.qLight);
  });
});

describe('QStateLight', () => {
  test('computeLightProfile returns valid color', () => {
    const cell = makeLightCell(0, 0, 'FIRE', 0.5, '11');
    const profile = computeLightProfile(cell);
    expect(profile.color.r).toBeGreaterThan(0);
    expect(profile.lux).toBeGreaterThanOrEqual(0);
  });

  test('glass distorts color', () => {
    const cell = makeLightCell(0, 0, 'GLASS', 0.5, '10');
    cell.physics.pressure = 2;
    const profile = computeLightProfile(cell);
    expect(profile.color.r).not.toBe(128); // debería estar distorsionado
  });
});

describe('LightAudioBridge', () => {
  test('detects Q transition', () => {
    const bridge = new LightAudioBridge();
    const cells = [makeLightCell(0, 0, 'STONE', 0, '00')];
    bridge.process(cells, 1);
    cells[0].light.qLight = '11';
    const events = bridge.process(cells, 2);
    expect(events.length).toBeGreaterThan(0);
    expect(events[0].event.type).toContain('burst');
  });
});
