import os
import argparse
from sample_code_1 import count_sentences, compute_sentence_score, spelling_mistakes_to_score
from sample_code_2 import detect_agreement_errors, verb_errors_to_score

def main(filename):
    directory = "essays"
    file_path = os.path.join(directory, filename)
    
    try:
        # Read the essay text
        with open(file_path, 'r', encoding='utf-8') as file:
            essay_text = file.read()
        
        # (a) Number of sentences and length
        num_sentences = count_sentences(essay_text)
        sentence_score = compute_sentence_score(num_sentences)
        print(f"Number of sentences in {filename}: {num_sentences}")
        print(f"Sentence score for {filename}: {sentence_score}")

        # (b) Spelling Mistakes
        spelling_score = spelling_mistakes_to_score(essay_text)
        print(f"Spelling score for {filename}: {spelling_score}")
        # c(i) Agreement errors
        agreement_errors = detect_agreement_errors(essay_text)
        print(f"Agreement errors for {filename}: {agreement_errors}")

        # c(ii) Verb errors - Placeholder
        verb_error_score = verb_errors_to_score(essay_text)
        print(f"Verb error scores for {filename}: {verb_error_score}")

    except Exception as e:
        print(f"Error reading file {filename}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process an essay file.')
    parser.add_argument('filename', type=str, help='Name of the essay file to process')
    args = parser.parse_args()
    main(args.filename)

