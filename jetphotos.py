# Piradar
# JetPhotos.py

"""
Get images of aircraft from JetPhotos
"""

from requests import get
from bs4 import BeautifulSoup

def full(tail):
    """
    Get the full image of an aircraft from its tail number
    Includes watermark
    """

    url = "https://www.jetphotos.com/showphotos.php?keywords-type=reg&keywords=" + tail + "&search-type=Advanced&keywords-contain=0&sort-order=4"
    response = get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    image_url_element = soup.find("a", class_="result__photoLink")
    response = get("https://jetphotos.com" + image_url_element["href"])
    soup = BeautifulSoup(response.text, "html.parser")
    image = soup.find("img", class_="large-photo__img")
    response = get(image["srcset"])
    name = tail + ".jpg"
    with open(name, "wb") as local_image:
        local_image.write(response.content)

def thumb(tail):
    """
    Get a small, thumbnail image of an aircraft from its tail number
    Does not include watermark
    """

    url = "https://www.jetphotos.com/showphotos.php?keywords-type=reg&keywords=" + tail + "&search-type=Advanced&keywords-contain=0&sort-order=4"
    response = get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    image = soup.find("img", class_="result__photo")
    response = get("https:" + image["src"])
    name = tail + ".jpg"
    with open(name, "wb") as local_image:
        local_image.write(response.content)
