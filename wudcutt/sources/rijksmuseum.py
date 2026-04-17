from __future__ import annotations

import os

from .base import BaseSource
from ..models import SearchCandidate
from ..scoring import score_candidate


class RijksmuseumSource(BaseSource):
    provider = "rijksmuseum"
    API_URL = "https://www.rijksmuseum.nl/api/en/collection"

    def search(self, query: str) -> list[SearchCandidate]:
        payload = self._fixture_payload("rijksmuseum.json")
        if payload is None:
            api_key = os.getenv("RIJKSMUSEUM_API_KEY")
            if not api_key:
                raise RuntimeError("RIJKSMUSEUM_API_KEY is required for live Rijksmuseum searches")
            response = self.session.get(self.API_URL, params={"q": query, "imgonly": True, "ps": 20, "key": api_key}, timeout=30)
            response.raise_for_status()
            payload = response.json()
        candidates = []
        for item in payload.get("artObjects", []):
            web_image = item.get("webImage") or {}
            image_url = web_image.get("url")
            if not image_url:
                continue
            candidate = SearchCandidate(
                provider=self.provider,
                title=item.get("title", "Untitled"),
                artist=item.get("principalOrFirstMaker") or "Unknown",
                year=((item.get("dating") or {}).get("presentingDate") or "unknown"),
                medium="woodcut" if "print" in [x.lower() for x in item.get("objectTypes") or []] else "historical illustration",
                source_institution="Rijksmuseum",
                source_page_url=((item.get("links") or {}).get("web") or ""),
                source_file_url=image_url,
                preview_url=image_url,
                license_label="public domain",
                license_reason="Rijksmuseum open collection image",
                width=web_image.get("width"),
                height=web_image.get("height"),
                tags=[str(t).lower() for t in item.get("objectTypes") or []],
                notes="Candidate returned from Rijksmuseum search",
            )
            candidates.append(score_candidate(candidate))
        return candidates
