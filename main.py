#!./venv/bin/python

import re
import requests
from bs4 import BeautifulSoup
from os import path

download_page = 'https://blogs.msdn.microsoft.com/mssmallbiz/2016/07/10/free-thats-right-im-giving-away-millions-of-free-microsoft-ebooks-again-including-windows-10-office-365-office-2016-power-bi-azure-windows-8-1-office-2013-sharepoint-2016-sha/'
download_href_host = 'ligman.me'
download_directory = path.expanduser('~/downloads')

def __download_file__(url, file):
	if path.exists(file):
		print("Resuming:", url, "to", file)
		resume_header = {'Range': 'bytes=%d-' + str(path.getsize(file))}
		r = requests.get(url, stream=True, headers=resume_header)
		write_mode = 'ab'
	else:
		print("Downloading:", url, "to", file)
		r = requests.get(url, stream=True)
		write_mode = 'wb'
	with open(file, write_mode) as f:
		for chunk in r.iter_content(chunk_size=1024):
			if chunk:
				f.write(chunk)

if __name__ == '__main__':
	result = requests.get(url=download_page)
	source_html = result.text
	soup = BeautifulSoup(source_html, 'html.parser')
	links = soup.find_all('a')
	url_regex = re.compile('.*\\.\\w{3,}')
	for link in links:
		current_url = link.get('href')
		if download_href_host in current_url:
			response = requests.get(current_url, allow_redirects=False)
			if 'Location' in response.headers:
				redir_url = response.headers['Location']
				redir_filename = redir_url.split('/')[-1]
				if url_regex.match(redir_filename):
					__download_file__(current_url, path.join(download_directory, redir_filename))
					