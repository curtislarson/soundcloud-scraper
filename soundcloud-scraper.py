import getopt
import sys
import urllib2
import json

#TODO
# - Have a list of previously downloaded songs
# - Output directory

#
# format for finding title

def scrape(tag, number, outputDirectory):
	# We need to find this every time.
	clientId = "b45b1aa10f1ac2941910a7f0d10f8e28"
	exploreUrl = "https://api.soundcloud.com/explore/v2/" + tag + "?limit=" + str(number)
	explorePage = urllib2.urlopen(exploreUrl)

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
			download(trackDownloadUrl, title, outputDirectory)

def getTitle(trackId, clientId):
	url = ("https://api.soundcloud.com/tracks/" + str(trackId) +
		".json?client_id=" + clientId)
	infoPage = urllib2.urlopen(url)
	info = infoPage.read()
	info = json.loads(info)

	title = info["title"]
	return title

def download(trackUrl, title, outputDirectory):
	print (trackUrl)

def main(argv):
	tag = ''
	number = 100
	outputDirectory = "~/"
	try:
		opts,args = getopt.getopt(argv, "t:n:o:", ["tag=","number=","output="])
	except getopt.GetoptError:
		print("soundcloud-scraper.py -t <tag> -n <number>")
		sys.exit(2)
	for opt,arg in opts:
		if opt == "-h":
			print("soundcloud-scraper.py -t <tag> -n <number> -o <outputDirectory>")
			sys.exit()
		elif opt in ("-t","--tag"):
			tag = arg
		elif opt in ("-n","--number"):
			number = arg
		elif opt in ("-o","--output"):
			outputDirectory = arg
	scrape(tag, number, outputDirectory)

if __name__ == '__main__':
	main(sys.argv[1:])