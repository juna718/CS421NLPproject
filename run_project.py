from sample_code_1 import count_sentences, compute_sentence_score
from sample_code_2 import detect_agreement_errors, detect_verb_errors

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
                
                # (a) Number of sentences and length
                num_sentences = count_sentences(essay_text)
                sentence_score = compute_sentence_score(num_sentences)
                print(f"Number of sentences in {filename}: {num_sentences}")
                print(f"Sentence score for {filename}: {sentence_score}")

                # (b) Spelling Mistakes - Placeholder
                # detect_spelling_mistakes(essay_text)

                # c(i) Agreement errors
                agreement_errors = detect_agreement_errors(essay_text)
                print(f"Agreement errors in {filename}: {agreement_errors}")

                # c(ii) Verb errors - Placeholder
                # verb_errors = detect_verb_errors(essay_text)
                # print(f"Verb errors in {filename}: {verb_errors}")

            except Exception as e:
                print(f"Error reading file {filename}: {e}")

if __name__ == "__main__":
    main()
