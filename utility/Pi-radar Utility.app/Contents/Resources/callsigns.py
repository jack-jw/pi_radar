import csv
import re
import sys

# get requests library
try:
    import requests
except ImportError:
    print("Installing requests...")
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        import requests
    except Exception as e:
        print(f"Failed to install requests: {e}")
        sys.exit(1)

# get beautifulsoup4 library
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Installing beautifulsoup4...")
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])
        from bs4 import BeautifulSoup
    except Exception as e:
        print(f"Failed to install beautifulsoup4: {e}")
        sys.exit(1)

def extract_table_content(html_content):
    match = re.search('<table[^>]*>(.*?)</table>', html_content, re.DOTALL)
    if match:
        return match.group(1)

def html_to_csv(html_content, output_file):
    table_content = extract_table_content(html_content)

    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(table_content, 'html.parser')

    # Process the table_content as needed
    # For simplicity, let's write it to a CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Find all table rows
        rows = soup.find_all('tr')
        for row in rows:
            # Find all table cells in the row
            cells = row.find_all(['th', 'td'])

            # Extract text content from each cell
            columns = [cell.get_text(strip=True) for cell in cells]

            # Write the row to the CSV file
            writer.writerow(columns)

# Wikipedia link
wikipedia_link = "https://en.wikipedia.org/wiki/List_of_airline_codes"

# Fetch the HTML content from the Wikipedia link
response = requests.get(wikipedia_link)
html_content = response.text

# Define the output CSV file
output_csv_file = "/tmp/callsigns.csv"

# Convert HTML to CSV
html_to_csv(html_content, output_csv_file)

print(f"Conversion complete. CSV file saved at {output_csv_file}")
