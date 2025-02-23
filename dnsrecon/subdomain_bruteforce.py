import aiodns
import asyncio

class SubdomainBruteforcer(object):
    def __init__(self, domain, wordlist):
        self.domain = domain
        self.wordlist = wordlist
        self.resolver = aiodns.DNSResolver()

    async def _check_subdomain(self, subdomain):
        try:
            answers = await self.resolver.query(subdomain, 'A')
            return {subdomain:[answer.host for answer in answers]}
        except:
            return None

    async def bruteforce(self):
        tasks = [self._check_subdomain(f"{word}.{self.domain}") for word in self.wordlist]
        results = await asyncio.gather(*tasks)
        
        return [result for result in results if result]
