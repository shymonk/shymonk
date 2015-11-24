#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals

AUTHOR = 'shymonk'
SITENAME = "shymonk"
SITESUBTITLE = 'Programming with python and emacs'
SITEURL = ''

# Article path
PATH = 'content/posts/'
IGNORE_FILES = ['.#*', '*.org']

# Theme
THEME = 'themes/cleanblog'

DEFAULT_LANG = 'en'
LOCALE = ('en_US',)
TIMEZONE = 'Asia/Shanghai'
DEFAULT_DATE = 'fs'
DEFAULT_DATE_FORMAT = '%B %d, %Y'

# Place articles in a location such as {slug}/index.html
# and link to them as {slug} instead of {slug}.html
# for clean URLs
ARTICLE_URL = "posts/{date:%Y}/{date:%m}/{slug}/"
ARTICLE_SAVE_AS = "posts/{date:%Y}/{date:%m}/{slug}/index.html"
YEAR_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/index.html'
PAGE_URL = "{slug}.html"
PAGE_SAVE_AS = "{slug}.html"
AUTHORS_SAVE_AS = ""
CATEGORY_SAVE_AS = ""
TAG_SAVE_AS = ""

# Disqus
DISQUS_SITENAME = "shymonk"
GOOGLE_ANALYTICS = "UA-56451105-1"
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False
MENUITEMS = (
    ('Archives', '/archives.html'),
    ('About', '/about.html'),
)

LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
GITHUB_URL = 'http://github.com/shymonk'
INSTAGRAM_URL = 'https://www.instagram.com/shymonk/'
EMAIL_URL = 'mailto:hellojohn201@gmail.com'


DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
