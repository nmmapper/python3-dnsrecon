import aiodns
import asyncio

class DNSEnumerator(object):
    def __init__(self, domain):
        self.domain = domain
        self.resolver = aiodns.DNSResolver()

    async def get_a_records(self):
        return await self._resolve_record('A')

    async def get_aaaa_records(self):
        return await self._resolve_record('AAAA')

    async def get_mx_records(self):
        return await self._resolve_record('MX')

    async def get_ns_records(self):
        return await self._resolve_record('NS')

    async def get_txt_records(self):
        return await self._resolve_record('TXT')

    async def get_cname_records(self):
        return await self._resolve_record('CNAME')

    async def get_soa_records(self):
        return await self._resolve_record('SOA')

    async def _resolve_record(self, record_type):
        try:
            answers = await self.resolver.query(self.domain, record_type)
            if(record_type == "TXT"):
                return [answer.text for answer in answers]
                
            elif(record_type == "SOA"):
                return [answers.nsname, answers.expires, answers.hostmaster, answers.serial]
                
            return [answer.host for answer in answers]
        except Exception as e:
            return str(e)
