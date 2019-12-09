import newspaper
import traceback
import urllib.parse
import urllib.request
import ssl
import aiohttp
import asyncio
import os
import sys
import math
from aiohttp import ClientSession
import operator

#########################
#    Get Newspaper Article
#########################
def article_text(article_link,count):
	text = ''
	print(count)
	n_object = newspaper.Article(article_link)
	n_object.download()
	n_object.parse()
	try:
		source_url = '.'.join(urllib.parse.urlparse(n_object.source_url)[1].split('.')[-2:])
	except e:
		traceback.print_exc()
		source_url = 'undefined'
	text += "article is from " + source_url + " "
	article = n_object.text.replace("&","and").replace('\n','').replace('\t','').replace('.','. ')
	text += article
	return text

#########################
#    Get Html
#########################
def get_html(url):
	myssl = ssl.create_default_context();
	myssl.check_hostname=False
	myssl.verify_mode=ssl.CERT_NONE
	req = urllib.request.Request(url)
	req.add_header('Referer','www.google.com')
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36')
	req.add_header('Accept','*/*')
	# req.add_header('Accept-Encoding','gzip, deflate, sdch, br')
	req.add_header('Accept-Language','en-US,en;q=0.8')
	req.add_header('Connection','keep-alive')
	# req.add_header('Host','www.google.com')
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
	res = urllib.request.urlopen(req,context=myssl).read().decode()
	res = ''.join([x for x in res if ord(x) < 128])
	return res	

#########################
#    USING AIOHTTP
#########################
async def async_get_html(url):
	response = await aiohttp.request('GET', url)
	content = await response.text()
	return content

#########################
#    get item in iterable
#########################
def get_item(iterable, index, default=''):
	try:
		return operator.getitem(iterable, index).strip()
	except:
		return default

#########################
#    Message
#########################
def p(inquiry):
	os.system("cls")
	row_offset = math.floor(os.get_terminal_size()[1] / 3)
	print("\n" * row_offset)
	print("----------------------------")
	print(inquiry)
	print("----------------------------")
	print("\n")
	return input("> ")


def sanitize(word):
	return ''.join([x for x in str(word) if ord(x) < 128])
	
def file_get_contents(filename):
	f = open(filename, 'r', encoding="utf-8")
	r = f.read()
	r = sanitize(r)
	f.close()
	return r