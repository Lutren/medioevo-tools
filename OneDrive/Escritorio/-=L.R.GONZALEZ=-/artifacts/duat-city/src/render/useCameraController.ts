import { useCallback, useState } from "react";
import type { Camera } from "./camera";
import type { ViewportSize } from "./cameraPresets";

export function useCameraController(initialCamera: Camera) {
  const [camera, setCamera] = useState<Camera>(initialCamera);
  const [viewport, setViewport] = useState<ViewportSize>({ width: 960, height: 720 });

  const updateViewport = useCallback((width: number, height: number) => {
    setViewport(prev => {
      if (prev.width === width && prev.height === height) return prev;
      return { width, height };
    });
  }, []);

  return { camera, setCamera, viewport, updateViewport };
}
