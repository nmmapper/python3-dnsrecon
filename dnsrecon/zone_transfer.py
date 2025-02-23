import dns.zone
import dns.query

class ZoneTransfer(object):
    def __init__(self, domain, nameserver):
        self.domain = domain
        self.nameserver = nameserver

    def attempt_zone_transfer(self):
        try:
            zone = dns.zone.from_xfr(dns.query.xfr(self.nameserver, self.domain))
            return zone.nodes
        except Exception as e:
            return str(e)
