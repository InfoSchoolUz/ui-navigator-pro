import requests

class AgentAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def health(self) -> dict:
        r = requests.get(self.base_url + "/health", timeout=10)
        r.raise_for_status()
        return r.json()

    def plan(self, payload: dict) -> dict:
        r = requests.post(self.base_url + "/plan", json=payload, timeout=60)
        r.raise_for_status()
        return r.json()