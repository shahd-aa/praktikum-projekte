import requests
from bs4 import BeautifulSoup
import json

# Fetch URL
url = "https://www.dwd.de/DE/leistungen/klimadatendeutschland/statliste/statlex_html.html;jsessionid=E1D047C421FA29EB8FA59B318ED088F6.live11054?view=nasPublication&nn=16102"
response = requests.get(url)
print(f"checkpoint 1: response {response.status_code}")

# Check if the response is successful
if response.status_code == 200:
    print(f"checkpoint 2: page fetched successfully!")

    # Parse the page content
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")

    # Check for table
    if table:
        print(f"checkpoint 3: table found!")

        # Extract all rows (skip the header row)
        rows = table.find_all("tr")[1:]
        print(f"checkpoint 4: rows extracted, found {len(rows)} rows!")

        # Empty list to store row data
        filled_rows = []

        # Loop through each row and extract text from cells
        for row in rows:
            current_row_data = []
            cells = row.find_all("td")

            # Skip rows that don't have enough cells
            if len(cells) >= 4:
                current_row_data.append(cells[0].get_text(strip=True))  # Stationsname
                current_row_data.append(cells[1].get_text(strip=True))  # Stations_ID
                current_row_data.append(cells[3].get_text(strip=True))  # Stationskennung

                # Only add the row if it has the necessary data
                if len(current_row_data) == 3:
                    filled_rows.append(current_row_data)
                else:
                    print(f"warning: row with missing data skipped: {row}")
            else:
                print(f"warning: row with insufficient cells skipped: {row}")

        print(f"checkpoint 5: rows filled with data! Total rows: {len(filled_rows)}")

        # Convert rows to dictionary format
        data = [
            {"Stationsname": row[0], "Stations_ID": row[1], "Kennung": row[2]}
            for row in filled_rows
        ]
        print(f"checkpoint 6: data converted into dictionaries! Total entries: {len(data)}")

        # Save raw data to a JSON file
        with open("stations.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("checkpoint 7: stations.json created!")

        # Load the data from the saved JSON
        with open("stations.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        # Filter unique cities based on station name
        unique_data = []
        seen = set()

        for entry in data:
            station_name = entry.get("Stationsname", "")
            station_id = entry.get("Stations_ID", "")
            stationskennung = entry.get("Kennung", "")

            # Check for valid station name and ensure it isn't a duplicate
            if (
                station_name
                and station_name not in seen
                and not station_name.isdigit()
            ):
                unique_data.append(
                    {
                        "name": station_name,
                        "id": station_id,
                        "kennung": stationskennung,
                    }
                )
                seen.add(station_name)
            else:
                print(f"warning: invalid or duplicate entry found: {entry}")

        print(f"checkpoint 8: {len(unique_data)} unique cities found")

        # Save cleaned and unique data to another JSON file
        with open("cities.json", "w", encoding="utf-8") as f:
            json.dump(unique_data, f, indent=4, ensure_ascii=False)
        print("checkpoint 9: duplicates removed and saved to 'cities.json'")

    else:
        print("error: table not found on page.")

else:
    print(f"error fetching the page. status code: {response.status_code}")
