from pathlib import Path


FORBIDDEN_POSITIVE_PATTERNS = [
    ("duat", "pre" + "dice", "ele" + "cciones"),
    ("duat", "pre" + "dice", "vo" + "tos"),
    ("duat", "ran" + "kea", "vo" + "tantes"),
    ("duat", "prue" + "ba", "causa" + "lidad"),
    ("duat", "es", "ora" + "culo"),
    ("osit", "vali" + "dado", "fi" + "sica"),
    ("mercados", "predic" + "cion", "ver" + "dad"),
]


def test_docs_do_not_assert_forbidden_claims():
    root = Path(__file__).resolve().parents[1]
    allowed_context = ("bloque", "blocked", "no ", "not ", "forbidden", "boundary")
    for path in root.rglob("*"):
        if path.suffix.lower() not in {".md", ".json", ".py"}:
            continue
        if ".pytest_cache" in str(path) or path.name == "test_no_forbidden_claims.py":
            continue
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            low = line.lower()
            for tokens in FORBIDDEN_POSITIVE_PATTERNS:
                if all(token in low for token in tokens):
                    assert any(marker in low for marker in allowed_context), (path, line)
