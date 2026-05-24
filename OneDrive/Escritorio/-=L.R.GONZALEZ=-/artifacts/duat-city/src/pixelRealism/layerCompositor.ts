export interface CompositorLayer {
  id: string;
  order: number;
  visible: boolean;
  hash: string;
}

export interface LayerCompositeResult {
  schema: "duat.layer_composite.v1_2";
  layerCount: number;
  visibleLayers: string[];
  compositeHash: string;
}

export function composeLayers(layers: CompositorLayer[]): LayerCompositeResult {
  const visible = layers.filter(layer => layer.visible).sort((a, b) => a.order - b.order);
  return {
    schema: "duat.layer_composite.v1_2",
    layerCount: layers.length,
    visibleLayers: visible.map(layer => layer.id),
    compositeHash: hash(visible.map(layer => `${layer.id}:${layer.hash}`).join("|")),
  };
}

function hash(value: string): string {
  let out = 5381;
  for (let i = 0; i < value.length; i++) out = ((out << 5) + out) ^ value.charCodeAt(i);
  return (out >>> 0).toString(16).padStart(8, "0");
}
