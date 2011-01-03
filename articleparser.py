#!/usr/bin/python

import os
import urllib
import markdown
from BeautifulSoup import BeautifulSoup

path = "/Users/matthew.finlayson/Desktop/"
f = open(os.path.join(path, 'Tumblelog Backup Tool.html'), 'r')

soup = BeautifulSoup(f)

def convert_month(char_month):
		if char_month == "Jan":
			return "01"
		elif char_month == "Feb":
			return "02"
		elif char_month == "Mar":
			return "03"
		elif char_month == "Apr":
			return "04"
		elif char_month == "May":
			return "05"
		elif char_month == "Jun":
			return "06"
		elif char_month == "Jul":
			return "07"
		elif char_month == "Aug":
			return "08"
		elif char_month == "Sep":
			return "09"
		elif char_month == "Oct":
			return "10"
		elif char_month == "Nov":
			return "11"
		elif char_month == "Dec":
			return "12"

for article in soup.findAll(attrs={"id" : "post"}):
	
	# Grab the date string, we cheat by using the font tag change to find it.
	# We have known lengths so we slice it up and run the 3 letter month through a converter
	font = article.find('font')
	year = font.find('a').contents[0][13:-9]
	day =  font.find('a').contents[0][6:-18]
	month = convert_month(font.find('a').contents[0][9:-14])

	# Grab the title out of the h2 and try to clean it up. 
	title = article.find('h2').contents[0]

	title = title.replace('[','').replace(']','').replace(':','').replace('~','').replace('\'','')
	title = title.replace('(','').replace(')','').replace('%','').replace('#','').replace('---','-').replace('--','-')
	
	# The slug is the the lowercase title spaced with hyphensq!
	
	slug = title.replace('&amp;', '').replace('?', '').replace('!', '').replace('+', '').replace('=', '').replace('.', '')
	slug = slug.replace(' ', '-').lower().replace('/', '-').replace('---','-').replace('--','')
	# We hope the post is tagged. If not we make it blank
	try : 
		tags = article.find(attrs={"id" : "tags"}).contents[0][13:]
	except (NameError, AttributeError):
		tags = ""
	
	article_body = article.findAll('p')
	
	lines = []
	#---------------------------------
	lines.append("---\n")
	lines.append("title: %s\n" % (title))
	lines.append("date: %s/%s/%s\n" % (year, month, day))
	lines.append("tags: %s\n" % (tags))
	lines.append("slug: %s\n" % (slug))
	lines.append("old_url: %s\n" % (font.find('a')['href']))
	lines.append("new_url: %s/%s/%s/%s/\n" % (year, month, day, slug))
	lines.append("content_type: text/html\n")
	lines.append("\n")
	for body_line in article_body:
		lines.append("%s" % body_line)
	o = open("articles/%s-%s-%s-%s.txt" % (year, month, day, slug), "w")
	o.writelines(lines)
	o.close()
	print slug

f.close()

