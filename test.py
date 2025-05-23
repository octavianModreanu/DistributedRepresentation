from train_data import TRAIN_DATA, CATEGORIES
from Categorizer import NaiveBayes
from collections import Counter, defaultdict
from math import log
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# === Helper: Letter Frequency ===
def letter_count_for_category(category):
    letters = []
    for key, cat in TRAIN_DATA:
        if cat["categories"][category] == 1:
            letters.extend(list(key.lower()))
    return dict(Counter(letters))

def letter_freq(counter):
    total = sum(counter.values())
    return {ch: count / total for ch, count in counter.items()} if total else {}

def letter_freq_from_text(text):
    counter = Counter([ch for ch in text.lower() if ch.isalpha()])
    return letter_freq(counter)

# === Helper: Feature Extraction for Logistic Regression ===
def extract_features(word, category_ngrams, ng_nb, category_list, category_letter_freqs):
    length = len(word)
    num_digits = sum(c.isdigit() for c in word)
    num_alpha = sum(c.isalpha() for c in word)
    has_space = int(' ' in word)
    has_hyphen = int('-' in word)
    is_title = int(word.istitle())
    # NGram Overlap
    _, ngram_overlap_scores = predict_category_ngram(word, category_ngrams, category_letter_freqs)
    ngram_overlap_feat = [ngram_overlap_scores[cat] for cat in category_list]
    # NGramNB logprobs
    _, ngramnb_scores = ng_nb.predict(word, return_scores=True)
    ngramnb_feat = [ngramnb_scores.get(cat, 0.0) for cat in category_list]
    # Replace any inf/-inf/nan with -20 or 0
    clean_ngramnb_feat = [x if np.isfinite(x) else -20.0 for x in ngramnb_feat]
    # If you want to sanitize ngram_overlap_feat as well (rare), do the same:
    clean_ngram_overlap_feat = [x if np.isfinite(x) else 0.0 for x in ngram_overlap_feat]
    return np.array([length, num_digits, num_alpha, has_space, has_hyphen, is_title] + clean_ngram_overlap_feat + clean_ngramnb_feat)

def predict_with_lr(word):
    feats = extract_features(word, category_ngrams, ng_nb, CATEGORIES, category_letter_freqs).reshape(1, -1)
    feats_scaled = scaler.transform(feats)
    pred = clf.predict(feats_scaled)[0]
    probs = clf.predict_proba(feats_scaled)[0]
    prob_dict = {cat: prob for cat, prob in zip(clf.classes_, probs)}
    return pred, prob_dict

def format_probs(prob_dict, decimals=3):
    top2 = sorted(prob_dict.items(), key=lambda x: -x[1])[:2]
    return ", ".join([f"{cat}: {prob:.{decimals}f}" for cat, prob in top2])

# === Helper: KL Divergence & Cosine Similarity ===
def kl_divergence(p, q):
    keys = set(p.keys()).union(q.keys())
    eps = 1e-10
    return sum(
        p.get(k, 0) * np.log((p.get(k, 0) + eps) / (q.get(k, 0) + eps))
        if p.get(k, 0) > 0 else 0
        for k in keys
    )

def cosine_similarity(p, q):
    keys = set(p.keys()).union(q.keys())
    v1 = np.array([p.get(k, 0) for k in keys])
    v2 = np.array([q.get(k, 0) for k in keys])
    norm = np.linalg.norm(v1) * np.linalg.norm(v2)
    return np.dot(v1, v2) / norm if norm else 0

# === N-Gram Utilities ===
def get_ngrams(text, n):
    text = f"_{text.lower()}_"
    return [text[i:i+n] for i in range(len(text)-n+1)]

def get_all_ngrams(text):
    return get_ngrams(text, 2) + get_ngrams(text, 3)

# === N-Gram Overlap Model ===
def build_category_ngrams(train_data):
    cat_ngrams = defaultdict(Counter)
    for word, meta in train_data:
        cat = next(c for c, val in meta["categories"].items() if val == 1)
        ngrams = get_all_ngrams(word)
        cat_ngrams[cat].update(ngrams)
    return cat_ngrams

def predict_category_ngram(text, category_ngrams, category_letter_freqs):
    word_ngrams = Counter(get_all_ngrams(text))
    cat_scores = {cat: sum(min(word_ngrams[ng], ngram_counter[ng]) for ng in word_ngrams)
                  for cat, ngram_counter in category_ngrams.items()}
    max_score = max(cat_scores.values())
    tied = [cat for cat, score in cat_scores.items() if score == max_score]
    if len(tied) == 1:
        return tied[0], cat_scores
    # Tiebreak: KL divergence, then cosine
    input_freq = letter_freq_from_text(text)
    kl_scores = {cat: kl_divergence(input_freq, category_letter_freqs[cat]) for cat in tied}
    min_kl = min(kl_scores.values())
    kl_tied = [cat for cat, v in kl_scores.items() if v == min_kl]
    if len(kl_tied) == 1:
        return kl_tied[0], cat_scores
    cos_scores = {cat: cosine_similarity(input_freq, category_letter_freqs[cat]) for cat in kl_tied}
    max_cos = max(cos_scores.values())
    cos_tied = [cat for cat, v in cos_scores.items() if v == max_cos]
    return cos_tied[0] if len(cos_tied) == 1 else (cos_tied, cat_scores)

# === NGram Naive Bayes Model ===
class NGramNaiveBayes:
    def __init__(self, train_data, categories, ngram_sizes=(2, 3), smoothing=1):
        self.ngram_sizes = ngram_sizes  # tuple, e.g., (2,3) for bigram and trigram
        self.smoothing = smoothing
        self.categories = categories
        self.cat_ngram_counts = {cat: Counter() for cat in categories}
        self.cat_total_ngrams = {cat: 0 for cat in categories}
        self.vocab = set()
        self._train(train_data)
        
    def get_ngrams(self, word):
        word = f"_{word.lower()}_"
        ngrams = []
        for n in self.ngram_sizes:
            ngrams.extend([word[i:i+n] for i in range(len(word)-n+1)])
        return ngrams
    
    def _train(self, train_data):
        for text, meta in train_data:
            cat = next(c for c, val in meta["categories"].items() if val == 1)
            ngrams = self.get_ngrams(text)
            self.cat_ngram_counts[cat].update(ngrams)
            self.cat_total_ngrams[cat] += len(ngrams)
            self.vocab.update(ngrams)
        self.vocab = sorted(self.vocab)
        self.vocab_size = len(self.vocab)
        
    def predict(self, word, return_scores=False):
        ngrams = self.get_ngrams(word)
        contains_letter = any(c.isalpha() for c in word)
        categories = [cat for cat in self.categories if not (contains_letter and cat == "Age")]
        scores = {}
        for cat in categories:
            logprob = 0
            seen = sum(ng in self.cat_ngram_counts[cat] for ng in ngrams)
            if seen == 0:
                scores[cat] = -float('inf')
                continue
            for ng in ngrams:
                ng_count = self.cat_ngram_counts[cat].get(ng, 0)
                prob = (ng_count + self.smoothing) / (self.cat_total_ngrams[cat] + self.smoothing * self.vocab_size)
                logprob += np.log(prob)
            scores[cat] = logprob
        if not scores:
            return "N/A", {}
        best_cat = max(scores, key=scores.get)
        if return_scores:
            return best_cat, scores
        return best_cat

# === Build all model resources ===
nb = NaiveBayes()
ng_nb = NGramNaiveBayes(TRAIN_DATA, CATEGORIES, ngram_sizes=(2,3))
category_ngrams = build_category_ngrams(TRAIN_DATA)
category_letter_freqs = {cat: letter_freq(letter_count_for_category(cat)) for cat in CATEGORIES}
# Build features and labels for logistic regression
X = []
y = []
for word, meta in TRAIN_DATA:
    cat = next(c for c, val in meta["categories"].items() if val == 1)
    X.append(extract_features(word, category_ngrams, ng_nb, CATEGORIES, category_letter_freqs))
    y.append(cat)
X = np.array(X)
y = np.array(y)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
clf = LogisticRegression(max_iter=2000, solver='lbfgs')
clf.fit(X_scaled, y)



# === Test and compare ===
test_words = [
    "Thomas","Kevin", "Liam", "Oliver", "24", "Olivia", "Miller", "Smith",
    "Trey Gangesters", "Bounty Hunter Bloods", "United Blood Nation", "10th Street Gang"
]

print(f"{'Input':16} | {'WholeWordNB':15} | {'NGram-Overlap':15} | {'NGramNB':15} | {'LR':15}")
print('-'*90)
for word in test_words:
    # Whole-word Naive Bayes
    try:
        nb_scores, nb_pred, nb_prob = nb.NaiveBayes(word)
    except Exception:
        nb_pred = "N/A"
    # N-gram overlap (with tiebreakers)
    pred, scores = predict_category_ngram(word, category_ngrams, category_letter_freqs)
    # N-gram Naive Bayes
    ng_pred, ng_scores = ng_nb.predict(word, return_scores=True)
    # Logistic Regression
    lr_pred, lr_probs = predict_with_lr(word)
    print(f"{word:16} | {nb_pred:15} | {pred:15} | {ng_pred:15} | {lr_pred:15}")
    print(f"    LR Top2: {format_probs(lr_probs)}")
    # Optional: print probability distribution for LR
    print(f"    LR Probabilities: {lr_probs}")
    # Show tiebreakers if overlap has tie
    max_score = max(scores.values())
    tied = [cat for cat, score in scores.items() if score == max_score]
    if len(tied) > 1:
        print(f"   Tie between: {tied}")
        input_freq = letter_freq_from_text(word)
        for cat in tied:
            kl = kl_divergence(input_freq, category_letter_freqs[cat])
            cos = cosine_similarity(input_freq, category_letter_freqs[cat])
            print(f"      {cat:15} | KL: {kl:.5f} | Cosine: {cos:.5f}")


