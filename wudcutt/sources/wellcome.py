from __future__ import annotations

from .base import BaseSource
from ..models import SearchCandidate
from ..scoring import score_candidate


class WellcomeSource(BaseSource):
    provider = "wellcome"
    API_URL = "https://api.wellcomecollection.org/catalogue/v2/works"

    def search(self, query: str) -> list[SearchCandidate]:
        payload = self._fixture_payload("wellcome.json")
        if payload is None:
            response = self.session.get(self.API_URL, params={"query": query}, timeout=30)
            response.raise_for_status()
            payload = response.json()
        candidates = []
        for item in payload.get("results", []):
            license_label = (((item.get("license") or {}).get("label")) or "").lower()
            if "public domain" not in license_label and "cc0" not in license_label:
                continue
            locations = (((item.get("images") or [{}])[0].get("locations") or [{}]))
            image_url = locations[0].get("url") if locations else ""
            if not image_url:
                continue
            contributors = item.get("contributors") or []
            productions = item.get("production") or []
            genres = [g.get("label", "").lower() for g in item.get("genres") or [] if g.get("label")]
            candidate = SearchCandidate(
                provider=self.provider,
                title=item.get("title", "Untitled"),
                artist=((((contributors[0] if contributors else {}).get("agent") or {}).get("label")) or "Unknown"),
                year=str((productions[0] if productions else {}).get("date") or "unknown"),
                medium="woodcut",
                source_institution="Wellcome Collection",
                source_page_url=((item.get("source") or {}).get("url") or f"https://wellcomecollection.org/works/{item.get('id', '')}"),
                source_file_url=image_url,
                preview_url=image_url,
                license_label="cc0" if "cc0" in license_label else "public domain",
                license_reason=license_label,
                tags=genres,
                notes=str(item.get("type") or "Candidate returned from Wellcome search"),
            )
            candidates.append(score_candidate(candidate))
        return candidates
