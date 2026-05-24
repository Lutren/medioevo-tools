/**
 * Light EML — Selector de Complejidad Lumínica
 * 
 * EML(lux_local, R_scene) decide complejidad por celda:
 * - EML bajo (compresión): luz ambient aproximada + un directional
 * - EML alto (expansión): propagación local + emissive + subsurface
 */

import { WorldCell } from '../types';
import { emlEvaluate } from '../core/eml';

export interface LightComplexity {
  mode: 'AMBIENT' | 'PROPAGATED' | 'FULL';
  steps: number;
  enableSubsurface: boolean;
  enableEmissive: boolean;
}

/**
 * Decide complejidad lumínica para una celda
 */
export function selectLightComplexity(
  cell: WorldCell,
  sceneResidue: number
): LightComplexity {
  const localComplexity = cell.light.emissive + cell.light.receivedLux;
  const eml = emlEvaluate(localComplexity, sceneResidue);

  if (eml.mode === 'COMPRESS') {
    return {
      mode: 'AMBIENT',
      steps: 1,
      enableSubsurface: false,
      enableEmissive: cell.light.emissive > 0.8
    };
  }

  if (eml.mode === 'EXPAND') {
    return {
      mode: 'FULL',
      steps: 4,
      enableSubsurface: cell.material === 'ORGANIC' || cell.material === 'WATER',
      enableEmissive: true
    };
  }

  return {
    mode: 'PROPAGATED',
    steps: 2,
    enableSubsurface: false,
    enableEmissive: cell.light.emissive > 0.5
  };
}
