import aiodns
import asyncio

class ReverseLookup(object):
    def __init__(self, ip_range):
        self.ip_range = ip_range
        self.resolver = aiodns.DNSResolver()

    async def _reverse_lookup(self, ip):
        try:
            reverse_name = aiodns.reversename.from_address(ip)
            answers = await self.resolver.query(reverse_name, 'PTR')
            return ip, [answer.host for answer in answers]
        except:
            return ip, None

    async def perform_reverse_lookup(self):
        tasks = [self._reverse_lookup(ip) for ip in self.ip_range]
        results = await asyncio.gather(*tasks)
        return dict(results)
