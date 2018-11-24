from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import logging
import requests
import re


def parse_top_charts(url_genre):
    """Returns a list of songs and the artist based on the genre passed in.
       Args:    url genre (top_songs URL_SWITCH)
       Returns: url list  - a list of lists that holds song and artist
    """

    try:
        # need header to spoof browser so the website doesn't block out bot
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        # send the request
        url_req = Request(url_genre, headers=header)

        # read request
        web_byte = urlopen(url_req).read()

        #print(web_byte.decode())

        webpage = web_byte.decode('utf-8')

        # parse html with BeautifulSoup import
        page_soup = soup(webpage, "html.parser")

        song_data_wrap = page_soup.find_all("div", {"class", "chart-content col-xs-12 col-sm-8"})


        artist_songs = []
        for data in song_data_wrap:
            artist = data.em.text
            song = data.a.text

            artist_songs.append([song, artist])

        return artist_songs


    except Exception as e:
        # if word doesnt exit or error return none
        print(e)
        logging.basicConfig(filename='Cloud_lyrics.log', filemode='a', format='%(asctime)s - %(message)s',
                            datefmt='%b-%d-%Y %H:%M:%S')
        logging.error('Error parsing url')
        logging.error('------------------')
        logging.error("Exception occurred", exc_info=True)
        logging.error('------------------')


def scrape_song_url(url):
    """Scrapes given url for lyrics
       Args:        url
       Returns:     lyrics string
    """
    page = requests.get(url)
    html = soup(page.text, 'html.parser')
    lyrics = html.find('div', class_='lyrics').get_text()

    # remove things like [Intro], [Verse 1: ], etc. from lyrics
    lyrics = re.sub(r"\[([A-Za-z0-9_:\s]+)\]", "", lyrics)

    return lyrics


def clean_lyrics(lyrics):
    """Returns lyrics that have had puncutation and newline characters removed.
       Args:    lyrics
       Returns: lyrics without punctuation or newline characters
    """
    lyrics = re.sub(r'[\[].*?[\]]', '', lyrics)  # remove all announcements ([Bridge], [Chorus], [Verse1], etc.)
    lyrics = re.sub(r'[^\w\s]', '', lyrics)  # remove all puncuation
    lyrics = lyrics.replace("\n", " ")  # replace newline characters with spaces, otherwise words are joined together
    lyrics = re.sub(' +', ' ', lyrics)  # remove extra spaces

    return lyrics.title()


