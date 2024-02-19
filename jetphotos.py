import requests
from bs4 import BeautifulSoup

def full(tail):
	url = "https://www.jetphotos.com/showphotos.php?keywords-type=reg&keywords=" + tail + "&search-type=Advanced&keywords-contain=0&sort-order=4"
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	imageURLElement = soup.find('a', class_="result__photoLink")
	response = requests.get("https://jetphotos.com" + imageURLElement['href'])
	soup = BeautifulSoup(response.text, 'html.parser')
	image = soup.find('img', class_="large-photo__img")
	response = requests.get(image['srcset'])
	name = tail + ".jpg"
	with open(name, 'wb') as localImage:
		localImage.write(response.content)
		
def thumb(tail):
	url = "https://www.jetphotos.com/showphotos.php?keywords-type=reg&keywords=" + tail + "&search-type=Advanced&keywords-contain=0&sort-order=4"
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	image = soup.find('img', class_="result__photo")
	response = requests.get('https:' + image['src'])
	name = tail + ".jpg"
	with open(name, 'wb') as localImage:
		localImage.write(response.content)