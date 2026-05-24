# Audio Headed QA v1.3.2

Fingerprint: DUAT-v1.3.2-LOVABLE-ISO-EXTRACTION-VERMEER-LIGHT

Result:
- browserMode: Edge/CDP/headed-timeout-fallback
- focusStatus: unconfirmed
- enableButtonClicked: false
- previewButtonClicked: false
- perceptualAudio: AUDIO_HEADED_QA_NOT_AVAILABLE_TIMEOUT
- audioOffByDefault: true
- previewRequiresEnableFlag: true

Interpretation:
A headed Edge process was launched for local QA, but the CDP runner exceeded timeout before reliable interaction evidence. The fallback report is reproducible via tools/run-audio-headed-qa-v1_3_2.mjs and keeps the correct safety boundary: no autoplay, no external samples, no cloud, Wabi execution false.
