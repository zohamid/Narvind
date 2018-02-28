from pymongo import MongoClient
from PIL import Image
from io import StringIO
import urllib.request
import csv

client = MongoClient()
collection = client['precog']
database = collection['image_data']

def save_data(data):
	global database
	database.insert_one(data)


def download(url, name, path):
	urllib.request.urlretrieve(url, path+name)


def download_all_images():
	global database
	i = 0
	j = 0
	for x in database.find():
		if any(y in x['tweet'].lower() for y in ["namo", "modi"]):
			i += 1
			download(x['media_url'], str(i), "images/namo/")
		if any(y in x['tweet'].lower() for y in ["arvind", "kejri"]):
			j += 1
			download(x['media_url'], str(i), "images/arvind/")
	print(i)


def read_from_file(filename):
	i = 0
	with open(filename) as f:
		reader = csv.reader(f)
		next(reader, None)
		#print(reader)
		for row in reader:
			try:
				if len(row[3]) > 0:
					save_data({"tweet": row[2], "media_url": row[3]})
					i += 1
				else:
					print("not pushed")
			except Exception as ex:
				print(ex)
				break
	return i

channellist = ["newsworldin", "AllDUNews", "indiatvnews", "aajtak", "NewsX", "ZeeNews", "ndtvindia","abpnewstv","TimesNow","DilliAajtaktv","indianews","ibnlive","CNNnews18","timesofindia","htTweets"]
for i in channellist:
	print(read_from_file(i + "_tweets.csv"))

#download_all_images()
