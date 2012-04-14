#! /usr/bin/env python
# -*- coding: utf-8 -*-
 
import urllib
import simplejson

"""
Twitter job search for programmers
Author: Dani
License: Creative Commons CC BY-NC-SA license
Date: mid-April 2012
"""

t = {}			# Dictionary of Tweets
pages = '3'		# The number of pages of tweets we want to inspect
rpp = '100'		# Results per page

q = ['PHP', 'Python', 'Java',
	'Objective C', 'C', 'C++', 'C#',
	'SQL', 'Android', 'Ruby', 'JavaScript',
	'Action Script', 'ASP']

links = []		# The links within the tweets

def searchTweets(query):
	search = urllib.urlopen("http://search.twitter.com/search.json?q=Job%20"+query+'&rpp='+rpp+'&page='+pages)
	dict = simplejson.loads(search.read())
	for result in dict["results"]: # Result is a list of dictionaries
		floatTweets(result['text'], result['from_user'])
	c = 0
	for k in t:
		if 'http' in k:
			get_urls(k)
		if t[k][0] == 1:
			print t[k][0],'Tweet)'
			print '\t\033[1;32m%s\033[1;m' % k
			c += 1
		else:
			print t[k][0],'Tweets)'
			print '\t\033[1;32m%s\033[1;m' % k
			c += t[k][0]
		if len(t[k][1]) == 1:
			print '\t\033[1;33mUser:',t[k][1],'\033[1;m\n'
		else:
			print '\t\033[1;33mUsers:',t[k][1],'\033[1;m\n'
	print 'Query: \033[1;31m%s\033[1;m' % query
	print 'Total tweets scanned:',c # This number is not necessarily the same as
									# the number entered in variable qnum. Sometimes
									# there simply aren't that many tweets to scan.

# This function groups identical Tweets to avoid having them being 
# reprinted on the screen.
def floatTweets(tweet, user):
	if tweet in t:
		t[tweet][0] += 1
		t[tweet][1].append(user)
	else:
		t[tweet] = [1, [user]]
	return t

# Validate user input.
def check_lang(n):
	n -= 1
	prompt = 'Enter a number from 1 to %s:\n--->' % n
	while True:
		try:
			i = int(raw_input(prompt))
			if n >= i >= 1:
				return i
		except ValueError:
			print 'Only a number from 1 to',n,'can be input.'

def check_location():
	print '\nWould you like to specify a location? (ex. NYC, London)'
	print '1) No\n2) Yes'
	prompt = '--->'
	while True:
		try:
			i = int(raw_input(prompt))
			if i == 1:
				return ''
			elif i == 2:
				s = 'What location should be searched?\n--->'
				near = '&near:'
				loc = str(raw_input(s))
				loc = near + loc
				return loc
			else:
				print 'Only a value of 1 oe 2 is accepted here.'
		except ValueError:
			print 'Only a value of 1 or 2 is accepted here.'

def scan_urls(l):
	print '\n\nI\'ve collected a \033[1;32mlist of ' + str(len(links)) + ' URLs\033[1;m from the above Tweets'
	print '\nI can tell you the page title and give a brief description.'
	print 'Would you like me to look through the collected URLs?'
	print '1) No\n2) Yes'
	prompt = '--->'
	while True:
		try:
			i = int(raw_input(prompt))
			if i == 1:
				break
			elif i == 2:
				print 'Ok! Scanning...'
				c = 1
				for e in l:
					print '\n' + str(c) + '/' + str(len(l)) + ')'
					c += 1
					handle = urllib.urlopen(e)
					page = handle.read()
					if '<title>' in page:
						t_start_pos = page.find('<title>')
						t_end_pos = page.find('</title>')
						title = page[t_start_pos + len('<title>'):t_end_pos]
						title.strip(' \t\n\r')
						print '\033[1;31mTitle: \033[1;m' + title
					handle.close()
					print '\033[1;33mURL:\033[1;m ' + e
				return False
			else:
				print 'Only a value of 1 oe 2 is accepted here.'
		except ValueError:
			print 'Only a value of 1 or 2 is accepted here.'

# Make a list of all the URLs in the tweets we found
def get_urls(s):
	l = s.split()
	for e in l:
		if 'http' in e:
			links.append(e)
	
# Prompt the user for the Tweets to search for.
def prompt():
	print 'What language would you like to search for?'
	i = 1
	for entry in q:
		print i,')',entry
		i += 1
	num = check_lang(i) - 1
	loc = check_location()
	if loc == '':
		query = q[num]
	else:
		query = q[num] + loc
	searchTweets(query)
	scan_urls(links)

prompt()
