import urllib, datetime, re
from bs4 import BeautifulSoup
url = "http://www.spoj.com/status/lavee_singh"
now = datetime.datetime.now()
submissions = 0
for start in xrange(0, 80, 20):
	nurl = url + '/start=' + str(start)
	data = urllib.urlopen(nurl).read()
	soup = BeautifulSoup(data, 'lxml')
	for td in soup.findAll('td', {'class':'status_sm'}):
		subtime = re.split(r'[\- ]', td.text)
		if subtime[1] == str(now.month) and subtime[2] == str(now.day):
			submissions += 1

print "total submissions today:",submissions