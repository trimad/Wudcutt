from __future__ import annotations

from dataclasses import replace

from .models import SearchCandidate


def score_candidate(candidate: SearchCandidate) -> SearchCandidate:
    score = 40
    reasons: list[str] = []

    if candidate.width and candidate.height:
        pixels = candidate.width * candidate.height
        if pixels >= 12_000_000:
            score += 25
            reasons.append("Excellent resolution for print")
        elif pixels >= 5_000_000:
            score += 15
            reasons.append("Strong resolution for print")
        elif pixels >= 2_000_000:
            score += 8
            reasons.append("Usable resolution")
        else:
            score -= 8
            reasons.append("Low resolution may limit print quality")
    else:
        score -= 5
        reasons.append("Resolution unknown")

    keyword_bonus_terms = {
        "woodcut", "engraving", "apocalypse", "horsemen", "death", "animal",
        "demon", "saint", "skeleton", "myth", "beast", "occult", "heraldry",
    }
    normalized_text = " ".join([candidate.title, candidate.notes, *candidate.tags]).lower()
    matched_terms = sorted(term for term in keyword_bonus_terms if term in normalized_text)
    if matched_terms:
        score += min(15, 5 + len(matched_terms) * 2)
        reasons.append(f"Commercially useful subject terms: {', '.join(matched_terms[:4])}")

    if candidate.preview_url:
        score += 3
        reasons.append("Preview image available")

    if candidate.license_label in {"public domain", "cc0"}:
        score += 7
        reasons.append("Explicit reusable rights metadata")

    score = max(0, min(100, score))
    if score >= 80:
        grade = "A"
    elif score >= 60:
        grade = "B"
    else:
        grade = "C"

    return replace(candidate, quality_score=score, quality_grade=grade, quality_reasons=reasons)
