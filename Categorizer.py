from train_data import TRAIN_DATA, CATEGORIES


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

    @staticmethod
    def tokenizer(input):
        for i in input:
            if i == " ":
                return input.split(" ")
            elif i == "-":
                return input.split("-")
            elif i == ",":
                return input.split(",")
        else:
            return [input]

    def vectorize(self, tokens):
        for token in tokens:
            if token in self.vocab:
                self.vector[self.vocab[token]] += 1
        return self.vector

NB = NaiveBayes()

input_text = "John Doe, 30, Software Engineer, Single"
tokens = NB.tokenizer(input_text)
vector = NB.vectorize(tokens)
print(f"Tokens: {tokens}")
print(f"Vector: {vector}")


            


