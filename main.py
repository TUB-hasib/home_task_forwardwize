# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
import pandas as pd
import math


def home_task():
    # reading the data set
    df = pd.read_csv("./data/the_office_lines_scripts.csv")

    # .................................Data cleaning....................................................................
    df_main = df.copy(deep=True) # coping the whle data frame

    # lowercase speaker and line_text column
    df_main['speaker'] = df_main['speaker'].str.lower()
    df_main['line_text'] = df_main['line_text'].str.lower()

    #

    #exit()

    # ..................................................................................................................
    # Q1:  How many characters are there? What are their names (COMPLETE)
    name_of_characters = df_main.speaker.unique()
    no_of_character = len(df_main.speaker.unique())

    print(100 * "."+"\nQ1:  How many characters are there? What are their names?\nAnswer:\n")
    print(f"number of character: {no_of_character} ")
    print(f"characters: {name_of_characters}")

    # ..................................................................................................................
    # Q2:  For each character, find out who has the most lines across all episodes (COMPLETE)

    df_no_lines_for_character = df_main[['speaker', 'line_text']].groupby(
        ['speaker']).count()  # finding no of lines for each character
    df_no_lines_for_character_sorted = df_no_lines_for_character.sort_values(by='line_text')  # sort by no of lines

    print(100 * "." + "\nQ2:  For each character, find out who has the most lines across all episodes\nAnswer:\n")
    print(f"{df_no_lines_for_character_sorted.tail(1)}")
    # print(df_main['speaker'].value_counts()) # one line to do the wole task 2

    # ..................................................................................................................
    # Q3:  What is the average of words per line for each character? (COMPLETE)

    df_no_lines_for_character = df_main[['speaker', 'line_text']].groupby(
        ['speaker']).count()  # finding no of lines for each character

    df_main['words_in_line'] = df_main['line_text'].apply(count_words_in_line)  # new col showing no of words in line

    df_no_words_in_line_for_character = df_main[['speaker', 'words_in_line']].groupby(
        ['speaker']).sum()  # finding no of words for each character.

    df_temp = pd.merge(df_no_lines_for_character, df_no_words_in_line_for_character,
                       on='speaker', how='inner')  # merging total no of lines and total no of words for each character

    df_temp['avg_words'] = df_temp['words_in_line'] / df_temp['line_text']

    print(100 * "." + "\nQ3:  What is the average of words per line for each character?.\nAnswer:\n")
    print(df_temp.sort_values(by='line_text', ascending=0))

    # ..................................................................................................................
    # Q4:  What is the most common word per character? (COMPLETE)
    df_common_word = df_main[['speaker', 'line_text']].copy(deep=True)  # copying dataframe

    df_common_word = df_common_word.groupby(
        ['speaker'])['line_text'].apply(' '.join).reset_index()  # concating all lines based on speaker
    df_common_word['list_of_words'] = df_common_word['line_text'].apply(
        create_list_of_words)  # creating list of words from line

    print(100 * "." + "\nQ4:   What is the most common word per character?\nAnswer:\n")
    df_common_word['most_common_word'] = df_common_word['list_of_words'].apply(find_most_common_word)
    print(df_common_word[['speaker', 'most_common_word']])

    # ..................................................................................................................
    # Q5: Number of episodes where the character does not have a line, for each character (COMPLETE)
    print(100 * "." + "\nQ5 Number of episodes where the character does not have a line,for each character.\nAnswer:\n")

    df_episode_count = df_main[['speaker', 'season', 'episode']].copy(deep=True)  # copying dataframe

    total_no_of_episode = len(df_episode_count[['season', 'episode']].drop_duplicates()) # finding total no of episode
    print(f"Total number of episode {total_no_of_episode}")

    for character in name_of_characters:
        filter_ = (df_episode_count['speaker'] == character)  # finding lines for the character
        no_ep_with_line = len(df_episode_count[filter_].drop_duplicates())
        no_ep_without_line = total_no_of_episode - no_ep_with_line
        print(f"Character: {character}\nNumber of Episode without Line {no_ep_without_line}\n")

    # ..................................................................................................................
    # Q6: Number of times "That's what she said" joke comes up (COMPLETE)
    print(100 * "." + "\nQ6: Number of times \"That's what she said\" joke comes up.\nAnswer:")
    filter_ = df_main['line_text'].str.contains('That\'s what she said')
    print(df_main[filter_].line_text.count())

    # ..................................................................................................................
    # Q7:Include five examples of the joke

    print(100 * "." + "\nQ7: Include five examples of the joke.\nAnswer:")
    df_temp = df_main[filter_].copy(deep=True)  # dataframe with all the joke lines
    jokes_id_no = df_temp.id.to_numpy()  # storing id no of the jokes
    df_jokes = df_main[['id', 'speaker', 'line_text']]

    joke_count = 1
    for id_no in jokes_id_no[1:6]:  # filtering dataframe for each joke id and printing value from joke id and id-1
        print(f"joke: {joke_count}")
        filter_ = (df_jokes['id'] == id_no-1) | (df_jokes['id'] == id_no)
        print(df_jokes[filter_])
        joke_count += 1

    # ..................................................................................................................
    # Q8:The average percent of lines each character contributed each episode per season

    df_no_words_in_line_for_character = df_main[['season', 'episode', 'speaker']].groupby(
        ['season', 'episode']).value_counts(normalize=True)
    print(100 * "." + "\nQ8: The average percent of lines each character contributed each episode per season.\nAnswer:")
    print(df_no_words_in_line_for_character)

    # ..................................................................................................................
    # Q8:Total no of episode aired

    df_episode = df_main[['season', 'episode']].copy(deep=True)  # copying dataframe
    total_no_of_episode = len(df_episode[['season', 'episode']].drop_duplicates())  # count to no of episode
    print(100 * "." + "\nQ9: find Total no of episode aired .\nAnswer:")
    print(f"Total number of episode {total_no_of_episode}")


# finding out most common word in a list of words  input: list  output: max element in the list
def find_most_common_word(list_x):
    df_values = pd.value_counts(np.array(list_x))  # calculating no of occurrence for each element in the list
    most_common_word = df_values.idxmax()
    occurrence_most_common_word = df_values.max()
    return most_common_word


# counting no of words in given line. input: string  output: no of words
def count_words_in_line(x):
    l= x.split()
    return len(l)


# creating list of words from a string . input: string  output: list containg words
def create_list_of_words(x):
    lst = x.split()
    return list(lst)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    home_task()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
