
import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore
import html2text # type: ignore

def get_data_from_website(url):
    """
    Retrieve text content and metadata from a given URL.

    Args:
        url (str): The URL to fetch content from.

    Returns:
        tuple: A tuple containing the text content (str) and metadata (dict).
    """
    # Get response from the server
    response = requests.get(url)
    
    if response.status_code == 500:
        print("Server error")
        return None, None
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Remove JavaScript and CSS code
    for script in soup(["script", "style"]):
        script.extract()

    # Extract text in markdown format
    html = str(soup)
    html2text_instance = html2text.HTML2Text()
    html2text_instance.images_to_alt = True
    html2text_instance.body_width = 0
    html2text_instance.single_line_break = True
    text = html2text_instance.handle(html)

    # Extract page metadata
    try:
        page_title = soup.title.string.strip()
    except:
        page_title = url.split("//")[-1].split("/")[0]
    
    meta_description = soup.find("meta", attrs={"name": "description"})
    meta_keywords = soup.find("meta", attrs={"name": "keywords"})
    
    if meta_description:
        description = meta_description.get("content")
    else:
        description = page_title
    
    if meta_keywords:
        meta_keywords = meta_keywords.get("content")
    else:
        meta_keywords = ""

    metadata = {
        'title': page_title,
        'url': url,
        'description': description,
        'keywords': meta_keywords
    }

    return text, metadata


url = "https://thewasserstoff.com/"
text, metadata = get_data_from_website(url)
print("Text Content:", text)
print("Metadata:", metadata)
