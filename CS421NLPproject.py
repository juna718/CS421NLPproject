#CS421 Project Part 1
# Junha Liu - jliu238@uic.edu
# Hamza Mansoor - smans4@uic.edu

import os
import re
import spacy

# Load English language model
nlp = spacy.load("en_core_web_sm")

# (a) Number of sentences and length
def count_sentences(text):
    """
    Count the number of sentences in the given text.
    """
    # Split the text into sentences using regular expressions
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    return len(sentences)

# (b) Spelling Mistakes - Placeholder function
def detect_spelling_mistakes(text):
    """
    Placeholder function for detecting spelling mistakes.
    """
    # Add code for spelling mistake detection here
    pass

# c(i) Subject-Verb agreement
def detect_subject_verb_agreement_errors(text):
    """
    Detect subject-verb agreement errors using SpaCy.
    """
    errors = 0
    # Process the text with SpaCy
    doc = nlp(text)
    for token in doc:
        if token.pos_ == "NOUN" and token.dep_ == "nsubj":  # Check if token is a subject
            head_verb = token.head
            if head_verb.pos_ == "VERB":
                # Check if the verb is in the 3rd person singular form
                if head_verb.tag_ != "VBZ":  
                    errors += 1
    return errors

# c(ii) Verb tense / missing verb / extra verb - Placeholder function
def detect_verb_errors(text):
    """
    Placeholder function for detecting verb tense/missing verb/extra verb errors.
    """
    # Add code for verb error detection here
    pass

def main():
    # Path to the directory containing essays
    directory = "essays_dataset/essays"
    
    # Loop through each essay file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            try:
                # Read the essay text
                with open(file_path, 'r', encoding='utf-8') as file:
                    essay_text = file.read()
                
                # (a) Number of sentences
                num_sentences = count_sentences(essay_text)
                print(f"Number of sentences in {filename}: {num_sentences}")
                
                # (b) Spelling Mistakes - Placeholder
                # Add code for spelling mistake detection here
                # detect_spelling_mistakes(essay_text)
                
                # c(i) Subject-verb agreement
                sva_errors = detect_subject_verb_agreement_errors(essay_text)
                print(f"Subject-verb agreement errors in {filename}: {sva_errors}")
                
                # c(ii) Verb tense / missing verb / extra verb - Placeholder
                # Add code for verb error detection here
                # detect_verb_errors(essay_text)

            except Exception as e:
                print(f"Error reading file {filename}: {e}")

if __name__ == "__main__":
    main()
