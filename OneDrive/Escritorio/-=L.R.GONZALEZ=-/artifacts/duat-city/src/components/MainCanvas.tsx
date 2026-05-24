import { useRef, useLayoutEffect, useCallback, useState } from "react";
import type { CityState, Mode, TileType } from "../core/types";
import type { GraphicsBudget, ViewMode } from "../graphics/types";
import type { PhysicsMetrics } from "../physics/types";
import type { SpriteResolver } from "../graphics/spriteResolver";
import type { PerformanceRenderCounters } from "../performance/performanceTypes";
import type { PixelRealismRuntime } from "../pixelRealism/pixelRealismMetrics";
import { Camera, TILE_SIZE, screenToTile, panCamera, zoomCamera } from "../render/camera";
import type { LODState } from "../render/lod-controller";
import { renderCity, type RenderOptions } from "../render/canvasRenderer";

interface MainCanvasProps {
  state: CityState;
  camera: Camera;
  lod: LODState;
  graphicsBudget?: GraphicsBudget;
  physicsMetrics?: PhysicsMetrics;
  mode: Mode;
  tool: TileType | "select" | "erase" | "scene";
  selectedId: string | null;
  showHeatmap: boolean;
  showFibmob: boolean;
  showAgentLabels: boolean;
  showPhysicsDebug: boolean;
  showChunkDebug: boolean;
  showQuaternaryDebug?: boolean;
  viewMode: ViewMode;
  spriteResolver?: SpriteResolver;
  pixelRealismRuntime?: PixelRealismRuntime;
  onRenderCounters?: (counters: PerformanceRenderCounters) => void;
  onViewportChange?: (width: number, height: number) => void;
  onCameraChange: (cam: Camera) => void;
  onTileClick: (x: number, y: number) => void;
  onSelect: (id: string | null) => void;
}

export function MainCanvas({
  state, camera, lod, graphicsBudget, physicsMetrics, mode, tool, selectedId,
  showHeatmap, showFibmob, showAgentLabels,
  showPhysicsDebug, showChunkDebug, showQuaternaryDebug, viewMode, spriteResolver, pixelRealismRuntime,
  onCameraChange, onTileClick, onSelect, onRenderCounters, onViewportChange,
}: MainCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [canvasVersion, setCanvasVersion] = useState(0);
  const dragRef = useRef({ dragging: false, startX: 0, startY: 0, lastX: 0, lastY: 0, moved: false });
  const camRef = useRef(camera);
  camRef.current = camera;

  // Resize canvas to fill container
  useLayoutEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const resize = () => {
      const previousWidth = canvas.width;
      const previousHeight = canvas.height;
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
      if (canvas.width !== previousWidth || canvas.height !== previousHeight) {
        setCanvasVersion(version => version + 1);
        onViewportChange?.(canvas.width, canvas.height);
      }
    };
    resize();
    const ro = new ResizeObserver(resize);
    ro.observe(canvas);
    return () => ro.disconnect();
  }, [onViewportChange]);

  // Render on every state/camera change
  useLayoutEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || canvas.width === 0) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    const opts: RenderOptions = {
      showHeatmap,
      showFibmob,
      showAgentLabels,
      selectedId,
      mode,
      graphicsBudget,
      physicsMetrics,
      showPhysicsDebug,
      showChunkDebug,
      showQuaternaryDebug,
      viewMode,
      spriteResolver,
      pixelRealismRuntime,
    };
    const counters = renderCity(ctx, state, camera, lod, opts);
    onRenderCounters?.(counters);
  }, [
    state,
    camera,
    lod,
    graphicsBudget,
    physicsMetrics,
    mode,
    selectedId,
    showHeatmap,
    showFibmob,
    showAgentLabels,
    showPhysicsDebug,
    showChunkDebug,
    showQuaternaryDebug,
    viewMode,
    spriteResolver,
    pixelRealismRuntime,
    canvasVersion,
    onRenderCounters,
  ]);

  const handleMouseDown = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    dragRef.current = {
      dragging: true,
      startX: e.clientX,
      startY: e.clientY,
      lastX: e.clientX,
      lastY: e.clientY,
      moved: false,
    };
  }, []);

  const handleMouseMove = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    const drag = dragRef.current;
    if (!drag.dragging) return;
    const dx = e.clientX - drag.lastX;
    const dy = e.clientY - drag.lastY;
    dragRef.current.lastX = e.clientX;
    dragRef.current.lastY = e.clientY;
    const totalDx = Math.abs(e.clientX - drag.startX);
    const totalDy = Math.abs(e.clientY - drag.startY);
    if (totalDx > 3 || totalDy > 3) dragRef.current.moved = true;

    // Only pan when dragging with select tool or right/middle button
    if (tool === "select" || dragRef.current.moved) {
      onCameraChange(panCamera(camRef.current, dx, dy));
    }
  }, [tool, onCameraChange]);

  const handleMouseUp = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    const drag = dragRef.current;
    const wasMoved = drag.moved;
    dragRef.current.dragging = false;
    dragRef.current.moved = false;

    if (wasMoved) return; // pan, not click

    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const sx = e.clientX - rect.left;
    const sy = e.clientY - rect.top;
    const { x, y } = screenToTile(sx, sy, camRef.current);

    if (tool === "select") {
      // Find agent or building at tile
      const agent = state.agents.find(a => Math.round(a.x) === x && Math.round(a.y) === y);
      if (agent) { onSelect(agent.id); return; }
      const tile = state.tiles[y * state.width + x];
      if (tile?.buildingId) { onSelect(tile.buildingId); return; }
      onSelect(null);
    } else if (tool === "scene") {
      onTileClick(x, y);
    } else {
      onTileClick(x, y);
    }
  }, [tool, state, onSelect, onTileClick]);

  const handleWheel = useCallback((e: React.WheelEvent<HTMLCanvasElement>) => {
    e.preventDefault();
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const cx = e.clientX - rect.left;
    const cy = e.clientY - rect.top;
    onCameraChange(zoomCamera(camRef.current, -e.deltaY, cx, cy));
  }, [onCameraChange]);

  return (
    <div className="canvas-area">
      <canvas
        ref={canvasRef}
        className="city-canvas"
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onWheel={handleWheel}
        style={{ cursor: tool === "select" ? "default" : "crosshair" }}
      />
      {viewMode !== "BEAUTIFUL" && (
        <div className="canvas-overlay">
          <span style={{ color: "#6e7681", fontSize: 10, background: "rgba(22,27,34,0.8)", padding: "2px 6px", borderRadius: 3 }}>
            Scroll: zoom · Drag: pan (select) · Click: build
          </span>
        </div>
      )}
    </div>
  );
}
