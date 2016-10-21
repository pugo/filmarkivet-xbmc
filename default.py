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

import os, sys
import xbmc, xbmcaddon, xbmcgui, xbmcplugin
from lib.filmarkivet import Filmarkivet
import urlparse, urllib

addon = xbmcaddon.Addon()
ADDON_PATH = addon.getAddonInfo('path')
__translation = addon.getLocalizedString


def view_menu(menu):
	for item in menu:
		title = u'{} | {}'.format(item.title, item.description) if item.description else item.title
		li = xbmcgui.ListItem(title, iconImage=item.icon)
		if item.playable:
			li.setProperty('isplayable', 'true')
			li.setInfo('video', {'plot': item.description})
		xbmcplugin.addDirectoryItem(info['handle'], item.url, li, not item.playable)
	xbmcplugin.endOfDirectory(info['handle'])


def keyboard_get_string(default, message):
	keyboard = xbmc.Keyboard(default, message)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
		return keyboard.getText()
	else:
		return None


if ( __name__ == "__main__" ):
	info = {'name': addon.getAddonInfo('name'),
			'id': addon.getAddonInfo('id'),
			'handle': int(sys.argv[1]),
			'path': sys.argv[0],
			'icon': os.path.join(addon.getAddonInfo('path'), 'icon.png'),
			'fanart': os.path.join(addon.getAddonInfo('path'), 'fanart.jpg'),
			'cache': xbmc.translatePath(addon.getAddonInfo("Profile")),
			'translation': addon.getLocalizedString
			}

	if not os.path.exists(info['cache']):
		os.makedirs(info['cache'])

	params = urlparse.parse_qs(sys.argv[2][1:])
	print ('PARAMS:', params)
	print ('ARGV:', sys.argv)

	if 'content_type' in params:
		content_type = params['content_type'][0]

	fa = Filmarkivet(info)
	if 'mode' in params:
		page = int(params['page'][0]) if 'page' in params else 1

		if params['mode'][0] == 'categories':
			view_menu(fa.get_categories())
		if params['mode'][0] == 'category':
			if 'url' in params:
				movies = fa.get_url_movies(params['url'][0], mode='category', page=page, limit=True)
				view_menu(movies)

		if params['mode'][0] == 'letters':
			view_menu(fa.get_letters())
		if params['mode'][0] == 'letter':
			if 'l' in params:
				view_menu(fa.get_letter_movies(params['l'][0]))

		if params['mode'][0] == 'themes':
			view_menu(fa.get_themes())
		if params['mode'][0] == 'theme':
			if 'url' in params:
				movies = fa.get_url_movies(params['url'][0], mode='theme', page=page, limit=True)
				view_menu(movies)

		if params['mode'][0] == 'watch':
			url = urllib.unquote(params['url'][0])
			media_url = fa.get_media_url(url)
			li = xbmcgui.ListItem(path=media_url)
			xbmcplugin.setResolvedUrl(info['handle'], True, li)

		if params['mode'][0] == 'search':
			key = params['key'][0] if 'key' in params else keyboard_get_string('', info['translation'](30023))
			movies = fa.get_url_movies('/sokresultat/?q={}'.format(key), mode='search&key={}'.format(key), page=page, limit=True)
			view_menu(movies)

	else:
		view_menu(fa.get_mainmenu())


