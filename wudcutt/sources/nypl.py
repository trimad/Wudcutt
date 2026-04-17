from __future__ import annotations

import os

from .base import BaseSource
from ..models import SearchCandidate
from ..scoring import score_candidate


class NYPLSource(BaseSource):
    provider = "nypl"
    API_URL = "https://api.repo.nypl.org/api/v2/items/search"

    def search(self, query: str) -> list[SearchCandidate]:
        payload = self._fixture_payload("nypl.json")
        if payload is None:
            token = os.getenv("NYPL_TOKEN")
            if not token:
                raise RuntimeError("NYPL_TOKEN is required for live NYPL searches")
            response = self.session.get(self.API_URL, params={"q": query}, timeout=30, headers={"Authorization": f"Token token={token}"})
            response.raise_for_status()
            payload = response.json()
        docs = ((payload.get("response") or {}).get("docs") or [])
        candidates = []
        for item in docs:
            image_id = item.get("imageID")
            if not image_id:
                continue
            preview_url = f"https://iiif.nypl.org/iiif/2/{image_id}/full/1000,/0/default.jpg"
            page_url = f"https://digitalcollections.nypl.org/items/{item.get('uuid', '')}"
            candidate = SearchCandidate(
                provider=self.provider,
                title=item.get("title", "Untitled"),
                artist=item.get("creatorLiteral") or "Unknown",
                year=str(item.get("date") or "unknown"),
                medium="woodcut",
                source_institution="New York Public Library",
                source_page_url=page_url,
                source_file_url=preview_url,
                preview_url=preview_url,
                license_label="public domain",
                license_reason="NYPL digital collections candidate",
                tags=[str(tag).lower() for tag in item.get("genre") or []],
                notes=str(item.get("typeOfResource") or "Candidate returned from NYPL search"),
            )
            candidates.append(score_candidate(candidate))
        return candidates
