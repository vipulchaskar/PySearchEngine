#usage: prompt> python crawler.py http://www.pagetocrawl.com search_keyword
#Starts crawling from the seed page specified in sys.argv[1]. Makes an index of the scanned keywords.
#Computes ranks of all scanned pages with an algorithm identical to PageRank.
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

def add_page_to_index(index,url,content):
	words = content.split()
	for word in words:
		add_to_index(index,word,url)

def add_to_index(index,keyword,url):
	if keyword in index:
		index[keyword].append(url)
	else:
		index[keyword] = [url]

def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    graph = {}
    index = {}
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index,page,content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)
    #return crawled
    return index,graph

def compute_ranks(graph):
        d = 0.8
        numloops = 10

        ranks = {}
        npages = len(graph)
        for page in graph:
                ranks[page] = 1.0/npages

        for i in range(0,numloops):
                newranks = {}
                for page in graph:
                        newrank = (1-d)/npages
                        for node in graph:
                                if page in graph[node]:
                                        newrank += ranks[node] * d / len(graph[node])
                        newranks[page] = newrank
                ranks = newranks
        return ranks


def lookup(index,ranks,word):
	results = {}
	if word in index:
		for result in index[word]:
			results[result] = ranks[result]
		return results
	else:
		return None

index,graph = crawl_web(sys.argv[1])

ranks = compute_ranks(graph)

#print(ranks)
#print(index)
resultdict = lookup(index,ranks,sys.argv[2])
print(sorted(resultdict, key=resultdict.get, reverse=True))
#http://www.udacity.com/cs101x/index.html
