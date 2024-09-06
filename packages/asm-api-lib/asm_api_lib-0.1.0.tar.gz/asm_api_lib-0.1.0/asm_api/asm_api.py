# asm_api/asm_api.py
from typing import Optional, List

# POC method only:

class AsmApi:
    def __init__(self, domains: List[str]):
        self.verified_domains = domains

    def remove_domains(self, assets: Optional[List[dict]]):
        if assets is not None:
            for asset in assets:
                domain_to_remove: Optional[str] = asset.get("name")
                if domain_to_remove and domain_to_remove in self.verified_domains:
                    self.verified_domains.remove(domain_to_remove)
                    print(f"Removed domain: {domain_to_remove}")