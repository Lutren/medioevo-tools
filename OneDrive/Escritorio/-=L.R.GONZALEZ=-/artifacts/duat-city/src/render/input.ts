import { panCamera, zoomCamera, screenToTile, Camera } from "./camera";

export interface InputState {
  isDragging: boolean;
  lastX: number;
  lastY: number;
  mouseX: number;
  mouseY: number;
}

export function makeInputState(): InputState {
  return { isDragging: false, lastX: 0, lastY: 0, mouseX: 0, mouseY: 0 };
}

export function handleMouseDown(
  e: MouseEvent | React.MouseEvent,
  input: InputState,
  tool: string
): InputState {
  if (tool === "select" || e.button === 1 || e.button === 2) {
    return { ...input, isDragging: true, lastX: e.clientX, lastY: e.clientY };
  }
  return input;
}

export function handleMouseMove(
  e: MouseEvent | React.MouseEvent,
  input: InputState,
  cam: Camera,
  onPan: (cam: Camera) => void
): InputState {
  const newInput = { ...input, mouseX: e.clientX, mouseY: e.clientY };
  if (input.isDragging) {
    const dx = e.clientX - input.lastX;
    const dy = e.clientY - input.lastY;
    onPan(panCamera(cam, dx, dy));
    return { ...newInput, lastX: e.clientX, lastY: e.clientY };
  }
  return newInput;
}

export function handleMouseUp(input: InputState): InputState {
  return { ...input, isDragging: false };
}

export function handleWheel(
  e: WheelEvent | React.WheelEvent,
  cam: Camera,
  canvasRect: DOMRect,
  onZoom: (cam: Camera) => void
): void {
  e.preventDefault?.();
  const cx = e.clientX - canvasRect.left;
  const cy = e.clientY - canvasRect.top;
  onZoom(zoomCamera(cam, -e.deltaY, cx, cy));
}
