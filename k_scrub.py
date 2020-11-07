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
  
trans_path = sys.argv[1]

domain = "https://kitsunekko.net"
sub_query = "/dirlist.php?dir=subtitles"
  
url = domain + sub_query
res = requests.get(url)

soup = BeautifulSoup(res.content, 'html.parser')

table_res = soup.find(id='flisttable') # id that points to the transcripts
trans_elem = table_res.find_all('a', class_='') # Using the table results, retrieve the rows with links to transcripts

anime_list = find_anime_list(trans_elem)

find_zip_files(anime_list, sys.argv[1])


'''
Get path to zip files for downloads.
'''

print("Downloading from Kistunekko.net...")

for zip_link in anime_list:
  zip_title = zip_link
  zip_url = domain + anime_list[zip_link]
  zip_res = requests.get(zip_url)

  soup = BeautifulSoup(zip_res.content, 'html.parser')

  table_res = soup.find(id='flisttable')
  trans_elem = table_res.find_all('a', class_='')

  for a_tag in trans_elem:
    trans_title = clean_html(str(zip_title))
    download_url = domain + "/" + a_tag["href"]
    download_files(download_url, trans_path + trans_title)

print("Download complete.")

dir_list = return_path_list(trans_path)

print("Decompressing files...")
decompress_files(dir_list, trans_path)
print("Done!")


'''Check if directory exists. If not, create one. '''
def check_path(file_path):
  if not os.path.exists(file_path):
    print(f"creating dir: {file_path}")
    os.mkdir(file_path)
    
def getListOfFiles(dir_path):

    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dir_path)
    allFiles = list()

    # Iterate over all the entries
    for entry in listOfFile:

        # Create full path
        fullPath = os.path.join(dir_path, entry)

        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles
  
'''extract files from zip, rar, and .7zip files'''
def decompress_files(trans_folder, trans_path):

  for zip_file in trans_folder:
    if ((".rar" in zip_file) or (".zip" in zip_file) or (".7z" in zip_file)):
      save_to = os.path.splitext(zip_file)[0]
      check_path(save_to)

      with open(zip_file, "rb") as f:
        try:
          Archive(zip_file).extractall(save_to)
          os.remove(zip_file) # remove zip file

        except: # in case of a bad zip file or magic number error
          pass
        
''' Gets a list of directories and subdirectories of the give path'''
def return_path_list(file_path):
  path_list = getListOfFiles(file_path)
  path_list = list()

  for (dirpath, dirnames, filenames) in os.walk(file_path):
      path_list += [os.path.join(dirpath, file) for file in filenames]

  return path_list

'''
Download file from kisunekko

Dir: where to store the download
URL: link to download the transcripts
'''
def download_files(url, dir):
  zip_path = os.path.expanduser(dir)
  download_to = zip_path + "/"

  
  if not os.path.exists(zip_path):
      os.makedirs(zip_path)
      try:
        wget.download(url=url, out=download_to)

      except:
        pass

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
