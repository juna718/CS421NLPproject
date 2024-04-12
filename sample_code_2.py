import spacy
from nltk import pos_tag, word_tokenize, sent_tokenize
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Load English language model
nlp = spacy.load("en_core_web_sm")

def find_next_verb(tagged, start_index):
    """
    Find the next verb after the specified index in the tagged list.
    Skip adjectives, adverbs, and other non-verbs until a verb is found.
    """
    for i in range(start_index + 1, len(tagged)):
        word, tag = tagged[i]
        if tag.startswith('VB'):  # Any verb form
            return word, tag
    return None, None


def check_subject_verb_agreement(sentence):
    # Tokenize and POS tag the input sentence
    tokens = word_tokenize(sentence)
    tagged = pos_tag(tokens)

    # Iterate through the tagged tokens
    for i, (word, tag) in enumerate(tagged):
        if tag in ['NNP', 'NN', 'PRP', 'NNS', 'NNPS']:  # Singular, plural nouns, and personal pronouns
            next_word, next_tag = find_next_verb(tagged, i)
            
            if next_word:
                if (tag in ['NNP', 'NN', 'PRP'] and word.lower() in ['he', 'she', 'it']) and next_tag != 'VBZ':
                    return True
                elif (tag in ['NNS', 'NNPS'] or (tag == 'PRP' and word.lower() in ['i', 'you', 'we', 'they'])) and next_tag != 'VBP':
                    return True
                elif tag in ['NNP', 'NN'] and next_tag != 'VBZ':
                    return True
                else:
                    return False

def subject_verb_agreement_errors(essay):
    sentences = sent_tokenize(essay)
    error_sentences = set()
    for sentence in sentences:
        if (check_subject_verb_agreement(sentence)):
            error_sentences.add(sentence)
    return error_sentences

def verb_tense_errors(essay):
    """
    Identify sentences in the essay that mix past tense and non-past tense verbs, 
    which is typically considered a grammatical error.
    """
    # Split the essay into sentences
    sentences = sent_tokenize(essay)
    error_sentences = set()
    
    for sentence in sentences:
        # Tokenize the sentence into words and tag each word with its part of speech
        tagged = pos_tag(word_tokenize(sentence))
        past_tense_verbs = 0
        non_past_tense_verbs = 0
        
        # Count past and non-past verbs
        for word, tag in tagged:
            if tag in ['VBD', 'VBN']:  # Past tense or past participle
                past_tense_verbs += 1
            elif tag in ['VB', 'VBG', 'VBP', 'VBZ']:  # Base, gerund, or present tense
                non_past_tense_verbs += 1
                
        # If both past and non-past verbs are found in a sentence, count as error
        if past_tense_verbs > 0 and non_past_tense_verbs > 0:
            error_sentences.add(sentence)
            
    return error_sentences

def missing_verb_extra_verb_errors(essay):
    """
    Detect sentences with either missing verbs or too many verbs, considering complex 
    structures such as relative and interrogative clauses.
    """
    sentences = sent_tokenize(essay)
    error_sentences = set()
    
    for sentence in sentences:
        words = word_tokenize(sentence)
        tagged = pos_tag(words)
        
        # Count verbs and expected verb counts based on certain conjunctions and prepositions
        verb_count = sum(1 for word, tag in tagged if tag.startswith('VB'))
        expected_verbs_count = 1 + sum(1 for word, tag in tagged if tag in ['CC', 'IN', 'TO', 'WDT', 'WP', 'WRB'])

        # Check for missing verbs or too many verbs
        if verb_count == 0 or verb_count > expected_verbs_count+1:
            error_sentences.add(sentence)
    
    return error_sentences

def total_verb_errors(essay):
    """
    Combine individual verb error checks to find all sentences with verb-related errors.
    """
    num_subject_verb_agreement_errors = len(subject_verb_agreement_errors(essay))
    num_verb_tense_errors = len(verb_tense_errors(essay))
    num_missing_verb_extra_verb_errors = len(missing_verb_extra_verb_errors(essay))
    
    # Use set union to combine error sentences from different checks
    error_sentences = subject_verb_agreement_errors(essay) | verb_tense_errors(essay) | missing_verb_extra_verb_errors(essay)
    return error_sentences, num_subject_verb_agreement_errors, num_verb_tense_errors, num_missing_verb_extra_verb_errors

def verb_errors_to_score(essay):
    """
    Calculate a score based on the number of unique verb-related errors in the essay.
    """
    # Count the unique verb errors
    num_mistakes = len(total_verb_errors(essay)[0])
    if num_mistakes == 0:
        return 5  # No mistakes
    elif 1 <= num_mistakes <= 2:
        return 4  # Few mistakes
    elif 3 <= num_mistakes <= 4:
        return 3  # Moderate mistakes
    elif 5 <= num_mistakes <= 6:
        return 2  # Many mistakes
    else:
        return 1  # Excessive mistakes
