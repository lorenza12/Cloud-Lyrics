from wordcloud import WordCloud, STOPWORDS
from Word_Counter import *
from tkinter import filedialog
from tkinter import *
import matplotlib.pyplot as plt
from Stop_Words import *
import logging
import time


def generate_word_cloud(word_count_dictionary, max_words=1000, max_font_size=None, min_font_size=5, background='black'):
    """Returns a word cloud object 
       Args:        dictionary of most frequent used words
       Optional:    max_words, max_font_size, min_font_size, background
       Returns:     wordcloud object  
    """

    word_cloud = WordCloud(width = 800,
                          height = 400, 
                          max_words = max_words,
                          relative_scaling = 0.5,
                          normalize_plurals = False,
                          prefer_horizontal = 0.7, 
                          scale = 5, 
                          background_color = background,
                          max_font_size = max_font_size,
                          min_font_size = min_font_size).generate_from_frequencies(word_count_dictionary)

    plt.figure( figsize=(18,10), facecolor='k')
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.title('Word Cloud')
    plt.tight_layout(pad=0)
    plt.show()

    return word_cloud

def save_word_cloud(word_cloud):
    """Opens a explorer to save a word cloud
       Args:        word cloud object
       Returns:     -
    """
    try:
        root = Tk()
        root.withdraw()
        file = filedialog.asksaveasfile(mode='w', 
                                        defaultextension=".png", 
                                        filetypes=( ('PNG Image', '*.png'), 
                                                    ('JPEG Image', '*.jpeg'),
                                                    ('All Files', '*.*')))
        if (file is None): # asksaveasfile return `None` if dialog closed with "cancel".
            return

        print("\nSaving Word Cloud..")
        cloud_save = word_cloud.to_file(file.name)
        root.destroy()
        file.close() # `()` was missing.

    except Exception as e:

        print("There was a problem when trying to save the word cloud")
        time.sleep(3)



def recolor_word_cloud(word_cloud):
    """Recolors a previously made wordcloud
       Args:    wordcloud object
       Returns: -
    """
    try:
        word_cloud.recolor()
        plt.figure( figsize=(18,10), facecolor='w')
        plt.imshow(word_cloud.recolor())
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.show()

        return word_cloud

    except Exception as e:
        #if word doesnt exit or error return none
        print(e)
        logging.basicConfig(filename = 'Cloud_lyrics.log', filemode='a', format='%(asctime)s - %(message)s', datefmt='%b-%d-%Y %H:%M:%S')
        logging.error('Error recoloring wordcloud')
        logging.error('------------------')
        logging.error("Exception occurred", exc_info=True)
        logging.error('------------------')

