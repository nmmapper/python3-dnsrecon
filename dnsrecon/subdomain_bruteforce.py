import aiodns
import asyncio
from typing import List, Dict

class SubdomainBruteforcer(object):
    def __init__(self, domain:str, wordlist:List[str]):
        self.domain = domain
        self.wordlist = wordlist
        self.resolver = aiodns.DNSResolver()

    async def _check_subdomain(self, subdomain) -> Dict[str, str]:
        try:
            answers = await self.resolver.query(subdomain, 'A')
            return {
                "subdomain":subdomain, 
                "address":[answer.host for answer in answers],
                "host":self.domain
            }
        except:
            return None

    async def bruteforce(self) -> List[dict]:
        tasks = [self._check_subdomain(f"{word}.{self.domain}") for word in self.wordlist]
        results = await asyncio.gather(*tasks)
        
        return [result for result in results if result]
