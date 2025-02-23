import aiodns
import asyncio

class CacheSnooper(object):
    def __init__(self, domain, nameserver):
        self.domain = domain
        self.nameserver = nameserver
        self.resolver = aiodns.DNSResolver()

    async def check_cache(self):
        try:
            answers = await self.resolver.query(self.domain, 'A')
            return [answer.host for answer in answers]
        except:
            return None
