from train_data import TRAIN_DATA
from Categorizer import NaiveBayes
from collections import Counter

# I want to do a character frequency distribution for each category
# I should also calculate the average length of the words in each category
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
                j = j.lower()
                letters.append(j)
    return dict(Counter(letters))

Name = dict(sorted(letter_count(ctg = "Name").items()))
Gang = dict(sorted(letter_count(ctg = "Gang").items()))
dict_name = dict(Counter(Name))
freq_name = {}
for i in dict_name:
     freq_name.update({f"{i}": dict_name[i]/Counter(Name).total()})
print(Counter(Name).total())

#print(Counter(Gang).total())
"""
So at this point I need to compare distributions

"""
