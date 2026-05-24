# SPRITE_LIGHTING_PIPELINE_OPTIONS

## Que si puede lograrse bien

- Sprites 2D con normal maps reaccionando a luces locales.
- Height maps simples para volumen aparente.
- SDF/contorno para rim light y sombras suaves.
- Layered cutout: cabeza, torso, brazos, piernas con z-order.
- Pseudo eje Z por capas y offsets.
- Contact shadows bajo pies/objetos.
- Iluminacion direccional dramatica sin modelo 3D completo.

## Limitaciones

- No hay self-shadowing 3D real.
- Rotaciones fuertes revelan planitud.
- Normales generadas automaticamente pueden fallar en ropa/caras.
- Articulacion anatomica exige metadata de pivotes/joints.
- CPU Canvas puede hacer version barata; calidad alta requiere shader/WebGL.

## Pipeline recomendado

Low tier:
- Albedo sprite atlas.
- Mask/contour SDF por sprite.
- Luz por sprite usando muestra central + rim/contact shadow.
- Sin normal map obligatorio.

Mid tier:
- Albedo + normal map + height map.
- Layered cutout con pivotes.
- Light sampling por capas.

High tier:
- WebGL shader per sprite.
- Normal/depth/occlusion maps.
- Pseudo-Z stack por articulacion.
- Shadow blob deformado por direccion de luz.

## Mejor balance calidad/rendimiento

Para DUAT ahora:
1. Layered cutout + SDF contour.
2. Normal map opcional por atlas.
3. Pseudo-Z por metadata de partes.
4. WebGL solo como backend high tier.

Esto evita crear modelos 3D completos y mantiene el target web ligero.

