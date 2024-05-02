Team Information
- Hamza Mansoor - smans4@uic.edu
- Junha Liu - jliu238@uic.edu

Installation

   1. Clone or Download the Repository

      - To get started, clone this repository to your local machine or download the ZIP and extract it.

   2. Install Required Packages

      - Install the necessary Python packages using pip:
      
      pip install nltk spacy pyspellchecker pickle os

   3. Start Stanford CoreNLP server

      - https://github.com/nltk/nltk/wiki/Stanford-CoreNLP-API-in-NLTK

   4. Download w2v.pkl file in the same location.

   Usage

      - To run the system, use the following command in the terminal:

      python run_project.py <filename>
      
      Replace `<filename>` with the name of the essay file you want to evaluate. Ensure the file is located in the `essays` directory.

   Example

   To process an essay named `example_essay.txt`, 

      python run_project.py example_essay.txt


Function Description

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

- 'analyze_sentence_structure(pos_tags)': Analyzes the grammatical structure of sentences, identifying errors based on POS tags.

- 'noun_without_determiner(word)': Checks if a noun typically is used without a determiner.

- 'check_constituents(pos_tags)': Identifies grammatical errors related to determiner usage before nouns.

- 'check_subordinating_conjunctions(parse_tree)': Verifies proper usage of subordinating conjunctions within parsed sentence structures.

- 'parse_essay(essay)': Analyzes an entire essay for syntactic errors using a combination of parsing and POS tagging.

- 'syntatic_errors_to_score(essay)': Converts the number of syntactic errors in an essay into a numerical score.

- 'load_w2v(filepath)': Loads a pre-trained Word2Vec model from a file.

- 'w2v(word2vec, token)': Retrieves the word vector for a specified word from the Word2Vec model.

- 'sentence_embedding(word2vec, tokens)': Computes the average word vector for a list of tokens.

- 'cosine_similarity(a, b)': Calculates the cosine similarity between two vectors.

- 'compute_similarity_to_prompt(prompt, essay_text, word2vec)': Computes the similarity between an essay and a given prompt using word embeddings.

- 'essay_coherence(essay_text, word2vec)': Evaluates the coherence of an essay by calculating the cosine similarity between consecutive sentences.

- 'read_essay(file_name)': Reads an essay from a specified file.

- 'analyze_essays(df, word2vec)': Analyzes a set of essays for similarity and coherence, returning averages for high and low graded essays.

- 'compute_similarity_coherence_score(sim_coh, avg_high, avg_low)': Assigns a score based on a value's proximity to average high and low values.

- 'calculate_final_score(a, b, c, d, e, f)': Computes the final score for an essay based on various metrics and weights.


### run_project.py

- This script is the main entry point for processing essays. It uses functions from `sample_code_1.py` and `sample_code_2.py` to perform a comprehensive analysis of essays, including counting sentences, detecting spelling mistakes, analyzing verb errors, and assessing both topic relevance and coherence.

## Packages Used:
- **SpaCy**: Utilized for NLP tasks, particularly for tokenization and word vector computations.
- **NumPy**: Used for numerical operations, especially in vector calculations and statistics.
- **spellchecker**: Employed to identify and score spelling mistakes within the essays.

Scoring Criteria

1. Sentence Counting and Scoring

Methodology:

Sentences are counted using regular expressions to split the text based on typical sentence-ending punctuation. The approach avoids common pitfalls like mistaking abbreviations for sentence ends.

Scoring:

5 points if the number of sentences is greater than or equal to the average of high-scoring essays (20.86).
4 points if the number of sentences is greater than or equal to the midpoint (15.33).
3 points if the number of sentences is greater than or equal to the average of low-scoring essays (9.8).
2 points if the number of sentences is greater than or equal to half of the low essay average.
1 point if the number of sentences is less than half of the low essay average.

2. Spelling Mistakes and Scoring

Methodology:

The SpellChecker library is used to identify spelling errors by comparing each word against a dictionary of correctly spelled words.

Scoring:

4 points for no spelling mistakes.
3 points for 1 to 2 mistakes.
2 points for 3 to 5 mistakes.
1 point for 6 to 8 mistakes.
0 points for more than 8 mistakes.

3. Grammar Correctness: Verb Errors

Subject-Verb Agreement Error

Methodology: Using SpaCy to check that the verb agrees with its subject in person and number.

Scoring: Integrated into the total verb error count.

Verb Tense Error

Methodology: NLTK is used to detect mixing of past and non-past tense verbs within the same sentence, which can indicate temporal inconsistencies.

Scoring: Integrated into the total verb error count.

Missing/Extra Verb Error

Methodology: Analyzing sentences for the correct number of verbs expected, given the structure and elements like conjunctions and prepositions.

Scoring: Integrated into the total verb error count.

Combined Scoring for Verb Errors:
5 points if there are no sentences with verb errors.
4 points for 1 to 2 sentences with verb errors.
3 points for 3 to 4 sentences with verb errors.
2 points for 5 to 6 sentences with verb errors.
1 point if more than 6 sentences have verb errors.


4. Syntactic Analysis

Methodology:

Parsing with CoreNLP: The CoreNLPParser is configured to analyze sentences from essays. It generates parse trees that help in understanding the grammatical structure of each sentence.

Sentence Structure Analysis:
Checks if a sentence improperly starts with a verb.
Verifies proper formation of questions starting with interrogative words (e.g., who, what, where).

Noun Determiner Check:
Analyzes singular nouns to ensure they have appropriate determiners preceding them, unless they are uncountable or abstract nouns, which typically do not require a determiner.

Subordinating Conjunction Check:
Ensures that subordinating conjunctions (like 'because', 'although', 'if') in a sentence properly introduce a clause that contains both a subject and a finite verb to maintain grammatical integrity.

Scoring:
Scores are assigned based on the number of syntactic errors detected:

5 points for 0-1 errors.
4 points for 2-3 errors.
3 points for 4-5 errors.
2 points for 6-7 errors.
1 point for more than 7 errors.



6. Computing Similarity to Prompt

Methodology:

 Calculates the average semantic similarity between the embeddings of sentences in an essay and the embedding of a given prompt. 
 This measures how well the content of the essay aligns with the expected response to the prompt.

average of high-scoring similarities: 0.8128154
average of low-scoring similarities: 0.4176300351755651

Scoring:

5 points if similarity is greater than or equal to the average of high-scoring similarities.
4 points if similarity is greater than or equal to the midpoint.
3 points if similarity is greater than or equal to the average of low-scoring similarities.
2 points if similarity is greater than or equal to half of the average of low-scoring similarities.
1 point if similarity is less than half of the average of low-scoring similarities.

7.Essay Coherence

Methodology:

Assesses the coherence of an essay by calculating cosine similarities between embeddings of consecutive sentences. This reflects how logically and smoothly ideas transition from one sentence to another within the essay.

average of high-scoring coherences: 0.7851273
average of low-scoring coherences: 0.4112611751226351


5 points if coherence is greater than or equal to the average of high-scoring coherences.
4 points if coherence is greater than or equal to the midpoint.
3 points if coherence is greater than or equal to the average of low-scoring coherences.
2 points if coherence is greater than or equal to half of the average of low-scoring coherences.
1 point if coherence is less than half of the average of low-scoring coherences.


Sample Input: python run_project.py 38209.txt

Sample Output:

38209.txt:

        It is generally believed that young people enjoy life more than older people do. Some people think, as young people are less aware of the seriousness of certain events, they can enjoy everything more than older people do. Other people oppose this point. As for me, I agree to say that young people enjoy life more than older people do.

        On the one hand, young people believe that older people can enjoy life more than they can. When I was a girl, I used to think that my parents and my grand parents are very lucky, because they didn't have homeworks, and could do whatever they want to do. I remember when I was 13 I said to my mom that I want to be 30 right now, because at this age, nothing were forbidden to me. I was so fed up to hear the adults saying "You cannot do this, you are too young" , or "You cannot stay here, we are discussing about a subject that you cannot understand !!" I was very upset, and thought that would be great to be older so that I can really enjoy life.

        However, I do not see it this way now. It seems to me that being young is synonym of being free, being independant. We can do whatever we want to without being always anxious.. Is that good? Am I suppose to do this? I really believe in the fact that, as young people are less aware of the seriousness of certain events, it is easier for them to enjoy life.
        Moreover, since we are still young, we have everything to discover. It is great and amazing to discover some new country for example when we have the opportunity to travel, to learn different cultures from all around the world.
        Furthermore, as we do not have children yet, we feel free to go out at night for parties, to do many things we won't be able to do in the future. Indeed, day after day, we would certainly feel bored to do always the same things, and we would not enjoy it likely.
        Last but not least, even if we have to study a lot, even if we have to work hard and may feel depressed time by time, I must recognise that it is even more interesting than staying at home everyday. It is more exciting to live without knowing what we will do tomorrow, than live everyday likely.

On the whole, I admit that I agree with the statement, because I think that young people enjoy life more than older people do as it is the first time they had discovered everything. Carpe Diem


Number of Sentences: 22 (a)
Spelling Mistakes: 6 (b)

Subject-Verb Agreement Error Sentences: 9
Verb Tense Error Sentences: 7
Missing Verb/Extra Verb Error Sentences: 3
Total Number of Sentences Containing any of Verb Errors: 13(c.i, ii)

Total Number of Syntactic Error: 10 (c.iii)

Essay addresses the topic (cosine similarity): 0.7890895009040833 (d.i)
Essay coherence (standard deviation of similarities): 0.2933473322126601 (d.ii)


Essay Length Score: 5
Spelling Mistakes Score: 1
Verb Error Score: 1
Syntactic Score: 1
Topic Score: 3
Coherence Score: 2
Final Score: 23


Support

https://github.com/juna718/CS421NLPproject