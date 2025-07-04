import requests
from bs4 import BeautifulSoup
import webbrowser
import os

url = "https://www.panabee.com/news/abbvie-earnings-q3-2025/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract all section tags
sections = soup.find_all('section')

# Combine all the extracted HTML
html_content = ''
for section in sections:
    html_content += section.prettify()

# If you want to wrap it in a simple HTML structure:
full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Extracted Sections</title>
</head>
<body>
{html_content}
</body>
</html>
"""

# Write to file
file_path = os.path.join(os.getcwd(), 'GFG.html')
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(full_html)

# Open the HTML file in a new browser tab
webbrowser.open_new_tab('file://' + file_path)
