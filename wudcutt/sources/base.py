from __future__ import annotations

import json
import os
from pathlib import Path

import requests


class BaseSource:
    provider: str = ""

    def __init__(self, session=None, fixture_dir: str | Path | None = None):
        self.session = session or requests.Session()
        if hasattr(self.session, "headers"):
            self.session.headers["User-Agent"] = os.getenv("WUDCUTT_USER_AGENT", "Wudcutt/0.1 (+https://github.com/trimad/Wudcutt)")
        self.fixture_dir = Path(fixture_dir) if fixture_dir else None

    def _fixture_payload(self, filename: str):
        if not self.fixture_dir:
            return None
        path = self.fixture_dir / filename
        if not path.exists():
            return None
        return json.loads(path.read_text())

    def search(self, query: str):
        raise NotImplementedError
