import getopt
import sys
import urllib2
import json
from os import listdir
from os.path import isfile, join

#TODO
# - Prevent gateway timeout

def scrapeTag(tag, number, offset, outputDirectory):
	# We need to find this every time.
	clientId = "b45b1aa10f1ac2941910a7f0d10f8e28"
	exploreUrl = ("https://api.soundcloud.com/explore/v2/" + tag + 
		"?limit=" + str(number) + "&offset=" + offset)
	explorePage = urllib2.urlopen(exploreUrl)

	files = getFilesInDirectory(outputDirectory)

	trackLinks = explorePage.read()
	trackLinks = json.loads(trackLinks)
	for item in trackLinks["docs"]:
		trackId =  item["urn"].split(":")[2]
		trackUrl = ("https://api.soundcloud.com/i1/tracks/" + str(trackId) + 
			"/streams?client_id=" + clientId)
		trackPage = urllib2.urlopen(trackUrl)
		trackData = trackPage.read()	
		trackData = json.loads(trackData)
		trackDownloadUrl = ''
		try:
			trackDownloadUrl = trackData["http_mp3_128_url"]
		except:
			print(str(trackId) + " does not have http")

		if trackDownloadUrl != '':
			title = getTitle(trackId, clientId)
			if (title + ".mp3") not in files:
				download(trackDownloadUrl, title, outputDirectory)
			else:
				print("Skipping " + title)

def scrapeSearch(searchTerm, number, offset, outputDirectory):
	clientId = "b45b1aa10f1ac2941910a7f0d10f8e28"
	searchUrl = ("https://api.soundcloud.com/search/sounds?q=" + searchTerm +
		"&facet=genre&limit=" + str(number) + "&offset=" + str(offset) 
		+ "&client_id=" + clientId)
	searchPage = urllib2.urlopen(searchUrl)
	searchPage = searchPage.read()
	searchPage = json.loads(searchPage)
	#print(searchPage)
	for item in searchPage["collection"]:
		trackId = item["id"]
		title = item["title"]
		print(title)

def getTitle(trackId, clientId):
	url = ("https://api.soundcloud.com/tracks/" + str(trackId) +
		".json?client_id=" + clientId)
	infoPage = urllib2.urlopen(url)
	info = infoPage.read()
	info = json.loads(info)

	title = info["title"]
	return title

def getFilesInDirectory(directory):
	files = [ f for f in listdir(directory) if isfile(join(directory, f))]
	return files

def download(trackUrl, title, outputDirectory):
	print("Downloading " + title)
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	headers = { 'User-Agent' : user_agent }

	trackFile = urllib2.urlopen(trackUrl, headers=headers)
	data = trackFile.read()
	if data.getCode() == 200:
		with open (outputDirectory + "/" + title + ".mp3", "wb") as mp3:
			mp3.write(data)

def printUsage():
	print("soundcloud-scraper.py -t <tag> -n <number> -o <outputDirectory> "
		"-f <offset>")


def main(argv):
	tag = ''
	number = 100
	outputDirectory = "~/"
	offset = 0
	searchTerm = ''
	try:
		opts,args = getopt.getopt(argv, "t:n:o:f:s:", ["tag=",
													   "number=",
													   "output=",
													   "offset=",
													   "searchTerm="])
	except getopt.GetoptError:
		printUsage()
		sys.exit(2)
	for opt,arg in opts:
		if opt == "-h":
			printUsage()
			sys.exit()
		elif opt in ("-t","--tag"):
			tag = arg
		elif opt in ("-n","--number"):
			number = arg
		elif opt in ("-o","--output"):
			outputDirectory = arg
		elif opt in ("-f","--offset"):
			offset = arg
		elif opt in ("-s","--searchTerm"):
			searchTerm = arg
	if searchTerm != '':
		scrapeSearch(searchTerm, number, offset, outputDirectory)
	else:
		scrapeTag(tag, number, offset, outputDirectory)

if __name__ == '__main__':
	main(sys.argv[1:])