# CS421NLPproject

Teammate 1 NAME: Hamza Mansoor - smans4@uic.edu
Teammate 2 NAME: Junha Liu - jliu238@uic.edu

Project files & functions:

- sample_code_1.py:

  - calculate_average_length function calculates the average sentence length from a corpus of texts.
  
  - count_sentences function calculates scoring criterion a (number of sentences and lengths)
  
  - compute_sentence_score function calculates scoring criterion a (sentence score)

  - remove_punctuation function removes all punctuation from the provided text. 

  - spelling_mistakes function identifies spelling mistakes within an essay. 

  - spelling_mistakes_to_score function converts the count of unique spelling mistakes identified by the spelling_mistakes function into a numeric score. The scoring system is tiered, with a range from 0 (excessive mistakes) to 4 (no mistakes), allowing for a quantifiable measure of spelling accuracy in the essay.
  
  - Calculates the average sentence length from a corpus of texts.
  
- sample_code_2.py:

  - subject_verb_agreement_errors function identifies sentences with subject-verb agreement errors.
  
  - verb_tense_errors function identifies sentences that mix past tense and non-past tense verbs, which can indicate tense inconsistency errors. It tokenizes the essay into sentences, tags each word with its part of speech, and counts the types of verb tenses. Sentences containing both past and non-past tense verbs are marked as error.

  - missing_verb_extra_verb_errors function detects sentences with either missing verbs or an excessive number of verbs. It assesses the expected number of verbs based on the presence of conjunctions, prepositions, and other linking parts of speech, comparing it to the actual count of verbs in the sentence. Sentences that don't meet the expected verb count are considered to have errors.

  - total_verb_errors function aggregates verb-related errors from the verb_tense_errors and missing_verb_extra_verb_errors functions into a set of unique error-containing sentences. 

  - verb_errors_to_score function quantifies the severity of verb-related errors by converting the count of unique error-containing sentences into a numeric score. The scoring system ranges from 1 (excessive mistakes) to 5 (no mistakes), allowing for a measurable assessment of verb usage and grammatical accuracy in the essay.
  
- run_project.py

Packages used:
- SpaCY
- Numpy
- spellchecker
