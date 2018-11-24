import Word_Counter as wc
import Wordcloud_Generator as wordcloud
import Top_Song_Charts as top_song
import Directory_Navigator as dir_nav
import UI_Helper as ui
import os
import time


def main():
    ui.display_header()
    dir_nav.check_for_directories()
    option = ""

    while option != "6":
        ui.clear_screen()
        ui.display_header()
        ui.display_menu()
        option = input("\n>> Enter Option: ")
        ui.clear_screen()

        if option == "1":
            ui.display_genres()
            genre_option = input("\n>> Enter Option: ")
            ui.clear_screen()
            while genre_option not in ui.GENRE_CHOICES:
                ui.display_genres()
                genre_option = input("\n>> Enter Option: ")
                ui.clear_screen()

                if genre_option == '9':
                    break


            if genre_option != '9':

                genre = ui.GENRE_SWITCH[genre_option]

                existing_excel = dir_nav.check_for_excel(genre)
                recreate_option = None
                if existing_excel != None:
                    recreate_option = ui.get_existing_excel_choice()
                    if recreate_option == '1':
                        have_stop_words, have_curse_words = ui.get_word_choice()

                        if have_stop_words != None and have_curse_words != None:
                            print("Creating Word Cloud..")
                            word_count_dictionary = wc.create_word_dictionary_from_excel(existing_excel, have_stop_words, have_curse_words)
                            cloud = wordcloud.generate_word_cloud(word_count_dictionary)

                            recolor_or_save = ui.save_or_recolor(cloud)
                            while recolor_or_save != None:
                                recolor_or_save = ui.save_or_recolor(recolor_or_save)



                    elif recreate_option == '2':
                        #Can pass because we just need to do the whole process
                        #which is done in the next if
                        pass

                if existing_excel == None or recreate_option =='2':
                
                    have_stop_words, have_curse_words = ui.get_word_choice()

                    if have_stop_words != None and have_curse_words != None:

                        if genre == 'Spotify_Global' or genre == 'Spotify_US':
                            charts = top_song.get_spotify_charts(genre)
                            song_artist_list = top_song.parse_csv_to_song_artist(charts)

                        else:
                            song_artist_list = top_song.parse_charts_to_song_artist(genre)


                        lyrics_counted_dictionary = ui.count_lyric_words(song_artist_list, genre, have_stop_words, have_curse_words)
                        cloud = wordcloud.generate_word_cloud(lyrics_counted_dictionary)

                        recolor_or_save = ui.save_or_recolor(cloud)
                        while recolor_or_save != None:
                            recolor_or_save = ui.save_or_recolor(recolor_or_save)

        elif option == "2":
            try:
                genre = 'Text_File'
                text_file_path = ui.get_text_file()

                if text_file_path != "":

                    have_stop_words, have_curse_words = ui.get_word_choice()

                    if have_stop_words != None and have_curse_words != None:

                        print("Creating Word Cloud..")
                        word_count_dictionary = wc.count_text_file_words(text_file_path, have_stop_words, have_curse_words)
                        word_count_dictionary_raw = wc.count_text_file_words(text_file_path, have_stop_words=True, have_curse_words=True)

                        if word_count_dictionary != None:
                            cloud = wordcloud.generate_word_cloud(word_count_dictionary)
                            excel_file = wc.write_word_count_excel(word_count_dictionary_raw, genre, None)
                        
                            recolor_or_save = ui.save_or_recolor(cloud)
                            while recolor_or_save != None:
                                recolor_or_save = ui.save_or_recolor(recolor_or_save)

                        else:
                            print("\n-- There was a problem creating a word cloud from this file")
                            time.sleep(3)

            except Exception as e:
                print("\n-- There was a problem creating a word cloud from this file" + str(e))
                time.sleep(3)




        elif option == "3":
            ui.display_previous_data_options()
            genre_option = input("\n>> Enter Option: ")
            ui.clear_screen()
            while genre_option not in ui.GENRE_CHOICES:
                ui.display_previous_data_options()
                genre_option = input("\n>> Enter Option: ")
                ui.clear_screen()

                if genre_option == '10':
                    break

            if genre_option != '10':
                genre = ui.GENRE_SWITCH[genre_option]
                excel_file_list = dir_nav.get_existing_excel(genre)
                total_files = len(excel_file_list)
                exit_number = total_files + 1


                if total_files > 0:

                    excel_choice = 0
                    while excel_choice != str(exit_number):

                        print()
                        print("Select Excel File To Create Word Cloud")

                        ui.display_excel_files(excel_file_list)

                        excel_choice = input("\n>> Enter Option: ")
                        ui.clear_screen()

                        if excel_choice.isdigit():
                            if int(excel_choice) > 0 and int(excel_choice) <= total_files:
                                break

                    if excel_choice == str(exit_number):
                        #Goes back to main menu
                        pass

                    else:
                        have_stop_words, have_curse_words = ui.get_word_choice()

                        if have_stop_words != None and have_curse_words != None:
                            print("Creating Word Cloud..")
                            word_count_dictionary = wc.create_word_dictionary_from_excel(excel_file_list[int(excel_choice)-1], have_stop_words, have_curse_words)
                            cloud = wordcloud.generate_word_cloud(word_count_dictionary)
                            #ui.save_or_recolor(cloud)

                            recolor_or_save = ui.save_or_recolor(cloud)
                            while recolor_or_save != None:
                                recolor_or_save = ui.save_or_recolor(recolor_or_save)

                else:
                    print("\n-- No Previous Files Could Be Found For " +  genre)
                    time.sleep(3)




        elif option == "4":
            excel_genre = ""
            while excel_genre not in ui.GENRE_CHOICES:
                ui.display_excel_genres()
                excel_genre = input("\n>> Enter Option: ")
                ui.clear_screen()

                if excel_genre == '10':
                    break

            if excel_genre != '10':

                excel_genre = ui.GENRE_SWITCH[excel_genre]
                excel_file_list = dir_nav.get_existing_excel(excel_genre)
                total_files = len(excel_file_list)
                exit_number = total_files + 1


                if total_files > 0:

                    excel_choice = 0
                    while excel_choice != str(exit_number):

                        print()
                        print("Select Excel File To Open")

                        ui.display_excel_files(excel_file_list)

                        excel_choice = input("\n>> Enter Option: ")
                        ui.clear_screen()

                        if excel_choice.isdigit():
                            if int(excel_choice) > 0 and int(excel_choice) <= total_files:
                                break

                    if excel_choice == str(exit_number):
                        #Goes back to main menu
                        pass

                    else:
                        file_name_start = excel_file_list[int(excel_choice)-1].rfind("\\")
                        file_name = excel_file_list[int(excel_choice)-1][file_name_start+1:]
                        print("Opening: " + file_name)
                        os.startfile(excel_file_list[int(excel_choice)-1])

                else:
                    print("\n-- No Previous Files Could Be Found For " +  excel_genre)
                    time.sleep(3)


        elif option == "5":
            ui.display_help()

            back = input("\n>> Press Any Key To Go Back: ")




if __name__ == '__main__':
    main()

