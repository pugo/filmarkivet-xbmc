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
		print '-- playable: {}'.format(item.playable)
		if item.playable:
			li.setProperty('isplayable', 'true')
			li.setInfo('video', {'plot': item.description})
		xbmcplugin.addDirectoryItem(info['handle'], item.url, li, not item.playable)
	xbmcplugin.addSortMethod(info['handle'], xbmcplugin.SORT_METHOD_TITLE)
	xbmcplugin.endOfDirectory(info['handle'])


# @plugin.route('/search')
# @plugin.route('/search/<search_string>')
# @plugin.route('/search/<search_string>/<page>')
# def search(search_string=None, page="1"):
# 	if search_string == None:
# 		search_string = unikeyboard("", "")
#
# 	films, next_url = data.parse_search(search_string, int(page))
# 	view(films, next_url=next_url)
#
# # Show keyboard with given message as instructions. Return result string or None.
# def unikeyboard(default, message):
# 	keyboard = xbmc.Keyboard(default, message)
# 	keyboard.doModal()
# 	if (keyboard.isConfirmed()):
# 		return keyboard.getText()
# 	else:
# 		return None
#
# # Show a list of data.
# def view(elements, next_url=None):
# 	if not elements:
# 		error_title = __translation(30002)
# 		error_message1 = __translation(30003)
# 		error_message2 = __translation(30005)
# 		error_message3 = __translation(30004)
# 		dialog = xbmcgui.Dialog()
# 		dialog.ok(error_title, error_message1, error_message2, error_message3)
# 		return
#
# 	total = len(elements)
# 	for title, url, descr, thumb in elements:
# 		descr = descr() if callable(descr) else descr
# 		thumb = thumb() if callable(thumb) else thumb
#
# 		li = xbmcgui.ListItem(title, thumbnailImage=thumb)
# 		playable = False
# 		# playable = plugin.route_for(url) == play
# 		# li.setProperty('isplayable', str(playable))
# 		# if playable:
# 		# 	li.setInfo('video', {'plot':descr})
# 		# xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(url), li, not playable, total)
#
# 	# if next_url:
# 	# 	text_next_page = __translation(30001)
# 	# 	addPager(text_next_page, next_url, '', total)
# 	# xbmcplugin.endOfDirectory(plugin.handle)
#
# # Add pager line at bottom of a list.
# def addPager(title, url, thumb, total):
# 	li = xbmcgui.ListItem(title, thumbnailImage=thumb)
# 	playable = plugin.route_for(url) == play
# 	li.setProperty('isplayable', str(playable))
# 	if playable:
# 		li.setInfo('video', {'plot':descr})
# 	xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(url), li, not playable, total)

 
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
		if params['mode'][0] == 'categories':
			view_menu(fa.get_categories())
		if params['mode'][0] == 'category':
			if 'url' in params:
				view_menu(fa.get_url_movies(params['url'][0], unlimit=True))

		if params['mode'][0] == 'letters':
			view_menu(fa.get_letters())
		if params['mode'][0] == 'letter':
			if 'l' in params:
				view_menu(fa.get_letter_movies(params['l'][0]))

		if params['mode'][0] == 'themes':
			view_menu(fa.get_themes())
		if params['mode'][0] == 'theme':
			if 'url' in params:
				view_menu(fa.get_url_movies(params['url'][0]))

		if params['mode'][0] == 'watch':
			url = urllib.unquote(params['url'][0])
			media_url = fa.get_media_url(url)
			li = xbmcgui.ListItem(path=media_url)
			xbmcplugin.setResolvedUrl(info['handle'], True, li)

	else:
		view_menu(fa.get_mainmenu())


