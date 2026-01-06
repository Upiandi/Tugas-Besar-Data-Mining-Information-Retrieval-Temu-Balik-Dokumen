# perhitungan VSM (TF-IDF) dan cosine similarity

import math

class DPHEngine:
    def __init__(self, corpus_tokens):
        self.corpus = corpus_tokens # List of list of tokens
        self.N = len(corpus_tokens)
        self.doc_lengths = [len(doc) for doc in corpus_tokens]
        self.avg_l = sum(self.doc_lengths) / self.N
        
        # Hitung df (document frequency) untuk setiap kata unik
        self.df = {}
        for doc in corpus_tokens:
            unique_words = set(doc)
            for word in unique_words:
                self.df[word] = self.df.get(word, 0) + 1

    def calculate_score(self, query_tokens):
        scores = []
        
        for i in range(self.N):
            doc = self.corpus[i]
            l = self.doc_lengths[i]
            doc_score = 0
            
            # Hitung tf (term frequency) dalam dokumen ini
            word_counts = {}
            for word in doc:
                word_counts[word] = word_counts.get(word, 0) + 1
            
            for word in query_tokens:
                if word in word_counts and word in self.df:
                    tf = word_counts[word]
                    n = self.df[word]
                    
                    # RUMUS DPH (Divergence From Randomness)
                    # Kita pakai log2 agar sesuai standar Information Theory
                    part1 = 1 / (tf + 1)
                    part2 = math.log2((tf * self.avg_l / l) * (self.N / n))
                    
                    word_score = part1 * part2
                    doc_score += max(0, word_score) # Skor tidak boleh negatif
            
            scores.append(doc_score)
        
        return scores