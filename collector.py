from bs4 import BeautifulSoup
import requests
import re
import os
from PIL import Image
from io import BytesIO
import pytesseract

# The idea is to get, from a range of ids, the .jpeg and text associated with it. Then, run the .jpeg
# through tesseract-ocr, and output data as {"prompt": <ocr_text>, "completion": <transcription>} in
# a .csv file, then pass it through the CLI data preparation tool to export it to JSONL

class Advertisement(object):
	def __init__(self, _id):
		self._id = _id
		self.url = "http://www.marronnage.info/fr/document.php?id=" + str(_id)
		self.request = requests.get(self.url)
		self.html = BeautifulSoup(self.request.text, "html.parser")
		self.document_url = self.get_document_url()
		self.transcription = self.get_transcription()
		self.location, self.newspaper, self.date = self.get_metadata()
		self.document = self.get_document()
		self.OCRd = False;
		self.OCRd_text = self.get_ocr_text()

	def get_document_url(self):
		urls = self.html.find_all('img')
		relative_url = urls[0].get('src')
		prefix = "https://www.marronnage.info/"
		return (prefix + relative_url[3:])
	
	def get_transcription(self):
		raw = self.html.find_all('p')
		return (raw[1].text)
	
	def get_metadata(self):
		raw = self.html.find_all('p')
		date = raw[0].text.split(' - ')[1]
		prefix = raw[0].text.strip(date)
		location = prefix.split(', ')[0].title()
		newspaper = prefix.split(', ')[1].replace(" -", "").title()
		return (location, newspaper, date)
	
	def get_date(self):
		raw = self.html.find_all('p')
		regex = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
		return (re.findall(regex, str(raw))[0])
	
	def get_document(self):
		response = requests.get(self.document_url)
		img = Image.open(BytesIO(response.content))
		return (img)

	def get_ocr_text(self):
		response = requests.get(self.document_url)
		img = Image.open(BytesIO(response.content))
		text = pytesseract.image_to_string(img)
		print(text)
		return ("")


if __name__ == '__main__':
	_id = 118
	ad = Advertisement(_id)