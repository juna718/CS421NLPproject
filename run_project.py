import os
import argparse
import pandas as pd
from sample_code_1 import count_sentences, compute_sentence_score, spelling_mistakes, spelling_mistakes_to_score, \
    calculate_average_length
from sample_code_2 import verb_errors_to_score, total_verb_errors, parse_essay, syntatic_errors_to_score, load_w2v, analyze_essays, read_essay, compute_similarity_to_prompt, essay_coherence, compute_similarity_coherence_score, calculate_final_score

def main(filename):
    # Set the directory where essays are stored
    directory = "essays"
    word2vec = load_w2v("w2v.pkl")
    file_path = os.path.join(directory, filename)
    average_length_low, average_length_high = calculate_average_length()
    df = pd.read_csv('index.csv', delimiter=';')
    prompt = str(df[df['filename'] == filename]['prompt'].values)
    avg_sim_high, avg_sim_low, avg_coh_high, avg_coh_low = analyze_essays(df, word2vec)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            essay_text = file.read()

        print(f"\n{filename}:")
        print(f"\n{essay_text}")

        # a) Analyze number of sentences and overall essay length for scoring
        num_sentences = count_sentences(essay_text)
        sentence_score = compute_sentence_score(num_sentences, average_length_high, average_length_low)
        print(f"\nNumber of Sentences: {num_sentences} (a)")

        # b) Check and score spelling mistakes in the essay
        num_spelling_mistakes = len(spelling_mistakes(essay_text))
        spelling_score = spelling_mistakes_to_score(essay_text)
        print(f"Spelling Mistakes: {num_spelling_mistakes} (b)")

        # c(i, ii) Analyze verb-related errors for scoring
        error_sentences, num_subject_verb_agreement_errors, num_verb_tense_errors, num_missing_verb_extra_verb_errors = total_verb_errors(essay_text)
        verb_error_score = verb_errors_to_score(essay_text)
        print(f"\nSubject-Verb Agreement Error Sentences: {num_subject_verb_agreement_errors}")
        print(f"Verb Tense Error Sentences: {num_verb_tense_errors}")
        print(f"Missing Verb/Extra Verb Error Sentences: {num_missing_verb_extra_verb_errors}")
        print(f"Total Number of Sentences Containing any of Verb Errors: {len(error_sentences)} (c.i, ii)\n")
        
        # c(iii)
        syntatic_error = parse_essay(essay_text)
        syntatic_error_score = syntatic_errors_to_score(essay_text)
        print(f"Total Number of Syntactic Error: {syntatic_error} (c.iii)\n")
        
        
        #d) Assess topic relevance (d.i) and coherence (d.ii) of the essay
        similarity = compute_similarity_to_prompt(prompt, essay_text, word2vec)
        coherence = essay_coherence(essay_text, word2vec)
        similarity_score = compute_similarity_coherence_score(similarity, avg_sim_high, avg_sim_low)
        coherence_score = compute_similarity_coherence_score(coherence, avg_coh_high, avg_coh_high)
        print(f"Essay addresses the topic (cosine similarity): {similarity} (d.i)")
        print(f"Essay coherence (standard deviation of similarities): {coherence} (d.ii)\n")

        # Summarize total scores from various assessments (integration of semantic scores is noted but not implemented here)
        print(f"\nEssay Length Score: {sentence_score}")
        print(f"Spelling Mistakes Score: {spelling_score}")
        print(f"Verb Error Score: {verb_error_score}")
        print(f"Syntactic Score: {syntatic_error_score}")
        print(f"Topic Score: {similarity_score}")
        print(f"Coherence Score: {coherence_score}")
        
        final_score = calculate_final_score(sentence_score, spelling_score, verb_error_score, syntatic_error_score, similarity_score, coherence_score)
        print(f"\nFinal Score: {final_score}")

    except Exception as e:
        print(f"Error reading file {filename}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process an essay file.')
    parser.add_argument('filename', type=str, help='Name of the essay file to process')
    args = parser.parse_args()
    main(args.filename)
