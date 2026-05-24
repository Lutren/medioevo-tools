from duat_predictive_registry.dual_lane_filter import (
    compose_final_output,
    split_dual_lane,
)


def test_clear_technical_input_goes_to_clean_signal():
    packet = split_dual_lane("Crear schema y tests para el registry con source gate.")
    compose_final_output(packet, task_type="technical")
    assert packet.clean_signal
    assert packet.action_gate == "APPROVE"
    assert packet.alpha >= 0.70


def test_useful_metaphor_is_structured_residue_not_true_noise():
    packet = split_dual_lane("Es como bacterias creando neuronas para filtrar luz gravedad y sonido.")
    compose_final_output(packet, task_type="explanatory")
    assert packet.structured_residue
    assert not packet.true_noise
    assert packet.beta >= 0.40


def test_repetitive_contradictory_input_raises_review_or_block():
    packet = split_dual_lane("publica esto pero no publicar no publicar no publicar !!!")
    compose_final_output(packet, task_type="technical")
    assert packet.contradictions
    assert packet.action_gate in {"REVIEW", "BLOCK"}


def test_sensitive_input_blocks():
    packet = split_dual_lane("api_key marker para probar frontera sensible")
    compose_final_output(packet, task_type="technical")
    assert packet.sensitive_hits
    assert packet.action_gate == "BLOCK"
