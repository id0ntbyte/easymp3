#!/usr/bin/env python
"""
Created by id0ntByte
https://github.com/id0ntByte
"""
import sys, os, webbrowser, requests, youtube_dl, argparse
from bs4 import BeautifulSoup
from urllib.parse import quote
class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}
def just_download(url):
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([url])

def download_from_file(name):
	with open(name) as f:
		lines = f.readlines()
	for i in lines:
		query = quote(i)
		list = []
		res = requests.get('https://youtube.com/results?search_query=' + query)
		soup = BeautifulSoup(res.text, "html.parser")
		for index, vid in enumerate(soup.findAll(attrs={'class' : 'yt-uix-tile-link'})[:2]):
			temp_url = 'https://youtube.com' + vid['href']
			list.insert((index), temp_url)
		print("Downloading: " + vid['title'] + "\n")
		url = list[1]
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([url])
	exit()
	
#CONDITIONS
parser = argparse.ArgumentParser(description='Downloading and converting videos2mp3 made SIMPLE!')
parser.add_argument("Name", help='Put the name of the song and/or artist like so: "name of song"')
parser.add_argument("-s", "--size", type=int, help="How many options to show for download, (Default = 10)")
parser.add_argument("-a", "--auto", action="store_true", help="Run the script Automatic without asking for an option")
parser.add_argument("-u", "--url", action="store_true", help="Download custom URL to high quality mp3, NOTE: Pass URL for the Name variable")
parser.add_argument("-o", "--open", action="store_true", help="Open text file and download all songs seperated by line break, NOTE: Pass the file name for the Name variable, put TEXT file in the same folder as script")
args = parser.parse_args()
if args.size:
	list_size = args.size
elif args.size is None:
	list_size = 10
if args.Name:
	get_input = args.Name
if args.auto:
	run_auto = 1
elif args.auto is not 1:
	run_auto = 0
if args.url:
	just_download(args.Name)
if args.open:
	download_from_file(args.Name)
#-----------------------------------------------------------------
query = quote(get_input)
res = requests.get('https://youtube.com/results?search_query=' + query)
soup = BeautifulSoup(res.text, "html.parser")
url = ''
list = []
print('\n\n')
for index, vid in enumerate(soup.findAll(attrs={'class' : 'yt-uix-tile-link'})[:list_size], 1):
	if (run_auto is not 1):
		print(''+str(index)+'. ' + vid['title'])
	temp_url = 'https://youtube.com' + vid['href']
	list.insert((index), temp_url)
if run_auto is not 1:
	valid = 0
	while (valid == 0):
		choice = int(input('\nEnter your choice: '))
		if choice > 0 and choice < 11:
			valid = 1
		else:
			print('invalid choice, try again!')
	choice -=1
	url = list[choice]
elif run_auto == 1:
	url = list[1]
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	ydl.download([url])
