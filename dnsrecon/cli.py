import argparse
import asyncio
from .dns_enum import DNSEnumerator
from .zone_transfer import ZoneTransfer
from .subdomain_bruteforce import SubdomainBruteforcer
from .reverse_lookup import ReverseLookup
from .cache_snooping import CacheSnooper
from .utils import load_wordlist, save_to_json, save_to_csv, save_to_xml

async def main():
    parser = argparse.ArgumentParser(description="DNSRecon - Modular DNS Enumeration Tool")
    parser.add_argument("-d", "--domain", help="Target domain")
    parser.add_argument("-t", "--type", help="Type of scan (enum, axfr, brt, rev, cache)")
    parser.add_argument("-w", "--wordlist", help="Path to wordlist for bruteforcing")
    parser.add_argument("-r", "--range", help="IP range for reverse lookup")
    parser.add_argument("-o", "--output", help="Output format (json, csv, xml)")
    args = parser.parse_args()

    if args.type == "enum":
        enumerator = DNSEnumerator(args.domain)
        results = {
            "A": await enumerator.get_a_records(),
            "AAAA": await enumerator.get_aaaa_records(),
            "MX": await enumerator.get_mx_records(),
            "NS": await enumerator.get_ns_records(),
            "TXT": await enumerator.get_txt_records(),
            "CNAME": await enumerator.get_cname_records(),
            "SOA": await enumerator.get_soa_records(),
        }
        print(results)
        if args.output:
            save_results(results, args.output)

    elif args.type == "axfr":
        transfer = ZoneTransfer(args.domain, args.nameserver)
        results = transfer.attempt_zone_transfer()
        print("Zone Transfer Results:", results)
        if args.output:
            save_results(results, args.output)

    elif args.type == "brt":
        wordlist = load_wordlist(args.wordlist)
        bruteforcer = SubdomainBruteforcer(args.domain, wordlist)
        results = await bruteforcer.bruteforce()
        print("Found Subdomains:", results)
        if args.output:
            save_results(results, args.output)

    elif args.type == "rev":
        reverse = ReverseLookup(args.range)
        results = await reverse.perform_reverse_lookup()
        print("Reverse Lookup Results:", results)
        if args.output:
            save_results(results, args.output)

    elif args.type == "cache":
        snooper = CacheSnooper(args.domain, args.nameserver)
        results = await snooper.check_cache()
        print("Cache Snooping Results:", results)
        if args.output:
            save_results(results, args.output)

def save_results(data, format):
    if format == "json":
        save_to_json(data, "results.json")
    elif format == "csv":
        save_to_csv(data, "results.csv")
    elif format == "xml":
        save_to_xml(data, "results.xml")
    else:
        print("Unsupported output format.")

if __name__ == "__main__":
    asyncio.run(main())
