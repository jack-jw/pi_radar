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

def extractTableContent(htmlContent):
    match = re.search('<table[^>]*>(.*?)</table>', htmlContent, re.DOTALL)
    if match:
        return match.group(1)

def htmlToCSV(htmlContent, outputFile):
    tableContent = extractTableContent(htmlContent)

    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(tableContent, 'html.parser')

    # Process the tableContent
    with open(outputFile, 'w', newline='', encoding='utf-8') as csvfile:
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

# Fetch the HTML content from the Wikipedia link
response = requests.get("https://en.wikipedia.org/wiki/List_of_airline_codes")
htmlContent = response.text

# Convert HTML to CSV
htmlToCSV(response.text, "/tmp/callsigns.csv")

print("Table successfully scraped and saved to /tmp/callsigns.csv.")