export const TILE_SIZE = 16;

export interface Camera {
  x: number;
  y: number;
  zoom: number;
}

export function defaultCamera(cityWidth: number, cityHeight: number): Camera {
  return {
    x: cityWidth / 2 - 15,
    y: cityHeight / 2 - 8,
    zoom: 1,
  };
}

export function worldToScreen(wx: number, wy: number, cam: Camera): { x: number; y: number } {
  return {
    x: (wx - cam.x) * TILE_SIZE * cam.zoom,
    y: (wy - cam.y) * TILE_SIZE * cam.zoom,
  };
}

export function screenToWorld(sx: number, sy: number, cam: Camera): { x: number; y: number } {
  return {
    x: sx / (TILE_SIZE * cam.zoom) + cam.x,
    y: sy / (TILE_SIZE * cam.zoom) + cam.y,
  };
}

export function screenToTile(sx: number, sy: number, cam: Camera): { x: number; y: number } {
  const w = screenToWorld(sx, sy, cam);
  return { x: Math.floor(w.x), y: Math.floor(w.y) };
}

export function panCamera(cam: Camera, dx: number, dy: number): Camera {
  return {
    ...cam,
    x: cam.x - dx / (TILE_SIZE * cam.zoom),
    y: cam.y - dy / (TILE_SIZE * cam.zoom),
  };
}

export function zoomCamera(cam: Camera, delta: number, cx: number, cy: number): Camera {
  const factor = delta > 0 ? 1.1 : 0.9;
  const newZoom = Math.max(0.3, Math.min(4, cam.zoom * factor));

  // Zoom toward cursor
  const wx = cx / (TILE_SIZE * cam.zoom) + cam.x;
  const wy = cy / (TILE_SIZE * cam.zoom) + cam.y;
  const newX = wx - cx / (TILE_SIZE * newZoom);
  const newY = wy - cy / (TILE_SIZE * newZoom);

  return { x: newX, y: newY, zoom: newZoom };
}

export function resetCamera(cityWidth: number, cityHeight: number): Camera {
  return defaultCamera(cityWidth, cityHeight);
}
