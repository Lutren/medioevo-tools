from obs_info_kernel.math_canon import SCIENCE_CLAIM_GATE, classify_claim_math_status


def test_science_claim_gate_blocks_f5_closed_without_dataset():
    status = classify_claim_math_status("F5 queda cerrado y validado.")

    assert SCIENCE_CLAIM_GATE == "BLOCK_STRONG_CLAIMS_UNTIL_F1_F6"
    assert status["status"] == "ACTIVE_NEEDS_REVIEW"
    assert "dataset" in status["reason"]


def test_mu_f_is_not_allowed_as_physical_extractor_claim():
    status = classify_claim_math_status("mu_F extrae el noumeno y prueba nueva fisica validada")

    assert status["status"] == "BLOCKED_CLAIM"
    assert "BLOQUEO" in status["action"]


def test_canonical_math_language_stays_operational_only():
    status = classify_claim_math_status(
        {
            "R": "R_or = 1 - prod_i(1-r_i)",
            "Phi_moi": "(T*S*C*K*(1-R))^(1/5)",
            "boundary": "mathematical_proxy_only",
        }
    )

    assert status["status"] == "CANON_07B"
    assert status["action"] == "allowed as local operational math proxy"
