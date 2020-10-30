{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "anime-match.ipynb",
      "provenance": [],
      "collapsed_sections": []
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "XVLWLFLMnUwC"
      },
      "source": [
        "# Anime Match\n",
        "----\n",
        "A classification model that uses transcipts from Anime to filter out specific themes. \n",
        "\n",
        "## The Problem\n",
        "---\n",
        "What do we consider when choosing anime? Genre, art style, content length, and popularity are typically what we think about.\n",
        "\n",
        "Current recommendation systems that only filter by broad genre tags allow for specific themes to slip through and also close of entire categories for general thematic elements that are assumed. Broad genres, including horror and fantasy, may include several anime that deal with death and supernatural elements. Any individual that wished to not see either of these categories may eliminate the broad genre, where several shows in that genre don’t deal with either theme. \n",
        "\n",
        "Alternatively, there are several instances where an anime may be tagged by a traditionally light- hearted genre but do include darker themes. For example, the anime “Your Lie in April” is included in the romance genre overall but regularly includes themes of death from the main character’s relative passing to one of the main characters passing by the finale. By focusing on a thematic filter, we can add to existing recommendation systems to better the experience of anime enthusiasts, both by reducing the amount of anime with minor mentions of exclusionary themes to slip through due to their overarching genre tags, and by broadening the available recommendations with previously excluded larger genres.\n",
        "\n",
        "## The Big Picture\n",
        "----\n",
        "Although the classification model we are building is Anime, it could also be applied to Manga, TV shows, books, newspapers, and other content. This model could also be used for parental control for children when they are searching the internet and watching Netflix.\n",
        "\n",
        "## Dataset\n",
        "---\n",
        "The datasets uses in this project are raw transcripts from [Kistunekko](https://kitsunekko.net). It contains transcripts from over 2000 anime in 4 languages: English, Japanese, Chinese, and Korean. For the purposes of this project, we will be sticking with English.\n",
        "\n",
        "Transcipts can be found in the /content/transcripts path.\n"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "YSkXblo2pVQI",
        "outputId": "7a4184cb-9ac1-4af5-8f53-36ad6c2eb71e",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "source": [
        "# run this to import from google drive\n",
        "from google.colab import drive\n",
        "drive.mount('/content/drive/') "
      ],
      "execution_count": 1,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "Mounted at /content/drive/\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "KKBArgmGriIb"
      },
      "source": [
        "import os\n",
        "import requests\n",
        "from pprint import pprint"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "OBTlfDzDBhXR"
      },
      "source": [
        "### I. Web Scraper\n",
        "First, we need to build a webscrapper for the kisunekko.net site! Here are our steps:\n",
        "\n",
        "(1) Build webscrapper using BeautifulSoup\n",
        "\n",
        "(2) We will retreive all zip files from each anime listed.\n",
        "\n",
        "(3) Extract all transcripts from each compressed files and lastly,\n",
        "\n",
        "(4) Remove leftover compressed files to save some space"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "YorlMf_EqhJ8",
        "outputId": "a67e110a-955e-435d-9d1e-6ee80f5fe513",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "source": [
        "'''\n",
        "Web-scraper for kistunekko.net\n",
        "'''\n",
        "\n",
        "domain = \"https://kitsunekko.net\"\n",
        "sub_query = \"/dirlist.php?dir=subtitles\"\n",
        "url = domain + sub_query\n",
        "res = requests.get(url)\n",
        "\n",
        "res"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "<Response [200]>"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 5
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "QCvK8S3e4r2X"
      },
      "source": [
        "from bs4 import BeautifulSoup\n",
        "\n",
        "soup = BeautifulSoup(res.content, 'html.parser')\n",
        "\n",
        "table_res = soup.find(id='flisttable') # id that points to the transcripts\n",
        "trans_elem = table_res.find_all('a', class_='') # Using the table results, retrieve the rows with links to transcripts"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "PxVQKrNBBdWY"
      },
      "source": [
        "import re\n",
        "\n",
        "''' Strip html tags from text '''\n",
        "def clean_html(raw_html):\n",
        "  strip_tags = re.compile('<.*?>')\n",
        "  clean_text = re.sub(strip_tags, '', raw_html)\n",
        "  return clean_text\n",
        "  "
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "pv2SBFNpCduX"
      },
      "source": [
        "'''\n",
        "Each Anime has a title and a link for download\n",
        "'''\n",
        "anime_list = {}\n",
        "for a_tag in trans_elem:\n",
        "    title_elem = a_tag.find('strong', class_='')\n",
        "    title = clean_html(str(title_elem))\n",
        "    anime_list[title] = a_tag[\"href\"]"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "s8vyjyyyM889",
        "outputId": "e9e0246e-0628-4712-c223-6fb6409196c2",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "source": [
        "print(f\"Total Anime: {len(anime_list.keys())}\")"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "Total Anime: 2000\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "uWDjT16OcO-X"
      },
      "source": [
        "import wget\n",
        "\n",
        "'''\n",
        "Download file from kisunekko\n",
        "\n",
        "Dir: where to store the download\n",
        "URL: link to download the transcripts\n",
        "'''\n",
        "def download_files(url, dir, title):\n",
        "  dir = os.path.expanduser(dir)\n",
        "  if not os.path.exists(dir):\n",
        "      os.makedirs(dir)\n",
        "\n",
        "  print(\"\\nDownloading kitsunekko transcripts...\")\n",
        "\n",
        "  if os.path.exists(os.path.join(dir, title)):\n",
        "      print(file, \"already downloaded\")\n",
        "  else:\n",
        "      wget.download(url=url, out=dir)\n",
        "\n",
        "  print(\"Download completed!\")"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "SmOJ86UhVYjp"
      },
      "source": [
        "'''Get path to zip files for downloads.'''\n",
        "\n",
        "trans_path = \"/content/drive/My Drive/Colab Notebooks/transcripts/\" # where to store the transcripts\n",
        "\n",
        "for zip_link in anime_list:\n",
        "  zip_url = domain + anime_list[zip_link]\n",
        "  zip_res = requests.get(zip_url)\n",
        "\n",
        "  soup = BeautifulSoup(zip_res.content, 'html.parser')\n",
        "\n",
        "  table_res = soup.find(id='flisttable')\n",
        "  trans_elem = table_res.find_all('a', class_='')\n",
        "\n",
        "  for a_tag in trans_elem:\n",
        "    title_elem = a_tag.find('strong', class_='')\n",
        "    trans_title = clean_html(str(title_elem))\n",
        "\n",
        "    download_url = domain + \"/\" + a_tag[\"href\"]\n",
        "\n",
        "    download_files(download_url, trans_path, anime_list[zip_link])"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "KryUHNRVdm9u"
      },
      "source": [
        "'''extract files from zip, rar, and .7zip files'''\n",
        "from pyunpack import Archive\n",
        "import sys\n",
        "import subprocess\n",
        "\n",
        "trans_folder = os.listdir(trans_path) # get files from the transcript directory\n",
        "\n",
        "for file in trans_folder:\n",
        "    if (\".rar\" in file or \".zip\" in file or \".7z\" in file):\n",
        "      print(file, \"will be unpacked\")\n",
        "      print(trans_path)\n",
        "\n",
        "      with open(trans_path + file, \"rb\") as f:\n",
        "        try:\n",
        "          Archive(trans_path + file).extractall(trans_path)\n",
        "        except: # in case of a bad zip file or magic number error\n",
        "          pass"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "7m1oOwX7tfUb"
      },
      "source": [
        "'''remove any compressed files'''\n",
        "for item in trans_folder:\n",
        "    if item.endswith(\".zip\" or \".7z\" or \".rar\"):\n",
        "      try:\n",
        "        os.remove(trans_path + item)\n",
        "      except:\n",
        "        pass"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "MoKW4Qgv24rY"
      },
      "source": [
        ""
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "Ph1sk1KD8cYd"
      },
      "source": [
        "## II. Random Generator\n",
        "This will be used to randomly select the anime we will train the model on!\n",
        "\n"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "VsrjWOtr8_V8"
      },
      "source": [
        ""
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "cJmcEm3n8wNt"
      },
      "source": [
        "## III. Clean Transcripts\n",
        "After randomly selecting the anime, we will select 10 episodes from each anime and run it through the parser."
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "lHfHWVc08o4F"
      },
      "source": [
        ""
      ],
      "execution_count": null,
      "outputs": []
    }
  ]
}