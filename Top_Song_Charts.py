import requests
import csv
import Web_Parser as parser
import Directory_Navigator as DN
import logging

URL_SWITCH = {
    'Spotify_US':       'https://spotifycharts.com/regional/us/daily/latest/download',
    'Spotify_Global':   'https://spotifycharts.com/regional/global/daily/latest/download',
    'iTunes':           'http://www.popvortex.com/music/charts/top-100-songs.php',
    'Rock':             'http://www.popvortex.com/music/charts/top-rock-songs.php',
    'Metal':            'http://www.popvortex.com/music/charts/top-heavy-metal-songs.php',
    'Country':          'http://www.popvortex.com/music/charts/top-country-songs.php',
    'Rap':              'http://www.popvortex.com/music/charts/top-rap-songs.php',
    'Pop':              'http://www.popvortex.com/music/charts/top-pop-songs.php',
    'Alternative':      'http://www.popvortex.com/music/charts/top-alternative-songs.php'
}


def get_spotify_charts(url_case='Spotify_US'):
    """Returns filename of the spotify top charts.
	   Args:    url_case of spotify website
	   Returns: filename of downloaded file
	"""

    try:
        file_download = requests.get(URL_SWITCH[url_case], allow_redirects=True)

        file_out = DN.write_csv(url_case, file_download.content)
        # open(file_out, 'wb').write(file_download.content)

        return file_out

    except Exception as e:
        print(e)
        logging.basicConfig(filename='Cloud_lyrics.log', filemode='a', format='%(asctime)s - %(message)s',
                            datefmt='%b-%d-%Y %H:%M:%S')
        logging.error('Error downloading spotify charts: ' + URL_SWITCH[url_case])
        logging.error('------------------')
        logging.error("Exception occurred", exc_info=True)
        logging.error('------------------')


def parse_csv_to_song_artist(csv_file):
    """Returns a list of lists holding a song and the correspongding artist
	   Args:    csv file
	   Returns: list of song / artist lists
	"""
    song_artist_list = []
    csv_header = []
    line_counter = 0

    try:

        with open(csv_file, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            for row in csv_reader:
                if line_counter == 1:
                    csv_header = row
                if line_counter > 1:
                    position = row[0]
                    song_title = row[1]
                    artist = row[2]
                    streams = row[3]
                    url = row[4]

                    song_artist_list.append([song_title, artist])

                line_counter += 1

        return song_artist_list

    except Exception as e:
        print(e)
        logging.basicConfig(filename='Cloud_lyrics.log', filemode='a', format='%(asctime)s - %(message)s',
                            datefmt='%b-%d-%Y %H:%M:%S')
        logging.error('Error parsing spotify csv')
        logging.error('------------------')
        logging.error("Exception occurred", exc_info=True)
        logging.error('------------------')


def parse_charts_to_song_artist(url_case='Rock'):
    """Returns a list of lists holding songs and their corresponding artists.
	   Args:    url case (Rock, Country..)
	   Returns: list of song / artist lists
	"""
    # call web parse
    try:
        charts_data = parser.parse_top_charts(URL_SWITCH[url_case])
        song_artist_list = []
        for item in charts_data:
            song = item[0]
            artist = item[1]

            song_artist_list.append([song, artist])

        return song_artist_list

    except Exception as e:
        # if word doesnt exit or error return none
        print(e)
        logging.basicConfig(filename='Cloud_lyrics.log', filemode='a', format='%(asctime)s - %(message)s',
                            datefmt='%b-%d-%Y %H:%M:%S')
        logging.error('Error making top charts url list')
        logging.error('------------------')
        logging.error("Exception occurred", exc_info=True)
        logging.error('------------------')

