# Color Theory Engine v1.0

The color engine lives in `src/color`.

## Implemented

- RGB to/from linear RGB.
- RGB to/from HSL.
- RGB to/from HSV.
- Approximate RGB to/from OKLab.
- Kelvin light temperature conversion.
- Warm/cold light blending.
- Day/night palette helper.
- Complementary, analogous, triadic, split-complementary and monochrome harmonies.
- Cinematic teal/amber and MEDIOEVO archeopunk profiles.
- Exposure, contrast, gamma, saturation, bloom threshold, shadow lift and highlight rolloff tone mapping.
- Bayer 4x4 and 8x8 ordered dithering.
- Deterministic palette quantization.

## Boundary

The pipeline is deterministic and local. It does not call AI, cloud services or external color APIs.
