from __future__ import annotations

from .base import BaseSource
from ..models import SearchCandidate
from ..scoring import score_candidate


class InternetArchiveSource(BaseSource):
    provider = "internet_archive"
    API_URL = "https://archive.org/advancedsearch.php"
    METADATA_URL = "https://archive.org/metadata/{identifier}"

    def _metadata_payload(self, identifier: str):
        payload = self._fixture_payload(f"internet_archive-{identifier}.json")
        if payload is not None:
            return payload
        response = self.session.get(self.METADATA_URL.format(identifier=identifier), timeout=30)
        response.raise_for_status()
        return response.json()

    def _choose_image_url(self, identifier: str, metadata_payload: dict) -> str:
        files = metadata_payload.get("files") or []
        for file_info in files:
            name = str(file_info.get("name") or "")
            format_name = str(file_info.get("format") or "").lower()
            if name.lower().endswith((".jpg", ".jpeg", ".png", ".tif", ".tiff")) or "jpg" in format_name or "png" in format_name:
                return f"https://archive.org/download/{identifier}/{name}"
        return ""

    def search(self, query: str) -> list[SearchCandidate]:
        payload = self._fixture_payload("internet_archive.json")
        if payload is None:
            response = self.session.get(
                self.API_URL,
                params={"q": query, "fl[]": ["identifier", "title", "creator", "year", "rights", "subject"], "output": "json"},
                timeout=30,
            )
            response.raise_for_status()
            payload = response.json()
        docs = ((payload.get("response") or {}).get("docs") or [])
        candidates = []
        for item in docs:
            rights = str(item.get("rights") or "").lower()
            if not rights:
                continue
            if "public domain" not in rights and "cc0" not in rights:
                continue
            identifier = item.get("identifier")
            if not identifier:
                continue
            metadata_payload = self._metadata_payload(identifier)
            image_url = self._choose_image_url(identifier, metadata_payload)
            if not image_url:
                continue
            page_url = f"https://archive.org/details/{identifier}"
            subjects = item.get("subject") or []
            if isinstance(subjects, str):
                subjects = [subjects]
            candidate = SearchCandidate(
                provider=self.provider,
                title=item.get("title", "Untitled"),
                artist=item.get("creator") or "Unknown",
                year=str(item.get("year") or "unknown"),
                medium="woodcut",
                source_institution="Internet Archive",
                source_page_url=page_url,
                source_file_url=image_url,
                preview_url=image_url,
                license_label="cc0" if "cc0" in rights else "public domain",
                license_reason=rights,
                tags=[str(tag).lower() for tag in subjects],
                notes="Candidate returned from Internet Archive search",
            )
            candidates.append(score_candidate(candidate))
        return candidates
