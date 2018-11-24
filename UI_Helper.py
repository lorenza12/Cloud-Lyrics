from tkinter import filedialog
from tkinter import *
import Genius_Api as genius
import Web_Parser as web_parser
import Word_Counter as wc
import Wordcloud_Generator as wordcloud
import os
import platform


GENRE_CHOICES = ['0','1', '2', '3', '4', '5', '6','7','8','9', '10']
WORD_CHOICES = ['1', '2', '3', '4', '5']
REOPEN_CHOICES = ['1','2','3']
SAVE_OR_RECOLOR_CHOICES = ['1','2','3']

GENRE_SWITCH = {    
    '0': 'Spotify_Global',
    '1': 'Spotify_US',
    '2': 'iTunes',
    '3': 'Alternative',
    '4': 'Country',
    '5': 'Pop',
    '6': 'Rap',
    '7': 'Rock',
    '8': 'Metal',
    '9': 'Text_File'    
    }

def get_text_file():
    """Opens a explorer menu to select text file
       Args:        -
       Returns:     file path  
    """    
    root = Tk()
    root.withdraw()
    home = os.path.expanduser('~')
    root.filename = filedialog.askopenfilename(initialdir=home, title="Select file", defaultextension=".txt",
                                               filetypes=(
                                                   (".txt", "*.txt"), ("all files", "*.*")))

    root.destroy()
    return root.filename


def count_lyric_words(song_artist_list, genre, have_stop_words=False, have_curse_words=True):
    """Helper function to count create dictionary of lyric words and their frequencies
       Args:        sogn artist list, genre, contain stop words, contain curse words
       Returns:     json file holding all words and frequencies 
    """
    json_file_path_raw = ''
    json_file_path_filtered = ''

    # percent counter
    counter = 1
    for song_artist_pair in song_artist_list:

        progbar(counter, len(song_artist_list), 51)

        # print('+ Sending Json Request')

        json_request = genius.request_song_info(song_artist_pair[0], song_artist_pair[1])

        url = genius.check_for_song_url(json_request, song_artist_pair[1])

        try:
            # print('+ Scraping lyrics')
            lyrics = web_parser.scrape_song_url(url)

            # print('+ Cleaning lyrics of puncuation')
            cleaned_lyrics = web_parser.clean_lyrics(lyrics)

            # print('+ Counting words')

            raw_frequency_dict = wc.raw_word_count(cleaned_lyrics)
            word_frequency_dict = wc.word_count(cleaned_lyrics, have_stop_words, have_curse_words)

            if json_file_path_raw and json_file_path_filtered:

                # print('+ Reading previous json')

                previous_json_word_count = wc.read_word_dictionary_json(json_file_path_filtered)
                updated_json_word_count_dict = wc.update_json_count(previous_json_word_count, word_frequency_dict,
                                                                    raw_lyrics=False)

                previous_json_word_count_raw = wc.read_word_dictionary_json(json_file_path_raw)
                updated_json_raw_word_count_dict = wc.update_json_count(previous_json_word_count_raw,
                                                                        raw_frequency_dict, raw_lyrics=True)

                # print('+ Updated raw and cleaned json files')

            else:

                # print('+ Creating new json lyrics count file')

                json_file_path_filtered = wc.write_word_count_json(word_frequency_dict, raw_lyrics=False)
                json_file_path_raw = wc.write_word_count_json(raw_frequency_dict, raw_lyrics=True)

                # print('+ Json file created')

        except Exception as e:
            # print('- Couldnt find song ' + song_artist_pair[0] + ' by ' + song_artist_pair[1])
            # print('Skipping..\n')
            pass

        counter += 1

    # print('+ Writing raw json to excel')

    raw_json = wc.read_word_dictionary_json(json_file_path_raw)
    excel_file = wc.write_word_count_excel(raw_json, genre, song_artist_list)

    clean_json = wc.read_word_dictionary_json(json_file_path_filtered)

    return clean_json


def display_excel_files(excel_file_list):
    """Displays a menu choice for which excel file user would like to open
       Args:        List of excel files in a given directory
       Returns:     -
    """
    total_files = len(excel_file_list)
    counter = 1
    for file in excel_file_list:
        file_name_start = file.rfind("\\")
        file_name = file[file_name_start+1:]
        if counter < 10:
            print(str(counter)+")  " + file_name)
        else:
            print(str(counter)+") " + file_name)
        counter += 1
    print(str(total_files+1) + ")  Main Menu")


def get_word_choice():
    """Displays a menu on if the user would like to have stop words or curse words
       Args:        -
       Returns:     have stop words boolean, have curse words boolen 
    """
    word_option = 0

    while word_option not in WORD_CHOICES:
        clear_screen()
        display_options()
        word_option = input("\n>> Enter Option: ")

    if word_option == '1':
        have_stop_words = False
        have_curse_words = True

    elif word_option == '2':
        have_stop_words = True
        have_curse_words = False

    elif word_option == '3':
        have_stop_words = False
        have_curse_words = False

    elif word_option == '4':
        have_stop_words = True
        have_curse_words = True 

    elif word_option == '5':
        clear_screen()
        return None, None

    clear_screen()
    return have_stop_words, have_curse_words

def get_existing_excel_choice():
    """Displays a meny on if the user would like to recreate a word cloud
       from previous data.
       Args:        -
       Returns:     number the user selected 
    """
    display_existing_excel()
    recreate_option = input("\n>> Enter Option: ")
    clear_screen()
    while recreate_option not in REOPEN_CHOICES:
        display_existing_excel()
        recreate_option = input("\n>> Enter Option: ")
        clear_screen()

    return recreate_option

def progbar(curr, total, full_progbar):
    """Displays a porgress bar
       Args:        -
       Returns:     - 
    """
    frac = curr / total
    filled_progbar = round(frac * full_progbar)
    print('\r', '#' * filled_progbar + '-' * (full_progbar - filled_progbar), '[{:>7.2%}]'.format(frac), end='')


def clear_screen():
    """Clears the terminal screen based on the os running
       Args:        -
       Returns:     - 
    """
    try:
        if platform.system() == 'Windows':
            os.system('cls') 
        else:
            os.system('clear')

    except Exception as e:
        pass


def save_or_recolor(word_cloud):
    """Displays a menu to either save or recolor word cloud
       Args:        word cloud object
       Returns:     newly recolored word cloud object or nothing  
    """
    option = 0
    while option not in SAVE_OR_RECOLOR_CHOICES:
        clear_screen()
        display_save_or_recolor()
        option = input("\n>> Enter Option: ")

    if option == '1':
        recolored = wordcloud.recolor_word_cloud(word_cloud)
        return recolored

    elif option == '2':
        wordcloud.save_word_cloud(word_cloud)
        return None

    elif option == '3':
        return None



def display_save_or_recolor():
    print()
    print("---- Save or Recolor Word Cloud ----")
    print("1) Recolor Word Cloud")
    print("2) Save Word Cloud")
    print("3) Main Menu")

def display_header():
    print("#############################################")
    print("    Welcome to Word Cloud Generator 1.5.1\n")
    print("  create word clouds from musical genres or")
    print("      from any text file you would like")
    print("#############################################")


def display_menu():
    print()
    print("1) Create Word Cloud From Lyrics")
    print("2) Create Word Cloud From Text")
    print("3) Create Word Cloud From Previous Data")
    print("4) Open Word Cloud Excel Document")
    print("5) Help")
    print("6) Exit")


def display_genres():
    print()
    print("---- Create Word Cloud From Lyrics ----\n")
    print("0)  Spotify Global")
    print("1)  Spotify US")
    print("2)  iTunes Top 100")
    print("3)  Alternative")
    print("4)  Country")
    print("5)  Pop")
    print("6)  Rap")
    print("7)  Rock")
    print("8)  Metal")
    print("9)  Main Menu")

def display_previous_data_options():
    print()
    print("---- Create Word Cloud From Previous Data ----\n")
    print("0)   Spotify Global")
    print("1)   Spotify US")
    print("2)   iTunes Top 100")
    print("3)   Alternative")
    print("4)   Country")
    print("5)   Pop")
    print("6)   Rap")
    print("7)   Rock")
    print("8)   Metal")
    print("9)   Text File")
    print("10)  Main Menu")

def display_excel_genres():
    print()
    print("---- Open Word Cloud Excel Document ----\n")
    print("0)   Spotify Global")
    print("1)   Spotify US")
    print("2)   iTunes Top 100")
    print("3)   Alternative")
    print("4)   Country")
    print("5)   Pop")
    print("6)   Rap")
    print("7)   Rock")
    print("8)   Metal")
    print("9)   Text File")
    print("10)  Main Menu")

def display_options():
    print()
    print("---- Select An Option ----\n")
    print("1) Remove Stop Words")
    print("2) Remove Curse Words")
    print("3) Remove Stop Words and Curse Words")
    print("4) Count All Words")
    print("5) Main Menu")


def display_existing_excel():
    print()
    print("It looks like a word cloud was already generated today for this genre.")
    print("Would you like to recreate the word cloud for this existing data,")
    print("or redownload all the the lyrics? Please note, redownloading the lyrics")
    print("will be a much slower taks.")
    print()
    print("1) Recrete Word Cloud")
    print("2) Start Fresh Redownloading Lyrics")
    print("3) Main Menu")

def display_help():
    print()
    print("--------------------------------- Help ---------------------------------\n")
    print("This program allows you to create word clouds from the current top songs")
    print("for a given genre, or from a selected text file. When creating word clouds")
    print("from a genre, there are nine differnt options. The first two options are")
    print("based on spotify's top 200 most played songs for the United States or globally.")
    print("The other seven options are based on the top 100 songs according to iTunes")
    print("for the selected genre found here: http://www.popvortex.com/music/charts/")
    print("When creating a word cloud from a text file, the file must be in a .txt format")
    print("as other formats sometimes cause issues.")
    print()
    print("When creating a word cloud, there are four different options you may take")
    print("to customize the outcome of it. You can have the word cloud not include")
    print("stop words like 'you', 'a', 'the', and many other common words. ")
    print("This is the recommended option as the word cloud will be less interesting")
    print("if you choose to include these stop words. You also have the option to")
    print("remove curse words if you would like to make a clean word cloud as the")
    print("top 200 spotify songs often contain explicit words.")
    print()
    print("After the word cloud is generated, it will be displayed where you have")
    print("the option to save it. Please be patient as the word cloud is generating")
    print("as the speed it generates is dependent on your internet connection.")
    print("Once you are finished with the word cloud, you will be presented with the")
    print("option to save or recolor it. The save option is there in case you forgot")
    print("to save it prior to closing out if it so you don have to deal with the hassle")
    print("of having to regenerate the word cloud once again. The recolor option will")
    print("open a new word cloud with the same results but with differnt colors of")
    print("words in case you were not happy with the coloring the first time.")
    print()
    print("When the word cloud is being generated, an excel file is also created")
    print("that holds all of the words and their frequencies so a more in depth")
    print("look of the words can be seen. Inside this exccel file a tab is also")
    print("created that holds all of the songs and the artists that were used")
    print("to create the word cloud.")
    print("This excel file can be used later to recreate a word cloud if you want")
    print("to remake a word cloud based on previous top songs you had ran earlier")
    print("as all word clouds generate differently each time.")
    print("Any of these previous excel files can be opened through the program")
    print("by selecting the option '4) Open Word Cloud Excel Document' on the ")
    print("main menu.")
    print()
