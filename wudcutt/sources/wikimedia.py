from __future__ import annotations

import re

from .base import BaseSource
from ..models import SearchCandidate
from ..scoring import score_candidate


class WikimediaSource(BaseSource):
    provider = "wikimedia"
    API_URL = "https://commons.wikimedia.org/w/api.php"

    @staticmethod
    def _normalize_title_artist(raw_title: str) -> tuple[str, str]:
        clean_title = re.sub(r"\s*\([^)]*\)", "", raw_title)
        clean_title = re.sub(r"\.[a-zA-Z0-9]+$", "", clean_title).strip()
        clean_title = clean_title.replace("–", "-")
        artist = "Unknown"

        if " - " in clean_title:
            left, right = [part.strip() for part in clean_title.split(" - ", 1)]
            if len(left.split()) <= 4:
                artist = left
                clean_title = right

        if artist == "Unknown" and "," in clean_title:
            parts = [part.strip() for part in clean_title.split(",") if part.strip()]
            if len(parts) >= 2 and len(parts[0].split()) <= 4:
                artist = parts[0]
                clean_title = parts[1]

        clean_title = re.sub(r"\b(?:NGA|MET|BM|WGA)\s*\d.*$", "", clean_title).strip(" ,-_")
        clean_title = re.sub(r"\s*-\s*\d{3,4}(?:\.\d+)*\s*-\s*.*museum of art$", "", clean_title, flags=re.IGNORECASE).strip(" ,-_")
        clean_title = re.sub(r"\s*-\s*\d{3,4}(?:\.\d+)*$", "", clean_title).strip(" ,-_")
        return clean_title or raw_title, artist

    @staticmethod
    def _extract_year(title: str, categories: list[str]) -> str:
        category_text = " ".join(categories)
        category_match = re.search(r"\b(1[4-9][0-9]{2}|20[0-2][0-9])\b", category_text)
        if category_match:
            return category_match.group(1)

        lowered = title.lower()
        if any(marker in lowered for marker in ["museum", "nga", "met", "bm", "cleveland", "dp", "accession"]):
            return "unknown"

        title_match = re.search(r"\b(1[4-9][0-9]{2}|20[0-2][0-9])\b", title)
        if title_match:
            year = int(title_match.group(1))
            if year <= 1929:
                return str(year)
        return "unknown"

    def search(self, query: str) -> list[SearchCandidate]:
        payload = self._fixture_payload("wikimedia.json")
        if payload is None:
            response = self.session.get(
                self.API_URL,
                params={
                    "action": "query",
                    "generator": "search",
                    "gsrsearch": query,
                    "gsrnamespace": 6,
                    "prop": "imageinfo|categories",
                    "iiprop": "url|size|extmetadata",
                    "cllimit": 10,
                    "format": "json",
                },
                timeout=30,
            )
            response.raise_for_status()
            payload = response.json()
        pages = payload.get("query", {}).get("pages", {})
        results = []
        for page in pages.values():
            info = (page.get("imageinfo") or [{}])[0]
            extmetadata = info.get("extmetadata") or {}
            license_name = (extmetadata.get("LicenseShortName") or {}).get("value", "").strip().lower()
            if not license_name:
                continue
            if "public domain" not in license_name and license_name != "cc0":
                continue
            raw_title = page.get("title", "").replace("File:", "")
            categories = [item.get("title", "").replace("Category:", "") for item in page.get("categories", [])]
            clean_title, artist = self._normalize_title_artist(raw_title)
            year = self._extract_year(raw_title, categories)
            candidate = SearchCandidate(
                provider=self.provider,
                title=clean_title,
                artist=artist,
                year=year,
                medium="woodcut",
                source_institution="Wikimedia Commons",
                source_page_url=f"https://commons.wikimedia.org/wiki/{page.get('title', '')}",
                source_file_url=info.get("url", ""),
                preview_url=info.get("url", ""),
                license_label="cc0" if license_name == "cc0" else "public domain",
                license_reason=license_name,
                width=info.get("width"),
                height=info.get("height"),
                tags=[category.lower() for category in categories if category],
                notes="Candidate returned from Wikimedia Commons search",
            )
            results.append(score_candidate(candidate))
        return results
