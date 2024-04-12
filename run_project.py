import os
import argparse
from sample_code_1 import count_sentences, compute_sentence_score, spelling_mistakes ,spelling_mistakes_to_score, calculate_average_length
from sample_code_2 import verb_errors_to_score, total_verb_errors, verb_errors_to_score

def main(filename):
    directory = "essays"
    file_path = os.path.join(directory, filename)
    average_length_low, average_length_high = calculate_average_length()
    try:
        # Read the essay text
        with open(file_path, 'r', encoding='utf-8') as file:
            essay_text = file.read()
            
        print(f"\n{filename}:")
        print(f"\n{essay_text}")
        
        # (a) Number of sentences and length
        num_sentences = count_sentences(essay_text)
        sentence_score = compute_sentence_score(num_sentences, average_length_high, average_length_low)
        print(f"\nNumber of Sentences: {num_sentences}")

        # (b) Spelling Mistakes
        num_spelling_mistakes = len(spelling_mistakes(essay_text))
        spelling_score = spelling_mistakes_to_score(essay_text)
        print(f"Spelling Mistakes: {num_spelling_mistakes}")
        
        
        # c(i) Agreement errors
        error_sentences, num_subject_verb_agreement_errors, num_verb_tense_errors, num_missing_verb_extra_verb_errors = total_verb_errors(essay_text)
        verb_error_score = verb_errors_to_score(essay_text)
        print(f"\nSubject-Verb Agreement Error Sentences: {num_subject_verb_agreement_errors}")
        
        # c(ii) Verb errors - Placeholder
        print(f"Verb Tense Error Sentences: {num_verb_tense_errors}")
        print(f"Missing Verb/Extra verb Error Sentences: {num_missing_verb_extra_verb_errors}")
        print(f"Total Number of Sentences Containing any of Verb Errors: {len(error_sentences)}")
        

        # Total Score
        print(f"\nEssay Length Score: {sentence_score}")
        print(f"Spelling Mistakes Score: {spelling_score}")
        print(f"Verb Error Score: {verb_error_score}")
        
    except Exception as e:
        print(f"Error reading file {filename}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process an essay file.')
    parser.add_argument('filename', type=str, help='Name of the essay file to process')
    args = parser.parse_args()
    main(args.filename)

