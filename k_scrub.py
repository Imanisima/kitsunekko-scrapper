import os
import requests
from bs4 import BeautifulSoup
import re
import wget

if sys.argv[1] = "" or None:
  print("Please enter a path to store transcripts: ")
  print("Ex: k_scrub.py path/to/folder")
  print("Terminating program...")
  sys.exit()

domain = "https://kitsunekko.net"
sub_query = "/dirlist.php?dir=subtitles"
  
url = domain + sub_query
res = requests.get(url)

soup = BeautifulSoup(res.content, 'html.parser')

table_res = soup.find(id='flisttable') # id that points to the transcripts
trans_elem = table_res.find_all('a', class_='') # Using the table results, retrieve the rows with links to transcripts

anime_list = find_anime_list(trans_elem)

find_zip_files(anime_list, sys.argv[1])


'''Get path to zip files for downloads.'''
def find_zip_files(anime_list, trans_path)

  for zip_link in anime_list:
    zip_url = domain + anime_list[zip_link]
    zip_res = requests.get(zip_url)

    soup = BeautifulSoup(zip_res.content, 'html.parser')

    table_res = soup.find(id='flisttable')
    trans_elem = table_res.find_all('a', class_='')

    for a_tag in trans_elem:
      title_elem = a_tag.find('strong', class_='')
      trans_title = clean_html(str(title_elem))

      download_url = domain + "/" + a_tag["href"]

      download_files(download_url, trans_path, anime_list[zip_link])

'''
Download file from kisunekko

Dir: where to store the download
URL: link to download the transcripts
'''
def download_files(url, dir, title):
  dir = os.path.expanduser(dir)
  if not os.path.exists(dir):
      os.makedirs(dir)

  print("\nDownloading kitsunekko transcripts...")

  if os.path.exists(os.path.join(dir, title)):
      print(file, "already downloaded")
  else:
      wget.download(url=url, out=dir) 

  print("Downloads finished!")

'''
Retrieve html tags holding the anime title and link
'''
def find_anime_list(trans_elem):

  anime_list = {}
  for a_tag in trans_elem:
      title_elem = a_tag.find('strong', class_='')
      title = clean_html(str(title_elem))
      anime_list[title] = a_tag["href"]

  return anime_list


''' Strip html tags from text '''
def clean_html(raw_html):
  strip_tags = re.compile('<.*?>')
  clean_text = re.sub(strip_tags, '', raw_html)
  return clean_text
