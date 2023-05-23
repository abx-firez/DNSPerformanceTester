# Some Python DNS Performance Testing Code
# For Demonstration Purposes
import time
import dns.resolver

DNS_SERVERS = [ '8.8.8.8', # Google 
		 		'8.8.4.4',  # Google 
		 		'80.80.80.80', # Freenom World
				'1.1.1.1', # Cloudflare
				'1.0.0.1', # Cloudflare
				'9.9.9.9', # Quad9
				'208.67.222.222', # OpenDNS
				'87.118.100.175' # German Privacy Foundation e.V. 
			  ]
DOMAINS = ['google.de', 'google.com', 'amazon.de', 'amazon.com', 'hnu.de', 'golem.de', 'heise.de', 'github.com']

def measure_response_time(server, domain):
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [server]
        resolver.timeout = 1
        start = time.time()
        result = resolver.resolve(domain)
        end = time.time()
        response_time = end - start
    except dns.resolver.Timeout:
        response_time = -1
    except dns.resolver.NoAnswer:
        response_time = -1
    except dns.resolver.NXDOMAIN:
        response_time = -1
    except dns.resolver.NoNameservers:
        response_time = -1
    except Exception as e:
        response_time = -1
    return response_time

def main():
    results = []

    for server in DNS_SERVERS:
        avg_response_time = sum(measure_response_time(server, domain) for domain in DOMAINS) / len(DOMAINS)
        results.append([server, round(abs(avg_response_time), 4) * 1000])

    sorted_results = sorted(results, key=lambda x: x[1])

    print('Tested ', len(DOMAINS), ' domains for each DNS server:')

    for element in sorted_results:
        if element[1] >= 1000:
            print("{0:>20} -> TIMEOUT".format(element[0]))
        else:
            print("{0:>20} -> {1} ms".format(element[0], element[1]))
        
        
if __name__ == "__main__":
    main()