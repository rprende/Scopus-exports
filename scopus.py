import requests
import csv
from csv import DictReader
from csv import DictWriter 
from BeautifulSoup import BeautifulSoup
import sys

links = []
with open(str(sys.argv[1]), 'rb') as f:
	reader = DictReader(f)
	for row in reader:
		link = row.get('Link')
		links.append(link)

def getAuthor(author, entry):
	if author[-31:] == 'View Correspondence (jump link)':
		print author[0:-31]
		entry['Author'] = author[0:-31]
		return 
	else:
		print author
		entry['Author'] = author
		return 

def getTitle(title, entry):
	t = ''
	if title[-13:] == '(Open Access)':
		t = title[0:-13]
	else:
		t = title
	t2 = ''
	if t[-9:] == '(Article)':
		t2 = t[0:-9]
	else:
		t2 = t
	entry['Title'] = t2
	return

def getDate(date, entry):
	date = date.split(',')
	for d in date:
		months = ['December','November','October','September','August','July','June','May','April','March','February','January']
		for month in months:
			if month in d:
				entry['Publication Date'] = d
				return
	
entries = []
for link in links:
	entry = {}
	r = requests.get(link)
	data = r.content
	html = BeautifulSoup(data)
	date = html.body.find('span', attrs={'id':'journalInfo'}).text
	getDate(date, entry)
	title = html.body.find('h2', attrs={'class':'h3'}).text
	getTitle(title, entry)
	author = html.body.find('section', attrs={'id':'authorlist'}).text
	getAuthor(author, entry)
	entry['Link'] = link
	entries.append(entry)


keys = ['Title', 'Author', 'Publication Date', 'Link']
f = open(str(sys.argv[2]), 'wb') 
writer = DictWriter(f, keys)
writer.writeheader()
for entry in entries:
	writer.writerow(entry)


















