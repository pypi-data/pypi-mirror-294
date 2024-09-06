# asm_api/asm_api.py
from typing import Optional, List

# POC method only:

class AsmApi:
    def __init__(self, domains: List[str]):
        self.verified_domains = domains

    def returns_a_domain(domain: str) -> str:
        print("🧪🧪 Calling AsmApi.return_a_domain()! 🧪🧪")
        return domain