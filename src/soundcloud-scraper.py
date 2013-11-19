import getopt
import sys
import urllib2

def scrape(tag):
	url = "https://soundcloud.com/explore/" + tag
	page = urllib2.urlopen(url)
	data = page.read()
	print data

def main(argv):
	tag = ''
	try:
		opts,args = getopt.getopt(argv, "t:", ["tag="])
	except getopt.GetoptError:
		print("soundcloud-scraper.py -t <tag>")
		sys.exit(2)
	for opt,arg in opts:
		if opt == "-h":
			print("soundcloud-scraper.py -t <tag>")
			sys.exit()
		elif opt in ("-t","--tag"):
			tag = arg
	scrape(tag)

if __name__ == '__main__':
	main(sys.argv[1:])