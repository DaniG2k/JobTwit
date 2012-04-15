#! /usr/bin/env python
# -*- coding: utf-8 -*-
 
import urllib, simplejson

"""
Twitter job search for programmers
Author: Dani
License: Creative Commons CC BY-NC-SA license
Date: mid-April 2012
"""

q = ['PHP', 'Python', 'Java',
	'Objective C', 'C', 'C++', 'C#',
	'SQL', 'MySQL', 'Ruby',
	'JavaScript', 'Action Script', 'ASP']

t = {}			# Dictionary of Tweets
links = []		# The links within the tweets

def getTweets(q):
	seed = "http://search.twitter.com/search.json?q=Job%20"
	rtype = '&result_type=mixed'
	pages = npages()	# The number of pages we inspect (max 15)
	rpp = 100			# The number of results per page we inspect (max 100)
	while pages >= 1:
		search = urllib.urlopen(seed+q+'&rpp='+str(rpp)+'&page='+str(pages)+rtype)
		dict = simplejson.loads(search.read())
		for result in dict["results"]: # Result is a list of dictionaries
			groupTweets(result['text'], result['from_user'])
		pages -= 1

# This function groups identical Tweets to avoid having them being 
# reprinted on the screen.
def groupTweets(tweet, user):
	if tweet in t:
		t[tweet][0] += 1
		t[tweet][1].append(user)
	else:
		t[tweet] = [1, [user]]
	return t

# Gives statistics of the various programming languages.
# Number of jobs per language and estimated language popularity.
def lang_stats():
	print 'Gathering statistics... this may take a few minutes'
	stats = {}
	for lang in q:
		global t
		t = {}
		c = 0
		getTweets(lang)
		for k in t:
			if lang.lower() in k.lower():
				c += 1
		stats[lang] = c
	totaljobs = 0
	for key in stats:
		totaljobs += stats[key]
	print '\nEstimated Popularity:'
	for key, val in sorted(stats.iteritems(), key=lambda (k,v): (v,k)):
		popularity = round(val / float(totaljobs) * 100, 2)
		if popularity < 10:
			if len(str(popularity)) >= 4:
				tabs = '\t\t'
		else:
			tabs = '\t'
		print '(' + red(str(popularity)) + '%)' + tabs + yellow(key) + \
		' = ' + green(str(val)) + ' jobs'

def parseTweets(query):
	getTweets(query)
	c = 0
	for k in t:
		if 'http' in k:
			get_urls(k)
		if t[k][0] == 1:
			print t[k][0],'Tweet)'
			print '\t' + green(k)
			c += 1
		else:
			print t[k][0],'Tweets)'
			print '\t' + green(k)
			c += t[k][0]
		if len(t[k][1]) == 1:
			print '\t' + yellow('User:') + yellow(t[k][1]) + '\n'
		else:
			print '\t' + yellow('Users:') + yellow(t[k][1]) + '\n'
	print 'Query: ' + red(query)
	print 'Total tweets scanned: ' + red(c)

# Prettify :D
def green(s):
	return '\033[1;32m%s\033[1;m' % s

def yellow(s):
	return '\033[1;33m%s\033[1;m' % s

def red(s):
	return '\033[1;31m%s\033[1;m' % s

def clear():
	print('\x1B[2J')

# Validate user input.
def check_lang(n):
	n -= 1
	prompt = 'Enter a number from 1 to %s:\n---> ' % n
	while True:
		try:
			i = int(raw_input(prompt))
			if n >= i >= 1:
				return i
		except ValueError:
			print 'Only a number from 1 to',n,'can be input.'

def npages():
	print '\nHow many pages of Tweets should I scan?'
	print 'Maximum is 15 pages (1500 Tweets)'
	prompt = '---> '
	while True:
		try:
			i = int(raw_input(prompt))
			if i > 15 or i < 1:
				print 'I can only scan 1 to 15 pages of Tweets.'
			else:
				return i
		except ValueError:
			print 'Only a value from 1 to 15 is accepted here.'
		

def check_location():
	print '\nWould you like to specify a location? (ex. NYC, London)'
	print '1) No\n2) Yes'
	prompt = '---> '
	while True:
		try:
			i = int(raw_input(prompt))
			if i == 1:
				return ''
			elif i == 2:
				s = 'What location should be searched?\n---> '
				loc = str(raw_input(s))
				return loc
			else:
				print 'Only a value of 1 oe 2 is accepted here.'
		except ValueError:
			print 'Only a value of 1 or 2 is accepted here.'

def crawl_urls(l):
	list_length = len(l)
	if list_length > 0:
		print '\n\nI\'ve collected a ' + \
		green('list of ' + str(list_length) + ' links ') + 'from the above Tweets'
		print '\nI can tell you more about them.'
		print 'Would you like me to look through the collected URLs?'
		print '1) No\n2) Yes'
		prompt = '---> '
		while True:
			try:
				i = int(raw_input(prompt))
				if i == 1:
					print 'Exiting!'
					break
				elif i == 2:
					print 'Ok! Scanning...'
					counter = 1
					total = str(len(l))
					for e in l:
						print '\n' + str(counter) + '/' + total + ')'
						counter += 1
						handle = urllib.urlopen(e)
						page = handle.read()
						if '<title>' in page:
							t_start_pos = page.find('<title>')
							t_end_pos = page.find('</title>')
							title = page[t_start_pos + len('<title>'):t_end_pos]
							title.strip(' \t\n\r')
							print red('Title: ') + title
						handle.close()
						print yellow('URL: ') + e
					return False
				else:
					print 'Only a value of 1 or 2 is accepted here.'
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
	print green('\t\t\tWelcome to JobTwit! :D')
	print '\nWould you like to:'
	print '1) Query Twitter for a particlar programming language\n' + \
	'2) View general statistics'
	prompt = '---> '
	while True:
		try:
			i = int(raw_input(prompt))
			if i == 1:
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
						query = q[num] + ' ' + loc
					parseTweets(query)
					crawl_urls(links)
					break
			elif i == 2:
				lang_stats()
				break
			else:
				print 'Only a value of 1 oe 2 is accepted here.'
		except ValueError:
			print 'Only a value of 1 or 2 is accepted here.'

clear()
prompt()
