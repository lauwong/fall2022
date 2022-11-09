import random
from urllib.request import urlopen

word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

response = urlopen(word_site)
txt = response.read()
WORDS = txt.splitlines()

num_words = 6
num_pages = 6
min_word_len = 4

def check_match(word_1, word_2):
    diff_letters = 0
    expected_len = len(word_1)
    if len(word_2) != expected_len: return False
    for i in range(expected_len):
        if word_1[i] != word_2[i]:
            diff_letters += 1
            if diff_letters > 1: return False
    return diff_letters == 1

def generate_matches(word_list, min_word_len):
    match_groups = {}
    for word_1 in word_list:
        if len(word_1) >= min_word_len:
            alike_words = set()
            for word_2 in word_list:
                if check_match(word_1, word_2):
                    alike_words.add(word_2.decode())
            if len(alike_words) > 0:
                match_groups[word_1.decode()] = alike_words
    return match_groups

words_list = generate_matches(WORDS, min_word_len)

def generate_path_from_word(word_list, start_word, path_len):
    stack = [(start_word,)]
    used_words = set()
    while stack:
        word_path = stack.pop(0)
        if len(word_path) == path_len: return word_path
        new_paths = [word_path + (word,) for word in word_list[word_path[-1]] if word not in used_words]
        stack = stack + new_paths
        used_words.add(word_path[-1])
    
def generate_paths(word_list, path_len, num_paths):
    paths = []
    words = list(word_list.keys())
    while len(paths) < num_paths:
        seed_word = random.choice(words)
        path = generate_path_from_word(word_list, seed_word, path_len)
        if path: paths.append(path)
    return paths

print(generate_paths(words_list, num_pages, num_words))