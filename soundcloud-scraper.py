import getopt
import sys
import urllib2
import json

#TODO
# - Have a list of previously downloaded songs
# - Output directory

def scrape(tag, number, outputDirectory):
	# We need to find this every time.
	clientId = "b45b1aa10f1ac2941910a7f0d10f8e28"
	url = "https://api.soundcloud.com/explore/v2/" + tag + "?limit=" + str(number)
	print url
	page = urllib2.urlopen(url)
	data = page.read()
	decoded = json.loads(data)
	for item in decoded["docs"]:
		trackId =  item["urn"].split(":")[2]
		trackUrl = ("https://api.soundcloud.com/i1/tracks/" + str(trackId) + 
			"/streams?client_id=" + clientId)
		page = urllib2.urlopen(trackUrl)
		trackData = page.read()	
		trackData = json.loads(trackData)
		track = ''
		try:
			track = trackData["http_mp3_128_url"]
		except:
			print(str(trackId) + " does not have http")

		if track != '':
			download(track, outputDirectory)

def download(trackUrl, outputDirectory):

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