import spacy
from nltk import pos_tag, word_tokenize, sent_tokenize
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Load English language model
nlp = spacy.load("en_core_web_sm")

def detect_agreement_errors(text):
    """
    Detect agreement errors using POS tagging.
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

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag

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
        if verb_count == 0 or verb_count > expected_verbs_count:
            error_sentences.add(sentence)
    
    return error_sentences

def total_verb_errors(essay):
    """
    Combine individual verb error checks to find all sentences with verb-related errors.
    """
    # Use set union to combine error sentences from different checks
    error_sentences = verb_tense_errors(essay) | missing_verb_extra_verb_errors(essay)
    return error_sentences

def verb_errors_to_score(essay):
    """
    Calculate a score based on the number of unique verb-related errors in the essay.
    """
    # Count the unique verb errors
    num_mistakes = len(total_verb_errors(essay))
    if num_mistakes == 0:
        return 5  # No mistakes
    elif 1 <= num_mistakes <= 2:
        return 4  # Few mistakes
    elif 3 <= num_mistakes <= 5:
        return 3  # Moderate mistakes
    elif 6 <= num_mistakes <= 8:
        return 2  # Many mistakes
    else:
        return 1  # Excessive mistakes
