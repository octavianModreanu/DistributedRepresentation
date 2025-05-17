from train_data import TRAIN_DATA
from Categorizer import NaiveBayes
from collections import Counter
from math import log

# I want to do a character frequency distribution for each category
# I should also calculate the average length of the words in each category
nb = NaiveBayes()
input_data = "Doe"

def letter_count(ctg = None, single_input = None):
    split_tokens = []
    letters = []

    if ctg is not None:
        for key,cat in TRAIN_DATA:
            if cat["categories"][ctg] == 1:
                split_tokens.append(nb.tokenizer(key,split = 1))
        for index in split_tokens:
            for j in index:
                    j = j.lower()
                    letters.append(j)
        return dict(Counter(letters))
    elif single_input is not None:
         return dict(Counter(single_input))
    else:
        raise ValueError("letter_count does not attribute a value (At least one expected)")
         
# This is basically the probability of a letter being in a certain ctg
def letter_freq(ctg):
    total_letters = sum(ctg.values())  
    freq = {i: count / total_letters for i, count in ctg.items()}  
    return dict(sorted(freq.items()))

# i think these are initialized in the constructor
lett_frq_name = letter_freq(letter_count(ctg = "Name"))
lett_frq_age = letter_freq(letter_count(ctg = "Age"))
lett_frq_edu = letter_freq(letter_count(ctg = "Education"))
lett_frq_occ = letter_freq(letter_count(ctg = "Occupation"))
lett_frq_gang = letter_freq(letter_count(ctg = "Gang"))
lett_frq_married = letter_freq(letter_count(ctg = "Marital Status"))

# This should be in one of the helper functions i think
input_data = input_data.lower()
tokens = nb.tokenizer(input_data, split = 1)
lett_frq_tokens = letter_freq(letter_count(single_input = tokens))
# Accumulate frequencies for all tokens in the input
for token in tokens:
    token_freq = letter_count(single_input=token)
    for letter, count in token_freq.items():
        lett_frq_tokens[letter] = lett_frq_tokens.get(letter, 0) + count

lett_frq_tokens = letter_freq(lett_frq_tokens)

def KL(ctg):
    probKL = 0
    # This needs to look for the specific letter and calculate kl between those
    for key in ctg:
        for index in lett_frq_tokens:
            if key == index:
                p = lett_frq_tokens.get(index, 0)
                q = ctg.get(key, 0)
                if p > 0 and q > 0:
                    probKL += (p * log(p/q))
                    print(f"Letter: {index}   Value: {p}")
                    print(f"Ctg_Letter: {key}   Ctg_Value: {q}")
                    print(f"probKL = {p * log(p/q)}")
                else:
                    print("probKL is undefined")
    if probKL == 0:
        print(f"The distributions are not similar at all, probKL is set to 99999")
        probKL = 9999
        return probKL
    else:
        print (f"Final KL value for input '{input_data}': {probKL}\n")
        return probKL

ctgkl = ["Name", "Age", "Education", "Occupation", "Gang", "Marital Status"]
lett_frq = [lett_frq_name, lett_frq_age, lett_frq_edu, lett_frq_occ, lett_frq_gang, lett_frq_married]
probKL = {}

# Loop over each category and its corresponding letter frequency distribution
for i, freq in zip(ctgkl, lett_frq):
    probKL[i] = KL(freq)  # Compute KL divergence for each category and store it in the dictionary

print(probKL)

"""
So at this point I need to compare distributions
Doe, 30, Software Engineer, Single


"""
