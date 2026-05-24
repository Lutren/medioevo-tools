import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import { createRpgModeBridge } from "../rpg/rpgModeBridge";

describe("rpg/metroidvania bridge v1.3", () => {
  it("transitions city isometric mode to metroidvania scene with quests and dialogue", () => {
    const bridge = createRpgModeBridge(createCity());
    expect(bridge.cityLayer).toBe("isometric");
    expect(bridge.outsideCityLayer).toBe("metroidvania");
    expect(bridge.metroidvaniaScene.schema).toBe("duat/metroidvania-mode-scene/v1.3");
    expect(bridge.questRuntime.activeQuests.length).toBeGreaterThan(0);
    expect(bridge.npcDialogue.length).toBeGreaterThan(0);
  });
});
