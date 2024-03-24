# Piradar
# jetphotos.py

"""
Get urls for images of aircraft from JetPhotos

Functions:
    full()
    thumb()
"""

from requests import get
from bs4 import BeautifulSoup

def full(tail):
    """
    Get the full image of an aircraft
    Includes JetPhotos watermark
    
    Takes a tail number as a string
    Returns a URL (or None if not found)
    """

    url = ("https://www.jetphotos.com/showphotos.php?keywords-type=reg&keywords="
           + tail
           + "&search-type=Advanced&keywords-contain=0&sort-order=4")
    response = get(url, timeout=60)
    soup = BeautifulSoup(response.text, "html.parser")
    image_url_element = soup.find("a", class_="result__photoLink")
    if not image_url_element:
        return None

    response = get("https://jetphotos.com" + image_url_element["href"], timeout=60)
    soup = BeautifulSoup(response.text, "html.parser")
    image = soup.find("img", class_="large-photo__img")

    if image:
        return image["srcset"]
    else:
        return None

def thumb(tail):
    """
    Get a small (thumbnail) image of an aircraft
    Does not include the JetPhotos watermark
    
    Takes a tail number as a string
    Returns a URL (or None if not found)
    """

    url = ("https://www.jetphotos.com/showphotos.php?keywords-type=reg&keywords="
           + tail
           + "&search-type=Advanced&keywords-contain=0&sort-order=4")
    response = get(url, timeout=60)
    soup = BeautifulSoup(response.text, "html.parser")
    image = soup.find("img", class_="result__photo")
    if image:
        return "https:" + image["src"]
    else:
        return None
