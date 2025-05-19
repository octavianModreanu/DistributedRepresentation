from train_data import TRAIN_DATA, CATEGORIES
import numpy as np
from collections import Counter

class NaiveBayes:
    def __init__(self, vocab = None, vector = None):
        
        if vocab is None:
            self.vocab = {}
            
            for text, _ in TRAIN_DATA:
                for token in NaiveBayes.tokenizer(text):
                    if token not in self.vocab:
                        self.vocab[token] = len(self.vocab)
                        print(f"Added token '{token}' to vocabulary with index {self.vocab[token]}")
            print(f"Vocabulary size: {len(self.vocab)}")
        else:
            self.vocab = vocab
        
        
        if vector is None:
            self.vector = [0] * len(self.vocab)
            self.category_vectors = {cat: [0] * len(self.vocab) for cat in CATEGORIES}
            for text, ann in TRAIN_DATA:
                tokens = NaiveBayes.tokenizer(text)
                counts = [0] * len(self.vocab)
                for t in tokens:
                    idx = self.vocab.get(t)
                    if idx is not None:
                        counts[idx] += 1
                for i, c in enumerate(counts):
                    self.vector[i] += c
                for cat, flag in ann["categories"].items():
                    if flag == 1:
                        for i, c in enumerate(counts):
                            self.category_vectors[cat][i] += c
    
            self.vector_name = self.category_vectors["Name"]
            self.vector_age = self.category_vectors["Age"]
            self.vector_education = self.category_vectors["Education"]
            self.vector_occupation = self.category_vectors["Occupation"]
            self.vector_gang = self.category_vectors["Gang"]
            self.vector_married = self.category_vectors["Marital Status"]
        
        else:
            self.vector = vector
    
    # why do be this static???
    @staticmethod
    def tokenizer(input, split = 0):
        split_input = []
        if split == 0:
            for i in input:
                if i == " ":
                    return input.split(" ")
                elif i == "-":
                    return input.split("-")
                elif i == ",":
                    return input.split(",")
            else:
                return [input]
        elif split == 1:
            for i in input:
                split_input.append(i)
            return split_input
        


    
    def vectorize(self, tokens):
        for token in tokens:
            if token in self.vocab:
                self.vector[self.vocab[token]] += 1
        return self.vector
    
    def count_nonzero(self, vector):
        return int(np.count_nonzero(vector))
    
    def count_vector(self, vector):
        vector_count = Counter(vector)
        count = []
        sum = 0
        for i in vector_count:
            if i > 0:
                count.append(vector_count[i])
        for i in count:
            sum += i
        return sum


    def NaiveBayes(self, input):
        """
        I used to have something here but git didn't save it for some reason. 
        It was basically saying that i can predict stuff based on the number of letters,
        length of the word and their probability of being in each category - I'm not quite
        sure if the model is going to predict it all the time but maybe i can just add more parameters
        to measure. Can't really think of any right now but that's a future me problem. 
        """
        """
        """
       
        input = self.tokenizer(input)
        
        # This looks a bit goofy, maybe i can put some for loops in there
        for t in input:  
            idx = self.vocab.get(t) # This is just the id
            if idx is not None:
                
                likelihood_name = self.vector_name[idx]/self.count_nonzero(self.vector_name)
                likelihood_age = self.vector_age[idx]/self.count_nonzero(self.vector_age)
                likelihood_education = self.vector_education[idx]/self.count_nonzero(self.vector_education)
                likelihood_occupation = self.vector_occupation[idx]/self.count_nonzero(self.vector_occupation)
                likelihood_gang = self.vector_gang[idx]/self.count_nonzero(self.vector_gang)
                likelihood_married = self.vector_married[idx]/self.count_nonzero(self.vector_married)
        
                prior_name = self.count_vector(self.vector_name) / len(self.vector)
                prior_age = self.count_vector(self.vector_age) / len(self.vector)
                prior_education = self.count_vector(self.vector_education) / len(self.vector)
                prior_occupation = self.count_vector(self.vector_occupation) / len(self.vector)
                prior_gang = self.count_vector(self.vector_gang) / len(self.vector)
                prior_married = self.count_vector(self.vector_married) / len(self.vector)
                
                posterior_name = likelihood_name * prior_name
                posterior_age = likelihood_age * prior_age
                posterior_education = likelihood_education * prior_education
                posterior_occupation = likelihood_occupation * prior_occupation
                posterior_gang = likelihood_gang * prior_gang
                posterior_married = likelihood_married * prior_married
                
                # So i need to know which one is the highest
                scores = {
                    "Name" : posterior_name,
                    "Age" : posterior_age,
                    "Education" : posterior_education,
                    "Occupation" : posterior_occupation,
                    "Gang" : posterior_gang,
                    "Marital Status" : posterior_married
                }
                
                highest_prob_cat = max(scores, key = scores.get)
                highest_prob_val = scores[highest_prob_cat]
                
                return scores, highest_prob_cat, highest_prob_val
            else:
                return print(f"There is no {input} token in the training dataset")
        

NB = NaiveBayes()

input_text = "John Doe, 30, Software Engineer, Single"
tokens = NB.tokenizer(input_text)
vector = NB.vectorize(tokens)

print(NB.tokenizer("Single"))

            


