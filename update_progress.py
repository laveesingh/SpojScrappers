def solve():
		url = "http://www.spoj.com/ranks/users/48292/"
		import urllib, pickle
		from bs4 import BeautifulSoup
		print "Fetching data"
		htmlData = urllib.urlopen(url).read()
		print "Data fetched"
		soup = BeautifulSoup(htmlData, 'lxml')
		def fetchScore(name):
			for anchor in soup.findAll('a'):
				if anchor.text == name:
					return anchor.findParent().findParent().find('td', {'class':'text-right'}).string
		lavee = 'zflash'
		ravi = 'ravi shankar'
		kapil = 'K.K'
		'''Data dumping format will be
		InitialScore CummulativeIncrementSum
		'''
		f = open("progress_data.pickle", 'a+')
		print "fetching old scores"
		linit, lfinal = pickle.load(f)
		rinit, rfinal = pickle.load(f)
		kinit, kfinal = pickle.load(f)
		f.close()
		lscore = float(fetchScore(lavee))
		rscore = float(fetchScore(ravi))
		kscore = float(fetchScore(kapil))
		lfinal += lscore - linit
		rfinal += rscore - rinit
		kfinal += kscore - kinit
		linit = lscore
		rinit = rscore
		kinit = kscore
		print "score updated, writing to the file"
		# Erase contents of the file
		open('progress_data.pickle', 'w').close()
		f = open("progress_data.pickle", "a+")
		pickle.dump((linit, lfinal), f)
		pickle.dump((rinit, rfinal), f)
		pickle.dump((kinit, kfinal), f)
		print "written to the file"
		f.close()
solve()
