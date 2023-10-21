import dns.resolver
import concurrent.futures

def check_dmarc_record(domain):
    """
    Check the DMARC record for a given domain and return 'p=none' if p=none is present, 'No DMARC record' if there is no DMARC record, or False otherwise.
    """
    try:
        answers = dns.resolver.resolve('_dmarc.' + domain, 'TXT')
    except dns.resolver.NXDOMAIN:
        return 'No DMARC record'
    except dns.resolver.NoAnswer:
        return 'No Answer'
    except dns.resolver.LifetimeTimeout:
        return "LifetimeTimeout"
    for rdata in answers:
        for txt_string in rdata.strings:
            if 'p=none' in txt_string.decode():
                return 'p=none'
    return False

def check_dmarc_multi_threaded(websites):
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_website = {executor.submit(check_dmarc_record, website): website for website in websites}
        for future in concurrent.futures.as_completed(future_to_website):
            website = future_to_website[future]
            try:
                result = future.result()
            except Exception as e:
                result = str(e)
            results.append((website, result))
    return results

def main():
    """
    Main function to check the DMARC records of a list of websites and write any sites that contain p=none or have no DMARC record to an output file.
    """
    print("It takes around 30 seconds for the first results to appear.")
    with open('tocrawl.txt') as f:
        websites = [line.strip() for line in f]
    results = check_dmarc_multi_threaded(websites)
    with open('dmarc_output.txt', 'w') as f:
        for i, (website, result) in enumerate(results):
            print(f'In queue: {i + 1}/{len(websites)}')
            if result:
                f.write(f"{website}: {result}\n")
    print("Finished checking DMARC records.")

if __name__ == '__main__':
    main()
