# encoding: utf-8
import csv
import urllib2
from bs4 import BeautifulSoup
from selenium import webdriver
import sys

def handle_response(url, link_set,failed_links):
	f = urllib2.urlopen(url).read()
	lst = BeautifulSoup(f).find_all(class_='card-ui cui-c-udc c-bdr-gray-clr ')
	result = []
	for i in lst:
		link = i.contents[1]['href']
		try:
			ori_price = i.contents[1].contents[1].contents[3].find_all(class_='cui-price-original c-txt-gray-dk ')[0].contents[0]
			dis_priec = i.contents[1].contents[1].contents[3].find_all(class_='cui-price-discount c-txt-price ')[0].contents[0]
			company_name = i.contents[1].contents[1].contents[3].contents[3].contents[0].split('\n')[1].strip()
			content = i.contents[1].contents[1].contents[3].contents[1].contents[0].split('\n')[1].strip()
			
		    
			browser.get(link) #emulate chrome to browse the page
			soup = BeautifulSoup(browser.page_source)
			contacts = set(zip([i.contents[0].split('\n')[1].strip() for i in soup.find_all(class_='address-content')],\
			    [i.contents[0].split('\n')[1].strip() for i in soup.find_all(class_='address-phone')]))

			if link not in link_set:
				links_set.add(link)
				record = zip([ori_price, dis_priec, company_name, content, link, list(contacts)])
				result.append(record)
				print len(links_set), "scrped"

			else:
				print "page scraped before"
		except:
			print url
			failed_links.append(link)

	return result

if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding('utf8')
	lst_urls = ['https://www.groupon.com/browse/new-york?category=health-and-fitness&category2=sports&page={}'.format(i) for i in range(1,17)] 
	links_set = set(list())
	old_len = 0
	new_len = 1
	failed_links = list()

	with open('sports_contacts', "a") as csv_file:
		browser = webdriver.Chrome()
		while new_len > old_len:
			old_len = len(links_set)
			for url in lst_urls:
				result = list()
				result = handle_response(url,links_set,failed_links)
				writer = csv.writer(csv_file)
				writer.writerows(result)
				print len(failed_links), "links failed"
			new_len = len(links_set)
		for link in failed_links:
			csv_file.write(link+'\n')
