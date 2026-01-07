import os
import math
import PyPDF2
from docx import Document

# === 1. READER: Bisa baca PDF, DOCX, TXT ===
class DocReader:
    def read(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        try:
            if ext == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            elif ext == '.pdf':
                text = ""
                with open(file_path, 'rb') as f:
                    pdf = PyPDF2.PdfReader(f)
                    for page in pdf.pages:
                        text += page.extract_text() or ""
                return text
            elif ext == '.docx':
                doc = Document(file_path)
                return "\n".join([p.text for p in doc.paragraphs])
        except Exception as e:
            print(f"Gagal baca {file_path}: {e}")
        return ""

# === 2. PREPROCESSOR: Pembersihan Teks Sederhana ===
def preprocess(text):
    # Case folding & buang karakter non-huruf
    tokens = "".join([c.lower() if c.isalnum() else " " for c in text]).split()
    return tokens

# === 3. ENGINE: DPH (Divergence From Randomness) ===
class DPHEngine:
    def __init__(self, corpus_dict):
        # corpus_dict = { filename: [tokens] }
        self.filenames = list(corpus_dict.keys())
        self.corpus = list(corpus_dict.values())
        self.N = len(self.corpus)
        self.doc_lengths = [len(doc) for doc in self.corpus]
        self.avg_l = sum(self.doc_lengths) / self.N if self.N > 0 else 0
        
        # Hitung Document Frequency (df)
        self.df = {}
        for doc in self.corpus:
            for word in set(doc):
                self.df[word] = self.df.get(word, 0) + 1

    def search(self, query):
        query_tokens = preprocess(query)
        results = []

        for i in range(self.N):
            l = self.doc_lengths[i]
            if l == 0: continue
            
            doc_tokens = self.corpus[i]
            score = 0
            
            # Hitung TF dalam dokumen
            word_counts = {}
            for word in doc_tokens:
                word_counts[word] = word_counts.get(word, 0) + 1

            for word in query_tokens:
                if word in word_counts and word in self.df:
                    tf = word_counts[word]
                    n = self.df[word]
                    
                    # RUMUS DPH
                    # part1: 1 / (tf + 1)
                    # part2: log2( (tf * avg_l / l) * (N / n) )
                    part1 = 1 / (tf + 1)
                    val = (tf * self.avg_l / l) * (self.N / n)
                    if val > 0:
                        score += part1 * math.log2(val)
            
            results.append((self.filenames[i], round(max(0, score), 4)))
        
        # Sorting berdasarkan skor tertinggi
        return sorted(results, key=lambda x: x[1], reverse=True)

# === 4. MAIN PROGRAM: Jalur Eksekusi ===
def main():
    folder_path = "./data" # Ganti dengan nama folder dokumenmu
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' tidak ditemukan!")
        return

    reader = DocReader()
    raw_data = {}

    print("Sedang membaca dokumen...")
    for filename in os.listdir(folder_path):
        path = os.path.join(folder_path, filename)
        content = reader.read(path)
        if content:
            raw_data[filename] = preprocess(content)

    engine = DPHEngine(raw_data)
    print(f"Berhasil memuat {len(raw_data)} dokumen.\n")

    while True:
        query = input("Masukkan kata kunci (atau 'exit' untuk keluar): ")
        if query.lower() == 'exit': break
        
        rankings = engine.search(query)
        
        print(f"\nHasil Pencarian untuk: '{query}'")
        print("-" * 40)
        found = False
        for file, score in rankings:
            if score > 0:
                print(f"[{score}] {file}")
                found = True
        
        if not found:
            print("Tidak ada dokumen yang relevan.")
        print("-" * 40 + "\n")

if __name__ == "__main__":
    main()