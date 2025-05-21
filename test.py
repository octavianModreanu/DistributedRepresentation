from train_data import TRAIN_DATA
from train_data import CATEGORIES
from Categorizer import NaiveBayes
from collections import Counter
from math import log
import numpy as np


"""
I want to do a character frequency distribution for each category
I should also calculate the average length of the words in each category


So, I want to implement cosine similarity on letter frequency distribution
If I have time maybe I can also implement the word length thing. 
"""
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


def KL(ctg):
    """
    KL Divergence gives you a quantitative measure of how much one distribution differs from another
    """
    probKL = 0
    # This needs to look for the specific letter and calculate kl between those
    for key in ctg:
        for index in lett_frq_tokens:
            if key == index:
                p = lett_frq_tokens.get(index, 0)
                q = ctg.get(key, 0)
                if p > 0 and q > 0:
                    probKL += (p * log(p/q))
                    #print(f"Letter: {index}   Value: {p}")
                    #print(f"Ctg_Letter: {key}   Ctg_Value: {q}")
                    #print(f"probKL = {p * log(p/q)}")
                else:
                    print(f"probKL is undefined for {key}")
    if probKL == 0:
        print(f"The distributions are not similar at all, probKL is set to 99999")
        probKL = 99999
        return probKL
    else:
        #print (f"Final KL value for input '{input_data}': {probKL}\n")
        return probKL

def cos_sim(dict_input):
    """
    Cosine similarity divides the direction of the vectors by their magnitude so 
    lengths of the vectors don't matter. 
    """
    lett_freq = [lett_frq_name,lett_frq_age,lett_frq_edu,lett_frq_occ,lett_frq_gang,lett_frq_married]
    cos_sim_dict = {}
    
    for frq, cat in zip(lett_freq,CATEGORIES):
        keys = list(frq.keys())
        vector_input = np.array([dict_input.get(k, 0) for k in keys])
        vector_cat = np.array([frq.get(k, 0) for k in keys])
        norm_product = np.linalg.norm(vector_input) * np.linalg.norm(vector_cat)
        if norm_product == 0:
            cos_sim_dict[cat] = float('nan')
        else:
            cos_sim_dict[cat] = np.dot(vector_input,vector_cat)/ norm_product
    return cos_sim_dict

nb = NaiveBayes()
input_data = "John"

# i think these are initialized in the constructor
# and they should also be called "character_frq"
lett_frq_name = letter_freq(letter_count(ctg = "Name"))
lett_frq_age = letter_freq(letter_count(ctg = "Age")) # this doesn't apply to age since it breaks them apart
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

lett_frq = [lett_frq_name, lett_frq_age, lett_frq_edu, lett_frq_occ, lett_frq_gang, lett_frq_married]
probKL = {}

mama = cos_sim(lett_frq_tokens)



# Loop over each category and its corresponding letter frequency distribution
for i, freq in zip(CATEGORIES, lett_frq):
    probKL[i] = KL(freq)

print(probKL)
print(mama)
"""
So at this point I need to compare distributions
Doe, 30, Software Engineer, Single



"""
