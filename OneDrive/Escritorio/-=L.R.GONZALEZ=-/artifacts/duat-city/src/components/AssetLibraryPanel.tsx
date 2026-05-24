import { createTileAtlas } from "../assets/tileAtlas";
import { createUiAtlas } from "../assets/uiAtlas";

export function AssetLibraryPanel() {
  const tileAtlas = createTileAtlas();
  const uiAtlas = createUiAtlas();
  const refs = [...Object.values(tileAtlas.refs), ...Object.values(uiAtlas.refs)];
  const reviewed = refs.filter(ref => ref.mode === "reviewed").length;
  return (
    <div className="section">
      <div className="section-title">Asset Library v1.2</div>
      <div className="scene-preview">
        <div><b>Mode:</b> procedural fallback</div>
        <div><b>Reviewed refs:</b> {reviewed}</div>
        <div><b>Fallback refs:</b> {refs.length - reviewed}</div>
        <div><b>Boundary:</b> INTERNAL_REVIEW_ONLY / publication false</div>
      </div>
    </div>
  );
}
