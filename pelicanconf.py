#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals

AUTHOR = 'shymonk'
SITENAME = "Shymonk Blog"
SITEURL = ''

# Article path
PATH = 'posts'

# Theme
THEME = 'themes/frankies'

# Locale
DEFAULT_LANG = 'en'
LOCALE = ('en_US',)
TIMEZONE = 'Asia/Shanghai'

# Datetime
DEFAULT_DATE = 'fs'
DEFAULT_DATE_FORMAT = '%B %d, %Y'

# Place articles in a location such as {slug}/index.html
# and link to them as {slug} instead of {slug}.html
# for clean URLs
ARTICLE_URL = "posts/{date:%Y}/{date:%m}/{slug}/"
ARTICLE_SAVE_AS = "posts/{date:%Y}/{date:%m}/{slug}/index.html"
CATEGORY_URL = "category/{slug}"
CATEGORY_SAVE_AS = "category/{slug}/index.html"
TAG_URL = "tag/{slug}/"
TAG_SAVE_AS = "tag/{slug}/index.html"
YEAR_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/index.html'

# Disqus
DISQUS_SITENAME = "shymonk"

# Google Analytics
GOOGLE_ANALYTICS = "UA-56451105-1"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

MENUITEMS = (
    ('Home', '/'),
    ('Archives', '/archives.html'),
    ('Projects', '/projects.html'),
)

LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
