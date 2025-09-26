import requests
from bs4 import BeautifulSoup
import json

# fetch → check → parse → extract → structure → output
# create checkpoints with print

# fetch url
url = "https://www.dwd.de/DE/leistungen/klimadatendeutschland/statliste/statlex_html.html;jsessionid=E1D047C421FA29EB8FA59B318ED088F6.live11054?view=nasPublication&nn=16102"

# get response
response = requests.get(url)
print(f"checkpoint 1: {response}")

# response 200 ? -> parse into soup
if response.status_code == 200:
    print(f"checkpoint 2: code is 200!")
    soup = BeautifulSoup(response.text, "html.parser")
    # extract data from big table
    print(f"checkpoint 3: data parsed")
    table = soup.find("table")
    if table:
        print(f"checkpoint 4: table was found!")
    stripped_table = table.get_text(strip=True)
    print(f"checkpoint 5: text was extracted!")
    
# create empty array of rows -> find rows (but skip header)
rows = table.find_all("tr")[1:]
print(f"checkpoint 6: all rows found!")

filled_rows = []
printed = False

# for every row, find cell
for row in rows:
    current_row_data = []
    cells = row.find_all("td")
    if not printed and cells:
        print(f"checkpoint 7: all cells found!")
        printed = True
        
    # extract text from cell
    for cell in cells:
      stripped_cell = cell.get_text(strip=True)
      current_row_data.append(stripped_cell)
      
      printed = False
      if not printed and stripped_cell:
        print(f"checkpoint 8: extracted text from cells!") 
        printed = True
      # append text from cell into empty array of rows
    filled_rows.append(current_row_data)

print(f"checkpoint 9: appended!")

# get all headers
headers = [th.get_text().strip() for th in table.find_all("th")]

# empty array of data -> get every row ->
data = []
for row in filled_rows:
    # take first header and first data point & pair together
    data.append(dict(zip(headers, row)))

# convert to json and print
    json_data = json.dumps(data, indent=4, ensure_ascii=False)
    print(json_data)
    
# bad response ? -> show error 
else:
    print(f"Error fetching the page. Status code: {response.status_code}")
# load the JSON data from file
with open('stations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)  # This will load the JSON as a Python list of dictionaries
    print(f"checkpoint 10: json converted in dict!")

# create a list to store unique cities based on 'name'
unique_data = []
seen = set()

# iterate over the data and add unique cities
for entry in data:
    
# check if the 'name' key exists before trying to access it
  if "name" in entry:
        city_name = entry["name"]
        if city_name not in seen:
            unique_data.append(entry)
            seen.add(city_name)
  # handle the case where 'name' doesn't exist in the entry
  else:
        # Handle the case where 'name' doesn't exist in the entry
        print(f"Warning: 'name' key missing in entry: {entry}")
        
# output the cleaned list (you can save it to a file)
with open('cities.json', 'w', encoding='utf-8') as f:
    json.dump(unique_data, f, indent=4, ensure_ascii=False)
    
# print duplicates removed as well as new json file
print("duplicates removed and saved to 'cities.json'")