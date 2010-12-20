#!/usr/bin/python

import os
import urllib
from BeautifulSoup import BeautifulSoup


f = open('Tumblelog Backup Tool.html', 'r')

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
		elif char_month == "June":
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

for link in soup.findAll(attrs={"id" : "post"}):
	target_url = link.find('a')
	font = link.find('font')
	year = font.find('a').contents[0][13:-9]
	day =  font.find('a').contents[0][6:-18]
	month = convert_month(font.find('a').contents[0][9:-14])
	title = target_url.contents[0].replace('/', '').replace('|','').replace(',','').replace('.','')
	title = title.replace('[','').replace(']','').replace(':','').replace('~','').replace('\'','')
	title = title.replace('(','').replace(')','').replace('%','').replace('#','').replace('---','-').replace('--','-')
	slug = title.replace(' ', '-').lower().replace('---','-')
	try : 
		tags = link.find(attrs={"id" : "tags"}).contents[0][13:]
	except (NameError, AttributeError):
		tags = ""
	
	lines = []
	#---------------------------------
	lines.append("---\n")
	lines.append("title: %s\n" % (title))
	lines.append("date: %s/%s/%s\n" % (year, month, day))
	lines.append("tags: %s\n" % (tags))
	lines.append("slug: %s\n" % (slug))
	lines.append("old_url: %s\n" % (font.find('a')['href']))
	lines.append("new_url: %s/%s/%s/%s/\n" % (year, month, day, slug))
	lines.append("\n")
        lines.append('<p><a href="%s">%s</a></p> <p>%s</p>\n' % (target_url['href'], target_url['href'], target_url.contents[0]))
	o = open("links/%s-%s-%s-%s.txt" % (year, month, day, slug), "w")
	print slug
	o.writelines(lines)
	o.close()
f.close()
