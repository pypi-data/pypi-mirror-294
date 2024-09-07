from typing import Any, Dict, List, Optional
from urllib.parse import urlencode
import json
import requests


class ASMDomainAPI:
    """Make a variety of ASM Api calls and functions, depending on apiTarget"""

    def __init__(
        self,
        api_url: str,  # like https://asm-dev.netspi.com/api
        api_target: str,
        api_key: str,
        client_id: str,
    ) -> None:
        self.api_target: str = api_target
        self.api_url: str = api_url
        self.api_key: str = api_key
        self.client_id: str = client_id
        self.headers = {}


        # IMPORTANT: Custom handling for LEGACY_ASM vs PLATFORM_ASM!
        if api_target == "PLATFORM_ASM":
            # self.domain_url = ""  # Not implemented
            # self.verify_assets_url = ""  # Not in use
            self.attack_surface_url = f"{self.api_url}/assets/surface"
            self.verify_assets_url = f"{self.api_url}/assets/verify"

            self.headers = {
                "x-app-name": "ASM-Root-Domain-Redirect",
                "Authorization": f"Token {self.api_key}",
            }
            self.verify_asm_assets = (
                # TODO: Change this back to v2, testing it out right now...
                
                self.verify_asm_assets_v2
            )  # E.g., skip verification!
            self.submit_assets_to_attack_surface = (
                self.submit_assets_to_attack_surface_v2
            )
        else:  # LEGACY_ASM, None, etc
            # self.domain_url = f"{self.api_url}/asset/domain" # NOT IN USE
            self.verify_assets_url = f"{self.api_url}/asset/ip/verify"
            self.attack_surface_url = f"{self.api_url}/surface"
            self.headers = {
                "Content-Type": "application/json",
                "Monster": self.api_key,
            }
            self.verify_asm_assets = self.verify_asm_assets_v1
            self.submit_assets_to_attack_surface = (
                self.submit_assets_to_attack_surface_v1
            )

    def verify_asm_assets_v1(self, domains: List[str]) -> List[Dict[str, Any]]:
        param: Dict[str, str] = {"c": self.client_id}

        print(f"🙆 Verifying domains: {domains} \n")

        encoded_param: str = urlencode(param)

        url_with_param: str = self.verify_assets_url + "?" + encoded_param

        payload: Dict[str, List[Dict[str, Dict[str, str]]]] = {
            "assets": self.convert_domains_to_verify_payload(domains),
        }

        verified_domains: List[str] = []
        verified_domains.extend(domains)

        try:
            print(f"Request({self.api_target}): /PUT {url_with_param} {payload}")
            response: requests.Response = requests.put(
                url_with_param,
                json=payload,
                headers=self.headers,
            )
            print(
                f"/{response.request.method} {response.request.url} {response.status_code}"
            )

            data: Dict[str, Any] = response.json()

            assets: Optional[List[Dict[str, Any]]] = data.get("assets")

            print(assets)

            if assets is not None:
                for asset in assets:
                    domain_to_remove: Optional[str] = asset.get("name")
                    if domain_to_remove and domain_to_remove in domains:
                        verified_domains.remove(domain_to_remove)
                        print(f"Removed domain: {domain_to_remove}")

        except Exception as e:
            print('Error:', e)

        return verified_domains

    def verify_asm_assets_v2(self, domains: List[str]) -> List[Dict[str, Any]]:                                                           
      param: Dict[str, str] = {"c": self.client_id}

      print(f"🙆🙆🙆 Verifying domains: {domains} \n")

      encoded_param: str = urlencode(param)

      url_with_param: str = self.verify_assets_url + "?" + encoded_param

      payload: Dict[str, List[Dict[str, Dict[str, str]]]] = {
          "assets": self.convert_domains_to_verify_payload(domains),
      }

      payload["clientId"] = self.client_id

      verified_domains: List[str] = []
      verified_domains.extend(domains)

      try:
          print(f"Request({self.api_target}): /PUT {url_with_param} {payload}")
          response: requests.Response = requests.put(
              url_with_param,
              json=payload,
              headers=self.headers,
          )
          print(
              f"/{response.request.method} {response.request.url} {response.status_code}"
          )

          data: Dict[str, Any] = response.json()

          assets: Optional[List[Dict[str, Any]]] = data.get("assets")

          print(assets)

          if assets is not None:
              for asset in assets:
                  domain_to_remove: Optional[str] = asset.get("name")
                  if domain_to_remove and domain_to_remove in domains:
                      verified_domains.remove(domain_to_remove)
                      print(f"Removed domain: {domain_to_remove}")

      except Exception as e:
          print('Error:', e)

      return verified_domains    
        # """PLATFORM_ASM skips the verify_asm_assets API entirely"""
        # print("WARNING: No asset verification performed!")
        # return domains

    def submit_assets_to_attack_surface_v1(self, payload):
        # LEGACY_ASM requires clientId in the requestParameters...
        param: Dict[str, str] = {"c": self.client_id}
        encoded_param: str = urlencode(param)
        url_with_param: str = self.attack_surface_url + "?" + encoded_param

        print(f"Request({self.api_target}): /PUT {url_with_param} {payload}")
        response: requests.Response = requests.put(
            url_with_param, json=payload, headers=self.headers
        )
        print(
            f"/{response.request.method} {response.request.url} {response.status_code}"
        )

        return response

    def submit_assets_to_attack_surface_v2(self, payload):
        # PLATFORM_ASM requires clientId in the JSON body...
        payload["clientId"] = self.client_id

        print(f"Request({self.api_target}): /PUT {self.attack_surface_url} {payload}")
        response: requests.Response = requests.put(
            url=self.attack_surface_url, json=payload, headers=self.headers
        )
        print(
            f"/{response.request.method} {response.request.url} {response.status_code}"
        )
        return response

    def add_asm_domains(
        self, domain_id: int, domains: List[str], attribution: str
    ) -> None:
        
        print(f"Adding domains to ASM: {domains}")

        payload: Dict[str, Any] = self.convert_domains_to_add_payload(
            domain_id, domains, attribution
        )

        print("payload below: ")
        print(payload)

        try:
            # will call submit_assets_to_attack_surface v1 or v2
            response = self.submit_assets_to_attack_surface(payload)
            response.raise_for_status()

        except requests.exceptions.RequestException as error:
            print(f"Error message: {error}")
            response_text: Optional[str] = getattr(response, "text", None)
            if response_text:
                print(response_text)

    @staticmethod
    def convert_domains_to_add_payload(
        domain_id: int, domains: List[str], attribution: str
    ) -> Dict[str, Any]:

        converted_domains: List[Dict[str, Dict[str, Any]]] = [
            {"domain": {"name": domain, "monitored": True}} for domain in domains
        ]
        print(f"converted_domains: {converted_domains}")
        return {
            "attribution": attribution,
            "attributionSourceId": domain_id,
            "attributionSourceType": "DOMAIN",
            "assets": converted_domains,
        }

    @staticmethod
    def convert_domains_to_verify_payload(
        domains: List[str],
    ) -> List[Dict[str, Dict[str, str]]]:
        return [{"domain": {"name": domain}} for domain in domains]