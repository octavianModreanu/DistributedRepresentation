from train_data import TRAIN_DATA
from Categorizer import NaiveBayes
from collections import Counter

# I want to do a character frequency distribution for each category
nb = NaiveBayes()
input_data = "John Doe, 30, Software Engineer, Single"

def letter_count(ctg):
    split_tokens = []
    letters = []

    for key,cat in TRAIN_DATA:
        if cat["categories"][ctg] == 1:
            split_tokens.append(nb.tokenizer(key,split=1))
    for index in split_tokens:
        for j in index:
                letters.append(j)
    return dict(Counter(letters))

Name = dict(sorted(letter_count(ctg = "Name").items()))
Gang = dict(sorted(letter_count(ctg = "Gang").items()))
print(Counter(Name).most_common(20)[0])
print(Counter(Gang).most_common(20)[0])
"""
So at this point I need to compare distributions
i need peak, spread,

"""
