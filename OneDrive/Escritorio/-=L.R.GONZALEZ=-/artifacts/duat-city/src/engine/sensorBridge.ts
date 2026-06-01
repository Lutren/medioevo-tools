import type { GameState } from "../game/gameTypes";

/**
 * SensorBridge translates real-world system sensor data into DUAT City environmental feedback.
 */
export interface SystemSensorData {
  thermalLoad: number; // Proxy for system stress
  wifiSignal: number;  // Proxy for environmental instability/topological mapping
  orientation: { pitch: number, roll: number, yaw: number };
}

export function updateGameStateFromSensors(game: GameState, sensors: SystemSensorData): void {
  // Translate thermal load to ecosystem temperature
  const envTemp = sensors.thermalLoad * 0.5 + 15; // Map to 15-65C range
  
  // Translate WiFi signal to "coherence interference"
  const coherenceImpact = (1 - sensors.wifiSignal) * 0.05;
  game.coherencePsi = Math.max(0, game.coherencePsi - coherenceImpact);

  // Future VR/AR integration: Apply orientation to camera state
  // game.camera.angle = sensors.orientation.yaw;
}
