#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

THEME = "oss-theme"

#GITHUB_URL = "https://github.com/mkfifo/open-source-stats"

LOAD_CONTENT_CACHE = False
DELETE_OUTPUT_DIRECTORY = True

#PAGE_ORDER_BY = 'page-order'

DISPLAY_PAGES_ON_MENU = False

# no need for articles
ARTICLE_SAVE_AS = ''
PAGE_PATHS = ['']
ARTICLE_PATHS = ['blog']

STATIC_PATHS = [ 'js', 'data', 'css' ]

USE_FOLDER_AS_CATEGORY = True
PAGE_URL = '{category}/{slug}.html'
PAGE_SAVE_AS = '{category}/{slug}.html'
#CATEGORY_URL = 'category/{slug}.html'
#CATEGORY_SAVE_AS = 'category/{slug}.html'

AUTHOR = 'Chris Hall'
SITENAME = 'open source stats'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

MENUITEMS = (
        ('Home',     '/index.html'),
        ('Projects', '/projects.html'),
        ('Users',    '/users.html'),
)
# Blogroll
#LINKS = (('Pelican', 'http://getpelican.com/'),
#         ('Python.org', 'http://python.org/'),
#         ('Jinja2', 'http://jinja.pocoo.org/'),
#         ('You can modify those links in your config file', '#'),)
#
## Social widget
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False

TEMPLATE_PAGES = {
        'projects.html': 'projects.html',
        'users.html': 'users.html',
}


