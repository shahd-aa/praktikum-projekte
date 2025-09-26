# library used to extract content from html
from bs4 import BeautifulSoup

   
with open('arc_solutions_logo.html', 'r', encoding='utf-8') as file:
  content = file.read() # open html file

soup = BeautifulSoup(content, "html.parser") # parse content

# input for text
user_input = input("Was soll der Spruch sein?: ")

# find header in html
header2 = soup.find("h2")

# clear for next input
if header2: 
  header2.clear()
  header2.string = user_input

# show changes
savechanges = soup.prettify("utf-8")
with open("arc_solutions_logo.html", "wb") as file: 
    file.write(savechanges)