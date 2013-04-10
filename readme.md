This is a quick script that I wrote for tracking changes on two popular (in Lithuania) advert sites and opening changed (added/updated/removed) adverts in new chrome tab. 

Script uses Beautiful Soup library for parsing html (currently only one page searches are supported) and local sqlite db for storing parsing results.

Following steps are required before starting:

	pip install beautifulsoup4

Currently supports skelbiu.lt and aruodas.lt. Relevant variables to modify are in the beginning of the script.

TODO:
* split into modules (db support, web site support, stored/retrived diffing)
* support for multiple page searches
* external config so I can compile it and distribute as exe?
