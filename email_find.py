import re
import whois

# Regular expression pattern to search for email addresses
email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

# Read the list of sites to crawl from the file
with open('tocrawl.txt', 'r') as f:
    sites_to_crawl = [line.strip() for line in f]

# Loop through each site in the list and perform an ICANN lookup
for site in sites_to_crawl:
    print(f'Performing ICANN lookup on {site}...')

    # Perform the ICANN lookup
    try:
        domain_info = whois.whois(site)
    except Exception as e:
        print(f'Error: {e}')
        continue

    # Compile all the email addresses associated with the website
    emails = []
    if hasattr(domain_info, 'emails') and domain_info.emails:
        for email in domain_info.emails:
            email_match = re.search(email_pattern, email)
            if email_match:
                emails.append(email_match.group())

    # Write the email addresses to the output file
    with open('emails.txt', 'a') as f:
        f.write(f'Emails for {site}:\n')
        for email in emails:
            f.write(f' - {email}\n')

    # Print the email addresses
    print(f'Emails for {site}:')
    for email in emails:
        print(f' - {email}')
    print()
