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

response = requests.get("https://speedbird.online/flightnumbers.php")

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all tables on the page
    tables = soup.find_all('table')

    # Check if there is a third table (flight numbers table)
    if len(tables) >= 3:
        table = tables[2]  # Select the third table (index 2)
        
        # Extract data from the table
        rows = table.find_all('tr')

        # Open a CSV file for writing
        with open('/tmp/routesBAW.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)

            # Write the header row if the table has one
            header_row = rows[0].find_all('th')
            if header_row:
                header = [header.text.strip() for header in header_row]
                csvwriter.writerow(header)

            # Write the data rows
            for row in rows[1:]:
                data = [cell.text.strip() for cell in row.find_all('td')]
                csvwriter.writerow(data)

        print("Data successfully scraped and saved to /tmp/routesBAW.csv.")
    else:
        print("The flight numbers table was not found.")
else:
    print(f"Failed to fetch the website. Status code: {response.status_code}")