from __future__ import annotations

from .base import BaseSource
from ..models import SearchCandidate
from ..scoring import score_candidate


class MetMuseumSource(BaseSource):
    provider = "metmuseum"
    SEARCH_URL = "https://collectionapi.metmuseum.org/public/collection/v1/search"
    OBJECT_URL = "https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"

    def search(self, query: str) -> list[SearchCandidate]:
        payload = self._fixture_payload("metmuseum-search.json")
        if payload is None:
            response = self.session.get(self.SEARCH_URL, params={"q": query, "hasImages": "true"}, timeout=30)
            response.raise_for_status()
            payload = response.json()
        object_ids = payload.get("objectIDs") or []
        candidates = []
        for object_id in object_ids[:10]:
            detail_payload = self._fixture_payload(f"metmuseum-{object_id}.json")
            if detail_payload is None:
                response = self.session.get(self.OBJECT_URL.format(object_id=object_id), timeout=30)
                response.raise_for_status()
                detail_payload = response.json()
            if not detail_payload.get("isPublicDomain"):
                continue
            primary_image = detail_payload.get("primaryImage", "")
            if not primary_image:
                continue
            tags = [item.get("term", "").lower() for item in (detail_payload.get("tags") or []) if item.get("term")]
            candidate = SearchCandidate(
                    provider=self.provider,
                    title=detail_payload.get("title", "Untitled"),
                    artist=detail_payload.get("artistDisplayName") or "Unknown",
                    year=detail_payload.get("objectDate") or "unknown",
                    medium=(detail_payload.get("medium") or "historical illustration").lower(),
                    source_institution=detail_payload.get("repository") or "The Metropolitan Museum of Art",
                    source_page_url=detail_payload.get("objectURL", ""),
                    source_file_url=primary_image,
                    preview_url=detail_payload.get("primaryImageSmall") or detail_payload.get("primaryImage", ""),
                    license_label="public domain",
                    license_reason="Met Open Access public domain object",
                    width=None,
                    height=None,
                    tags=tags,
                    notes=detail_payload.get("dimensions", "") or "Candidate returned from Met Museum search",
                )
            candidates.append(score_candidate(candidate))
        return candidates
