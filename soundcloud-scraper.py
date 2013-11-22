import getopt
import sys
import urllib2
import json

#TODO
# - Have a list of previously downloaded songs
# - Output directory


# https://api.soundcloud.com/explore/v2/electronic
# https://api.soundcloud.com/explore/v2/electronic?limit=100&offset=0
# https://api.soundcloud.com/i1/tracks/120859378/streams?client_id=b45b1aa10f1ac2941910a7f0d10f8e28&app_version=fc06c6b8
# need the correct client_id
def scrape(tag, number, outputDirectory):
	url = "https://api.soundcloud.com/explore/v2/" + tag + "?limit=" + str(number)
	print url
	page = urllib2.urlopen(url)
	data = page.read()
	decoded = json.loads(data)
	for item in decoded["docs"]:
		trackId =  item["urn"].split(":")[2]
		trackUrl = ("https://api.soundcloud.com/i1/tracks/" + str(trackId) + 
			"/streams?client_id=")
		print(trackUrl)

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