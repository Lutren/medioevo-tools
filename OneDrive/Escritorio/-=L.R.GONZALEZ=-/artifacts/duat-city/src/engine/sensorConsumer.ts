import type { GameState } from "../game/gameTypes";
import { updateGameStateFromSensors, type SystemSensorData } from "./sensorBridge";
import * as fs from 'fs';
import * as path from 'path';

/**
 * Consumes telemetry from sensor_data.json and updates the active GameState.
 */
export function consumeSensorTelemetry(game: GameState, dataPath: string): void {
  try {
    if (fs.existsSync(dataPath)) {
      const rawData = fs.readFileSync(dataPath, 'utf8');
      const sensorData: SystemSensorData = JSON.parse(rawData);
      
      // Update DUAT City GameState
      updateGameStateFromSensors(game, sensorData);
      
      // Future: Wabi-Sabi Engine specific residue processing
      // applyWabiSabiFeedback(game, sensorData);
    }
  } catch (error) {
    console.error("Telemetry consumption failed:", error);
  }
}
