import re
import math

def tokenize(text):
    """Convert text to a list of tokens"""
    text = re.sub(r'[^\w\s]', '', text)  # remove punctuation
    return text.lower().split()

def get_word_counts(tokens):
    """Count the number of occurrences of each word in a list of tokens"""
    word_counts = {}
    for token in tokens:
        word_counts[token] = word_counts.get(token, 0) + 1
    return word_counts

def get_vector(word_counts, all_words):
    """Convert a dictionary of word counts to a vector of word frequencies"""
    vector = []
    for word in all_words:
        frequency = word_counts.get(word, 0)
        vector.append(frequency)
    return vector

def get_cosine_similarity(v1, v2):
    """Calculate the cosine similarity between two vectors"""
    dot_product = sum(x * y for x, y in zip(v1, v2))
    magnitude1 = math.sqrt(sum(x ** 2 for x in v1))
    magnitude2 = math.sqrt(sum(y ** 2 for y in v2))
    if not magnitude1 or not magnitude2:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)

def get_similarities(query, seen_list):
    """Calculate the cosine similarity between the query and each string in the seen list"""
    all_tokens = [tokenize(text) for text in seen_list]
    all_words = set(word for tokens in all_tokens for word in tokens)
    query_tokens = tokenize(query)
    query_counts = get_word_counts(query_tokens)
    query_vector = get_vector(query_counts, all_words)
    similarities = []
    for tokens in all_tokens:
        word_counts = get_word_counts(tokens)
        vector = get_vector(word_counts, all_words)
        similarity = get_cosine_similarity(query_vector, vector)
        similarities.append(similarity)
    return similarities

# Example usage
query = 'Chrome/5.0 ApplWebKit/537.36 (pHTML, kike cecko)'
# query = '30X40X60'

seen_list = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
  '30X40X60']

similarities = get_similarities(query, seen_list)
for i, sim in enumerate(similarities):
    print(f"Similarity of query to string {i+1}: {sim}")