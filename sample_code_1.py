import re
import string
from spellchecker import SpellChecker
import pandas as pd
import os

def calculate_average_length():
    essays = {}
    directory = "essays"
    indexes_df = pd.read_csv('index.csv', delimiter=';')
    indexes_df['length'] = 0
    # Loop through each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    essays[filename] = file.read()
                    # Count the sentences and update the DataFrame
                    indexes_df.loc[indexes_df['filename'] == filename, 'length'] = count_sentences(essays[filename])
            except Exception as e:
                print(f"Error reading file {filename}: {e}")
    # Calculate the average length for grade 'low'
    average_length_low = indexes_df[indexes_df['grade'] == 'low']['length'].mean()

    # Calculate the average length for grade 'high'
    average_length_high = indexes_df[indexes_df['grade'] == 'high']['length'].mean()
    return average_length_low, average_length_high

def count_sentences(text):
    """
    Count the number of sentences in the given text.
    """
    # Split the text into sentences using regular expressions
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=[.?])\s', text)
    return len(sentences)


def compute_sentence_score(length, average_length_high, average_length_low):
    midpoint = (average_length_high + average_length_low) / 2
    
    # Assign numeric scores based on the length of the essay
    if length >= average_length_high:
        return 5
    elif length >= midpoint:
        return 4
    elif length >= average_length_low:
        return 3
    elif length >= average_length_low / 2:
        return 2
    else:
        return 1
    
def remove_punctuation(text):
    """
    Remove all punctuation characters from a given text.
    
    Args:
    text (str): The text from which to remove punctuation.
    
    Returns:
    str: The text without punctuation.
    """
    # Create a translation table that maps all punctuation characters to None
    translator = str.maketrans('', '', string.punctuation)
    # Use the translate method to remove all punctuation from the text
    text_without_punctuation = text.translate(translator)
    return text_without_punctuation

def spelling_mistakes(essay):
    """
    Identify misspelled words in an essay after removing punctuation.
    
    Args:
    essay (str): The essay text to check for spelling mistakes.
    
    Returns:
    set: A set of misspelled words.
    """
    # Initialize the spell checker
    spell = SpellChecker()
    # Remove punctuation from the essay to avoid incorrect spell-check results
    essay_removed_punc = remove_punctuation(essay)
    # Split the text into words and find the ones that are misspelled
    misspelled = spell.unknown(essay_removed_punc.split())
    return misspelled

def spelling_mistakes_to_score(essay):
    """
    Calculate a score based on the number of unique spelling mistakes in an essay.
    
    Args:
    essay (str): The essay text to evaluate for spelling mistakes.
    
    Returns:
    int: The spelling score, where a higher score indicates fewer mistakes.
    """
    # Get the set of misspelled words from the essay
    misspelled = spelling_mistakes(essay)
    # Count the unique spelling mistakes
    num_mistakes = len(misspelled)
    # Assign a score based on the number of mistakes
    if num_mistakes == 0:
        return 4  # No mistakes
    elif 1 <= num_mistakes <= 2:
        return 3  # Few mistakes
    elif 3 <= num_mistakes <= 5:
        return 2  # Moderate mistakes
    elif 6 <= num_mistakes <= 8:
        return 1  # Many mistakes
    else:
        return 0  # Excessive mistakes
