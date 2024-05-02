import spacy
import numpy as np
from scipy.spatial.distance import cosine
from nltk import pos_tag, word_tokenize, sent_tokenize
from nltk.parse.corenlp import CoreNLPParser
from nltk.corpus import wordnet as wn
from nltk import Tree
import os
import pickle as pkl
import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Load English language model from SpaCy with word vectors
nlp = spacy.load("en_core_web_md")

# c.ii
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

# c.iii
parser = CoreNLPParser(url='http://localhost:9000')

def is_noun(tag):
    return tag in ['NN', 'NNS', 'NNP', 'NNPS']

def is_verb(tag):
    return tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']

def is_preposition(tag):
    return tag in ['IN']

def is_determiner(tag):
    return tag in ['DT']

def analyze_sentence_structure(pos_tags):
    errors = []
    # Check if sentence starts properly
    if pos_tags[0][1] in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
        errors.append("Error: Sentence starts with a verb.")
    if pos_tags[0][0].lower() in ['who', 'what', 'when', 'where', 'why', 'how']:
        if not is_verb(pos_tags[1][1]):
            errors.append("Error: Question formed incorrectly.")
    return errors

def noun_without_determiner(word):
    # Check if the noun is typically used without a determiner
    synsets = wn.synsets(word, pos=wn.NOUN)
    for synset in synsets:
        lexname = synset.lexname()
        # Check for uncountable nouns or nouns that are abstract concepts
        if 'substance' in lexname or 'phenomenon' in lexname or 'attribute' in lexname or 'state' in lexname:
            return True
    return False

def check_constituents(pos_tags):
    errors = []
    for i, (word, tag) in enumerate(pos_tags):
        if is_noun(tag) and tag in ['NN', 'NNP']:  # Checking only singular common and proper nouns
            if i == 0 or not (is_determiner(pos_tags[i-1][1]) or pos_tags[i-1][1] in ['POS', 'PRP$', 'CD']):
                if not noun_without_determiner(word):
                    errors.append(f"Error: Missing determiner before the noun.")
    return errors

subordinating_conjunctions = {'because', 'although', 'if', 'while', 'since', 'after', 'before', 'once', 'until', 'unless', 'as', 'though'}

def check_subordinating_conjunctions(parse_tree):
    errors = []

    def traverse_tree(subtree):
        if subtree.label() == 'PP':
            # Check if the first child is an IN node which may contain a preposition or subordinating conjunction
            preposition_or_conjunction = subtree[0].leaves()[0].lower()
            if preposition_or_conjunction in subordinating_conjunctions:
                # Check for a following clause that should contain a subject and a finite verb
                has_clause = any(child.label() == 'S' for child in subtree)
                has_finite_verb = False
                if has_clause:
                    for child in subtree:
                        if child.label() == 'S':
                            # Ensure there's a subject and a finite verb in the clause
                            has_subject = any(grandchild.label() in ['NP', 'PRP'] for grandchild in child)
                            has_finite_verb = any(grandchild.label() == 'VP' and any(ggchild.label().startswith('VB') for ggchild in grandchild) for grandchild in child)
                            if not (has_subject and has_finite_verb):
                                errors.append(f"Subordinating conjunction used without a proper clause containing a subject and a finite verb.")
            else:
                pass

        # Recursively traverse the tree
        for child in subtree:
            if isinstance(child, Tree):
                traverse_tree(child)

    traverse_tree(parse_tree)

    return errors


def parse_essay(essay):
    sentences = sent_tokenize(essay)
    error_count = 0
    for sentence in sentences:
        tokens = word_tokenize(sentence)
        pos_tags = pos_tag(tokens)
        
        # Parse the sentence using CoreNLP
        parse_tree = next(parser.raw_parse(sentence))
        
        errors = analyze_sentence_structure(pos_tags)
        errors += check_constituents(pos_tags)
        errors += check_subordinating_conjunctions(parse_tree)
        if errors:
            error_count += 1
    return error_count 

def syntatic_errors_to_score(essay):
    num_mistakes = parse_essay(essay)
    if 0 <= num_mistakes <= 1:
        return 5
    elif 2 <= num_mistakes <= 3:
        return 4
    elif 4 <= num_mistakes <= 5:
        return 3
    elif 6 <= num_mistakes <= 7:
        return 2
    else:
        return 1
        
#d.i
# Function to load pre-trained Word2Vec embeddings
def load_w2v(filepath: str):
    with open(filepath, 'rb') as fin:
        return pkl.load(fin)

# Get a word vector for a given word
def w2v(word2vec, token: str) -> np.ndarray:
    return word2vec.get(token, np.zeros(300))  # Assuming embeddings are of size 300

# Compute average word embedding for a sentence
def sentence_embedding(word2vec, tokens: list) -> np.ndarray:
    embeddings = [w2v(word2vec, token) for token in tokens if token in word2vec]
    if embeddings:
        return np.mean(embeddings, axis=0)
    return np.zeros(300)  # Return zero vector if no embeddings are found

# Compute cosine similarity between two vectors
def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Main function to compute similarity to prompt
def compute_similarity_to_prompt(prompt: str, essay_text: str, word2vec) -> float:
    prompt_embedding = sentence_embedding(word2vec, prompt.split())
    essay_sentences = essay_text.split('\n')
    sentence_embeddings = [sentence_embedding(word2vec, sentence.split()) for sentence in essay_sentences]
    similarities = [cosine_similarity(prompt_embedding, emb) for emb in sentence_embeddings if np.any(emb)]
    return np.mean(similarities)

# Compute the coherence of an essay based on cosine similarities between consecutive sentences
def essay_coherence(essay_text: str, word2vec) -> float:
    sentences = essay_text.strip().split('\n')
    sentence_embeddings = [sentence_embedding(word2vec, sentence.split()) for sentence in sentences]
    
    # Compute cosine similarities between consecutive sentence embeddings
    similarities = [cosine_similarity(sentence_embeddings[i], sentence_embeddings[i+1])
                    for i in range(len(sentence_embeddings)-1)]
    
    # Analyze the variability of these similarity scores
    if similarities:
        mean_similarity = np.mean(similarities)
        return mean_similarity
    return 0.0

def read_essay(file_name):
    try:
        with open(os.path.join('essays', file_name), 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File {file_name} not found.")
        return None

def analyze_essays(df, word2vec):
    results = {'high': {'similarity': [], 'coherence': []},
               'low': {'similarity': [], 'coherence': []}}

    for _, row in df.iterrows():
        essay_text = read_essay(row['filename'])
        if essay_text:
            sim = compute_similarity_to_prompt(row['prompt'], essay_text, word2vec)
            coherence_mean = essay_coherence(essay_text, word2vec)

            results[row['grade']]['similarity'].append(sim)
            results[row['grade']]['coherence'].append(coherence_mean)

    # Compute averages and directly return the desired values
    avg_sim_high = np.mean(results['high']['similarity']) if results['high']['similarity'] else 0
    avg_sim_low = np.mean(results['low']['similarity']) if results['low']['similarity'] else 0
    avg_coh_high = np.mean(results['high']['coherence']) if results['high']['coherence'] else 0
    avg_coh_low = np.mean(results['low']['coherence']) if results['low']['coherence'] else 0

    return avg_sim_high, avg_sim_low, avg_coh_high, avg_coh_low


def compute_similarity_coherence_score(sim_coh, avg_high, avg_low):
    midpoint = (avg_high + avg_low) / 2
    
    # Assign numeric scores based on the sim_coh
    if sim_coh >= avg_high:
        return 5
    elif sim_coh >= midpoint:
        return 4
    elif sim_coh >= avg_low:
        return 3
    elif sim_coh >= avg_low / 2:
        return 2
    else:
        return 1

    
def calculate_final_score(a, b, c, d, e, f):
    # Compute the final score
    # c = c.i + c.ii
    final_score = (2 * a) - b + c + (2 * d) + (3 * e) + f

    return final_score
