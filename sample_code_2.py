import spacy
import numpy as np
from scipy.spatial.distance import cosine
from nltk import pos_tag, word_tokenize, sent_tokenize
import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Load English language model from SpaCy with word vectors
nlp = spacy.load("en_core_web_md")

def string_to_vec(sentence):
    """
    Converts a sentence into an average word vector, excluding stop words and focusing only on tokens with vectors.
    """
    doc = nlp(sentence)
    vectors = [token.vector for token in doc if not token.is_stop and token.has_vector]
    return np.mean(vectors, axis=0) if vectors else np.zeros((300,))  # Assuming 300 dimensions

def cosine_similarity(vec1, vec2):
    """
    Compute the cosine similarity between two vectors, handling cases where vectors might be zero.
    """
    if np.all(vec1 == 0) or np.all(vec2 == 0):
        return 0  # Handle cases where vector might be zero
    return 1 - cosine(vec1, vec2)

def essay_address_topic(essay, prompt):
    """
    Computes how well the essay addresses the prompt using cosine similarity (part d.i).
    This is determined between the prompt's topic vector and the average vector of the essay's sentences.
    """
    topic_vector = string_to_vec(prompt)
    essay_sentences = [sent.text for sent in nlp(essay).sents]
    sentence_vectors = [string_to_vec(sentence) for sentence in essay_sentences]
    essay_vector = np.mean(sentence_vectors, axis=0) if sentence_vectors else np.zeros((300,))
    return cosine_similarity(topic_vector, essay_vector)

def essay_coherence(essay):
    """
    Computes the coherence of the essay by analyzing cosine similarity between consecutive sentences (part d.ii).
    """
    essay_sentences = [sent.text for sent in nlp(essay).sents]
    sentence_vectors = [string_to_vec(sentence) for sentence in essay_sentences]
    similarities = [cosine_similarity(sentence_vectors[i], sentence_vectors[i+1]) for i in range(len(sentence_vectors)-1)]
    return np.std(similarities) if similarities else 0, similarities

def analyze_essay_coherence_and_topic(essay, prompt):
    """
    Integrates analysis for both the topic relevance (d.i) and coherence (d.ii) of an essay.
    """
    topic_relevance = essay_address_topic(essay, prompt)
    coherence_std, coherence_similarities = essay_coherence(essay)
    return topic_relevance, coherence_std, coherence_similarities

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
    tokens = word_tokenize(sentence)
    tagged = pos_tag(tokens)
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
        if check_subject_verb_agreement(sentence):
            error_sentences.add(sentence)
    return error_sentences

def verb_tense_errors(essay):
    sentences = sent_tokenize(essay)
    error_sentences = set()
    for sentence in sentences:
        tagged = pos_tag(word_tokenize(sentence))
        past_tense_verbs = sum(tag in ['VBD', 'VBN'] for word, tag in tagged)
        non_past_tense_verbs = sum(tag in ['VB', 'VBG', 'VBP', 'VBZ'] for word, tag in tagged)
        if past_tense_verbs > 0 and non_past_tense_verbs > 0:
            error_sentences.add(sentence)
    return error_sentences

def missing_verb_extra_verb_errors(essay):
    sentences = sent_tokenize(essay)
    error_sentences = set()
    for sentence in sentences:
        tagged = pos_tag(word_tokenize(sentence))
        verb_count = sum(1 for word, tag in tagged if tag.startswith('VB'))
        expected_verbs_count = 1 + sum(1 for word, tag in tagged if tag in ['CC', 'IN', 'TO', 'WDT', 'WP', 'WRB'])
        if verb_count == 0 or verb_count > expected_verbs_count+1:
            error_sentences.add(sentence)
    return error_sentences

def total_verb_errors(essay):
    error_sentences = subject_verb_agreement_errors(essay) | verb_tense_errors(essay) | missing_verb_extra_verb_errors(essay)
    return error_sentences, len(subject_verb_agreement_errors(essay)), len(verb_tense_errors(essay)), len(missing_verb_extra_verb_errors(essay))

def verb_errors_to_score(essay):
    num_mistakes = len(total_verb_errors(essay)[0])
    if num_mistakes == 0:
        return 5
    elif 1 <= num_mistakes <= 2:
        return 4
    elif 3 <= num_mistakes <= 4:
        return 3
    elif 5 <= num_mistakes <= 6:
        return 2
    else:
        return 1
