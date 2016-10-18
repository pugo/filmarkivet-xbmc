# -*- coding: utf-8 -*-

'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from bs4 import BeautifulSoup
import lib.webget
import urllib


class Filmarkivet(object):
	MOVIES_PER_PAGE = 20

	MAIN_MENU = [{'mode': 'categories', 'title': 30010},
				 {'mode': 'letters', 'title': 30011},
				 {'mode': 'themes', 'title': 30012},
				 {'mode': 'search', 'title': 30023}]

	class ListItem(object):
		def __init__(self, title, url, description, icon):
			self.title = title
			self.url = url
			self.description = description
			self.icon = icon
			self.playable = False

	def __init__(self, info):
		self.info = info
		self.webget = lib.webget.WebGet(info['cache'])

	def __url_for(self, url):
		return 'plugin://{}{}'.format(self.info['id'], url)

	def get_mainmenu(self):
		result = []
		for item in self.MAIN_MENU:
			result.append(self.ListItem(self.info['translation'](item['title']),
										self.__url_for('?mode={}'.format(item['mode'])), '', ''))
		return result

	def __mode_url(self, mode):
	    return 'plugin://{}?mode={}'.format(self.info['id'], mode)

	def get_categories(self):
		html = self.webget.getURL('/')
		soup = BeautifulSoup(html, 'html.parser')
		soup = soup.find('ul', {'class': 'site-nav-menu'})
		lists = soup.find_all('ul')
		if not len(lists):
			print('Error!')
			return []
		items = lists[0].find_all('li')
		result = []
		mode_url = self.__mode_url('category')
		for item in items[1:]:
			url = '{}&url={}'.format(mode_url, item.a['href'])
			result.append(self.ListItem(item.a.string, url, '', ''))
		return result

	def get_url_movies(self, url, unlimit=False):
		if unlimit:
			url = url + '&limit=1000'
		html = self.webget.getURL(url)
		soup = BeautifulSoup(html, 'html.parser')
		soup = soup.find('div', {'id': 'list'})
		movies = soup.find_all('a', {'class': 'item'})
		result = []
		mode_url = self.__mode_url('watch')
		for movie in movies:
			title = movie.h3.contents[0].strip()
			url = '{}&url={}'.format(mode_url, urllib.quote(movie['href'].replace('#038;', '')))
			desc = u'{} ({})'.format(movie.p.string.strip(), movie.h3.span.string.strip())
			img = movie.figure.img['src']
			li = self.ListItem(title, url, desc, img)
			li.playable = True
			result.append(li)
		return result

	def get_letters(self):
		result = []
		mode_url = self.__mode_url('letter')
		for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ":
			url = '{}&l={}'.format(mode_url, l.lower())
			result.append(self.ListItem(l, url, '', ''))
		return result

	def get_letter_movies(self, letter):
		html = self.webget.getURL('/filmer-a-o/')
		soup = BeautifulSoup(html, 'html.parser')
		result = []
		soup = soup.find('section', {'class': 'block', 'id': letter})
		soup = soup.find('ul', {'class': 'alphabetical'})
		movies = soup.find_all('a')
		print soup
		mode_url = self.__mode_url('watch')
		for movie in movies:
			title = movie.contents[0].strip()
			url = '{}&url={}'.format(mode_url, urllib.quote(movie['href']))
			# desc = u'{} ({})'.format(movie.p.string.strip(), movie.h3.span.string.strip())
			# img = movie.figure.img['src']
			li = self.ListItem(title, url, None, None)
			li.playable = True
			result.append(li)
		return result

	def get_themes(self):
		html = self.webget.getURL('/')
		soup = BeautifulSoup(html, 'html.parser')
		soup = soup.find('ul', {'class': 'site-nav-menu'})
		lists = soup.find_all('ul')
		if len(lists) < 2:
			print('Error!')
			return []
		items = lists[1].find_all('li')
		result = []
		mode_url = self.__mode_url('theme')
		for item in items[1:]:
			url = '{}&url={}'.format(mode_url, item.a['href'])
			result.append(self.ListItem(item.a.string, url, '', ''))
		return result

	def get_media_url(self, url):
		html = self.webget.getURL(url)
		soup = BeautifulSoup(html, 'html.parser')
		video = soup.find('div', {'class': 'video-container'}).get_text()
		start = video.find('sources:')
		if start >= 0:
			end = video.find('}]', start)
			video = video[start:end]
			for line in video.split('\n'):
				if line.strip().startswith('file:'):
					l = line.split('"')
					if l[1].startswith('https:'):
						return l[1]
		return None


# def parse_search(search_string, page=1):
# 	try:
# 		url = FILMARKIVET_BASE + 'Sok/?q=%s&page=%d' % (search_string, page)
# 		html = session.get(url).text
#
# 		hits = parseHits(html)
# 		films = parseFilms(html)
#
# 		next_url = None
# 		if page * MOVIES_PER_PAGE < hits:
# 			next_url = '/search/%s/%d' % (search_string, page+1)
#
# 		return films, next_url
# 	except:
# 		return None, None
#

# def parseHits(html):
# 	try:
# 		h = parseDOM(html, 'div', {'class':'number-of-hits'})
# 		return int(h[0].split('</span>')[1])
# 	except:
# 		print 'failed to get hits.'
# 	return 0


