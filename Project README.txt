# CS421NLPproject

## Team Information
- **Teammate 1 NAME**: Hamza Mansoor - smans4@uic.edu
- **Teammate 2 NAME**: Junha Liu - jliu238@uic.edu

## Project Files & Functions

### sample_code_1.py:
- `calculate_average_length`: Calculates the average sentence length from a corpus of texts

- `count_sentences`: Calculates scoring criterion a (number of sentences and lengths).

- `compute_sentence_score`: Calculates scoring criterion a (sentence score).

- `remove_punctuation`: Removes all punctuation from the provided text.

- `spelling_mistakes`: Identifies spelling mistakes within an essay.

- `spelling_mistakes_to_score`: Converts the count of unique spelling mistakes identified by the `spelling_mistakes` function into a numeric score. The scoring system is tiered, with a range from 0 (excessive mistakes) to 4 (no mistakes), providing a quantifiable measure of spelling accuracy in the essay.

### sample_code_2.py:
- `string_to_vec`: Converts a sentence into an average word vector, focusing on content words with vectors.

- `cosine_similarity`: Computes the cosine similarity between two vectors, used in determining essay coherence and topic relevance.

- `essay_address_topic` (Part d.i): Computes how well the essay addresses the prompt using cosine similarity between the prompt's topic vector and the essay's average sentence vector.

- `essay_coherence` (Part d.ii): Analyzes the coherence of the essay by examining cosine similarities between consecutive sentences, reflecting on the essay's internal logical flow.

- `analyze_essay_coherence_and_topic`: Integrates analyses for both topic relevance (d.i) and coherence (d.ii) of an essay.

- `subject_verb_agreement_errors`: Identifies sentences with subject-verb agreement errors.

- `verb_tense_errors`: Identifies sentences that mix past and non-past tense verbs, highlighting tense inconsistency errors.

- `missing_verb_extra_verb_errors`: Detects sentences with either missing verbs or an excessive number of verbs, assessing grammatical accuracy.

- `total_verb_errors`: Aggregates verb-related errors into a set of unique error-containing sentences.

- `verb_errors_to_score`: Quantifies the severity of verb-related errors into a numeric score, ranging from 1 (excessive mistakes) to 5 (no mistakes).

### run_project.py
- This script is the main entry point for processing essays. It uses functions from `sample_code_1.py` and `sample_code_2.py` to perform a comprehensive analysis of essays, including counting sentences, detecting spelling mistakes, analyzing verb errors, and assessing both topic relevance and coherence.

## Packages Used:
- **SpaCy**: Utilized for NLP tasks, particularly for tokenization and word vector computations.
- **NumPy**: Used for numerical operations, especially in vector calculations and statistics.
- **spellchecker**: Employed to identify and score spelling mistakes within the essays.
