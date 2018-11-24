# Cloud Lyrics

Make a wordcloud of the current top 200 most popular songs on Spotify or for a given genre (alternative, rock, country, metal, pop, rap, iTunes top 100).

There is also an option to make a wordcloud with a selected text file.

In the making of the wordcloud, a set of stop words and explicit words can be filtered out to make a more interesting result. The list of stop words can be found in the Stop_Words.py file, and words can be added or removed to change the results of the wordcloud. 

If you wish to see the numerical results of the words used and their frequencies, the program will also output an excel file holding all of the information, including the stop words. 

The excel file can be found in the Excel_Results folder inside the category (Spotify Global, Spotify US) or genre (Rock, Country, etc.) that the program was ran on. The excel files can also be accessed through the program.

The current Spotify charts list can be found [here](https://spotifycharts.com/regional/us/weekly/latest).

The top charts for a given genre is based of the results found on [popvortex.com](http://www.popvortex.com/music/charts/).

*Important Notes*
- The speed of the program is dependent on your internet connection, as a request is sent for each song to get the lyrics - please **Be Patient**
- Lyrics are not always found for every song, so the results may very depending on how many songs where found/not found.



## Getting Started

Clone the project down and follow the prerequisites and installation guide to set up a genius account and to also get the python modules needed in order to run Cloud Lyrics. 


### Prerequisites

This program was written using python 3.6.7. To use the program, you must download it from [here](https://www.python.org/downloads/)

In order to run the program, you will need the python modules found in the Requirements.txt file.

This can be simply done by navigating a command prompt to the location of the requirements.txt file and entering the command 
```
py -3.6 -m pip install -r Requirements.txt
```

Sometimes an error occures when trying to install the modules, and the fix I found was to install microsoft build tools from [visualstudio.microsoft.com](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

#### Getting Authorization Bearer
The lyrics are found using the genius api. You will need to create and account and authorize your account to get your own authorization bearer code. This can be done [here](https://docs.genius.com/). After creating an account, there will be a button on the right side of the documentation page that says 'Authorize'. Clicking the button will open a new tab to authorize your account. After authorizing your account and going back to the docs page, there will now be a authorization bearer code and also a button to 'Try It'. Copy the authorization bearer code and open Genius_Api.py file and paste in the code where it says '<PLACE AUTHORIZATION BEARER CODE HERE>'. Save the file and you should now be able to run it. 

## Running Cloud Lyrics

Open a command window and navigate to the directory of of the Main.py file. Execute the program using the following command:
```
py -3.6 Main.py
```


### Example Results

![Word Cloud](/Spotify_US.png)


## Version

* 1.5.1

## Author

* **Alik Lorenz**


## Acknowledgments

* Jack Schultz : [Getting Song Lyrics](https://bigishdata.com/2016/09/27/getting-song-lyrics-from-geniuss-api-scraping/)

