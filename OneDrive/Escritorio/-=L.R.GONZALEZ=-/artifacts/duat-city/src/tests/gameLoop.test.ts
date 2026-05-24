import { describe, expect, it } from "vitest";
import { createGameState } from "../game/gameState";
import { tickGame } from "../game/gameLoop";
import { saveGameState, loadGameState } from "../game/gameSave";
import { compileVibeAction } from "../vibecoding/vibeActionCompiler";

describe("game loop v1.2", () => {
  it("tick updates materials, lights and agents without NaN", () => {
    const game = createGameState();
    const next = tickGame(game, compileVibeAction("haz una calle lluviosa con neon y coloca agentes"));
    expect(next.scene.materials.length).toBeGreaterThan(0);
    expect(next.actors.length).toBeGreaterThan(0);
    expect(JSON.stringify(next)).not.toMatch(/NaN/);
  });

  it("save/load preserves scene", () => {
    const game = tickGame(createGameState(), compileVibeAction("haz un mercado subterraneo con luces rosas y humo"));
    const loaded = loadGameState(saveGameState(game));
    expect(loaded?.schema).toBe("duat.game_state.v1_2");
    expect(loaded?.scene.materials.length).toBe(game.scene.materials.length);
  });
});
