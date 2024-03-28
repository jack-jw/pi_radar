# Piradar
# jetphotos.py

"""
Get urls for images of aircraft from JetPhotos & cache them locally

Functions:
    full()
    thumb()
"""

from glob import glob
from requests import get
from bs4 import BeautifulSoup

_IMAGE_LOCATION = "./instance/images"

def full_url(tail):
    """
    Get the full image of an aircraft
    Includes JetPhotos watermark
    
    Takes a tail number as a string
    Returns a URL to JetPhotos as a string (or None if not found)
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

def thumb_url(tail):
    """
    Get a small (thumbnail) image of an aircraft
    Does not include the JetPhotos watermark

    Takes a tail number as a string
    Returns a URL to JetPhotos as a string (or None if not found)
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

def full(tail):
    """
    Get the full image of an aircraft
    Includes JetPhotos watermark
    Caches images locally for faster loading times

    Takes a tail number as a string
    Returns a URL as a string (or None if not found)
    """

    images = glob(f"{_IMAGE_LOCATION}/*-full-{tail}.jpeg")
    if images:
        return images[0]
    else:
        url = full_url(tail)
        if url:
            response = get(url, timeout=60)
            with open(f"{_IMAGE_LOCATION}/jp-full-{tail}.jpeg", "wb") as image_file:
                image_file.write(response.content)
            return f"{_IMAGE_LOCATION}/jp-full-{tail}.jpeg"
        else:
            return None

def thumb(tail):
    """
    Get a small (thumbnail) image of an aircraft
    Does not include the JetPhotos watermark
    Caches images locally for faster loading times

    Takes a tail number as a string
    Returns a URL to JetPhotos as a string (or None if not found)
    """

    images = glob(f"{_IMAGE_LOCATION}/*-thumb-{tail}.jpeg")
    if images:
        return images[0]
    else:
        url = thumb_url(tail)
        if url:
            response = get(url, timeout=60)
            with open(f"{_IMAGE_LOCATION}/jp-thumb-{tail}.jpeg", "wb") as image_file:
                image_file.write(response.content)
            return f"{_IMAGE_LOCATION}/jp-thumb-{tail}.jpeg"
        else:
            return None
