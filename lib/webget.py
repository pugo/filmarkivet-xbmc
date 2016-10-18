
import os
import urllib
import hashlib
import datetime
import urllib2



class GetException(Exception):
	pass

class WebGet(object):
	API_URL = "http://www.filmarkivet.se"

	def __init__(self, cachePath):
		self.cachePath = cachePath
		print('cache:', self.cachePath)

	def getURL(self, url='/'):
		print 'getURL:', url
		return self.__http_request(url)

	def __http_request(self, url, params=None, cache_minutes = 120):
		try:
			if not url.startswith('http://'):
				url = self.API_URL + url
				print 'xxxx:', url
			if params:
				url = url + '?' + urllib.urlencode(params, doseq=True)
			cache_path = os.path.join(self.cachePath, hashlib.md5(url).hexdigest() + '.cache')
			cache_until = datetime.datetime.now() - datetime.timedelta(minutes=cache_minutes)
			if not os.path.exists(cache_path) or datetime.datetime.fromtimestamp(os.path.getmtime(cache_path)) < cache_until:
				data = self.__download_url(url, cache_path)
			else:
				with open(cache_path) as f:
					data = f.read()
			return data
		except Exception as ex:
			raise GetException(ex)

	def __download_url(self, url, destination):
		data = ''
		u = urllib2.urlopen(url, timeout=30)
		data = u.read()
		u.close()

		try:
			with open(destination, 'w') as dest:
				dest.write(data)
		except:
			pass  # ignore, cache has no effect

		return data
