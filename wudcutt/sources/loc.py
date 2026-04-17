from __future__ import annotations

from .base import BaseSource
from ..models import SearchCandidate
from ..scoring import score_candidate


class LibraryOfCongressSource(BaseSource):
    provider = "loc"
    API_URL = "https://www.loc.gov/photos/"

    def search(self, query: str) -> list[SearchCandidate]:
        payload = self._fixture_payload("loc.json")
        if payload is None:
            response = self.session.get(self.API_URL, params={"q": query, "fo": "json"}, timeout=30)
            response.raise_for_status()
            payload = response.json()
        candidates = []
        for item in payload.get("results", []):
            rights = ((item.get("item") or {}).get("rights") or "").lower()
            if not rights:
                continue
            if "no known restrictions" not in rights and "public domain" not in rights and "cc0" not in rights:
                continue
            image_urls = item.get("image_url") or []
            if not image_urls:
                continue
            candidate = SearchCandidate(
                provider=self.provider,
                title=item.get("title", "Untitled"),
                artist=", ".join(item.get("contributor_names") or []) or "Unknown",
                year=str(item.get("date") or "unknown"),
                medium="woodcut",
                source_institution="Library of Congress",
                source_page_url=item.get("url", ""),
                source_file_url=image_urls[0],
                preview_url=image_urls[0],
                license_label="public domain",
                license_reason=rights or "no known restrictions",
                tags=[str(tag).lower() for tag in item.get("subject") or []],
                notes="Candidate returned from Library of Congress search",
            )
            candidates.append(score_candidate(candidate))
        return candidates
