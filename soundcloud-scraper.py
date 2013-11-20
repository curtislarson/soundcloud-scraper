import getopt
import sys
import urllib2

# https://api.soundcloud.com/explore/v2/electronic
# https://api.soundcloud.com/explore/v2/electronic?limit=100&offset=0
def scrape(tag, number):
	url = "https://api.soundcloud.com/explore/v2/" + tag + "?limit=" + number
	page = urllib2.urlopen(url)
	data = page.read()
	print data

def main(argv):
	tag = ''
	number = 100
	try:
		opts,args = getopt.getopt(argv, "t:n:", ["tag=","number="])
	except getopt.GetoptError:
		print("soundcloud-scraper.py -t <tag> -n <number>")
		sys.exit(2)
	for opt,arg in opts:
		if opt == "-h":
			print("soundcloud-scraper.py -t <tag> -n <number>")
			sys.exit()
		elif opt in ("-t","--tag"):
			tag = arg
		elif opt in ("-n","--number"):
			number = arg
	scrape(tag)

if __name__ == '__main__':
	main(sys.argv[1:])