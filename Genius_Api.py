import requests
import logging

AUTHORIZATION_BEARER =  '<PLACE AUTHORIZATION BEARER CODE HERE>'


BASE_URL = 'https://api.genius.com'
 
def request_song_info(song_title, artist_name):
	"""Returns a response message from genius api looking for song
       Args:    song and artist
       Returns: response json data
    """
	try:
		headers = {'Authorization': 'Bearer ' + AUTHORIZATION_BEARER}
		search_url = BASE_URL + '/search'
		data = {'q': song_title + ' ' + artist_name}
		response = requests.get(search_url, data=data, headers=headers)

		return response.json()
	except Exception as e:
		logging.basicConfig(filename = 'Cloud_lyrics.log', filemode='a', format='%(asctime)s - %(message)s', datefmt='%b-%d-%Y %H:%M:%S')
		logging.error('Error making genius api url')
		logging.error('------------------')
		logging.error("Exception occurred", exc_info=True)
		logging.error('------------------')


def check_for_song_url(json_data, artist):
	"""Returns a response message from genius api looking for song
       Args:    json response data, artist to check for specific song
       Returns: url of found lyrics at genius.com
    """
	remote_song_info = None

	try:
		for hit in json_data['response']['hits']:
			if artist.lower() in hit['result']['primary_artist']['name'].lower():
				remote_song_info = hit
				break

		if remote_song_info:
			song_url = remote_song_info['result']['url']
			return song_url

	except Exception as e:
		logging.basicConfig(filename = 'Cloud_lyrics.log', filemode='a', format='%(asctime)s - %(message)s', datefmt='%b-%d-%Y %H:%M:%S')
		logging.error('Error checking for song url')
		logging.error('------------------')
		logging.error("Exception occurred", exc_info=True)
		logging.error('------------------')
