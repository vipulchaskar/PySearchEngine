#usage: prompt> python crawler.py http://www.yourwebsitenamehere.com/somepage
#Scans the input page to find most of the links present and does simple crawling.
#Be cautious, crawlers can quickly go out of hand since web is an exhaustive resource to crawl.
#Use it in a controlled environment where you have a limited set of interlinked pages.

import sys
from urllib.request import urlopen

def union(list1, list2):
	for i in list2:
		if i not in list1:
			list1.append(i)

def get_next_target(s):
    start_link = s.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = s.find('"', start_link)
    end_quote = s.find('"', start_quote + 1)
    url = s[start_quote+1:end_quote]
    return url, end_quote

def get_all_links(page):
    linklist = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            linklist.append(url)
            page = page[endpos:]
        else:
            return linklist

def get_page(url):
    html = urlopen(url)
    page = html.read()
    return str(page)

def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            union(tocrawl, get_all_links(get_page(page)))
            crawled.append(page)
    return crawled

print(crawl_web(sys.argv[1]))

#print_all_links(get_page(sys.argv[1]))
#'http://www.udacity.com/cs101x/index.html'

