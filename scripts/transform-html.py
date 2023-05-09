import sys
from bs4 import BeautifulSoup

# Read the HTML document from stdin
html_doc = sys.stdin.read()

# Create a BeautifulSoup object
soup = BeautifulSoup(html_doc, 'html.parser')

for tag in soup.find_all(True):
    # Remove all inline styles
    if tag.has_attr('style'):
        del tag['style']

    # Remove ids (we can add these back later if needed)
    if tag.has_attr('id'):
        del tag['id']

    # Remove classes
    if tag.has_attr('class'):
        del tag['class']
    
    # Remove colspan / rowspan if they're set to the default (1)
    if tag.get('colspan') == "1":
        del tag['colspan']
    if tag.get('rowspan') == "1":
        del tag['rowspan']


# Remove unnecessary span tags
for span in soup.find_all('span'):
    span.unwrap()

# Remove empty paragraphs
for p in soup.find_all('p'):
    if not p.contents:
        p.extract()

# Remove empty anchors
for p in soup.find_all('a'):
    if not p.contents:
        p.extract()

# Pretty print the modified HTML
print(soup.prettify())
