import streamlit as st
import os
import math
import PyPDF2
import pickle
from docx import Document

# --- KELAS & FUNGSI (SAMA DENGAN SEBELUMNYA) ---
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
        except Exception:
            return ""
        return ""

def preprocess(text):
    tokens = "".join([c.lower() if c.isalnum() else " " for c in text]).split()
    return tokens

class DPHEngine:
    def __init__(self, corpus_dict):
        self.filenames = list(corpus_dict.keys())
        self.corpus = list(corpus_dict.values())
        self.N = len(self.corpus)
        self.doc_lengths = [len(doc) for doc in self.corpus]
        self.avg_l = sum(self.doc_lengths) / self.N if self.N > 0 else 0
        
        # OPTIMASI: Pre-calculate Term Frequency untuk setiap dokumen
        self.tf_maps = []
        self.df = {}
        for doc in self.corpus:
            counts = {}
            for word in doc:
                counts[word] = counts.get(word, 0) + 1
            self.tf_maps.append(counts)
            
            # Hitung DF
            for word in counts.keys():
                self.df[word] = self.df.get(word, 0) + 1

    def search(self, query):
        query_tokens = preprocess(query)
        results = []
        for i in range(self.N):
            l = self.doc_lengths[i]
            if l == 0: continue
            
            score = 0
            doc_tf = self.tf_maps[i] # Ambil tf yang sudah dihitung sebelumnya
            
            for word in query_tokens:
                if word in doc_tf and word in self.df:
                    tf = doc_tf[word]
                    n = self.df[word]
                    
                    part1 = 1 / (tf + 1)
                    val = (tf * self.avg_l / l) * (self.N / n)
                    if val > 1: # Log2 dari angka < 1 itu negatif, kita hindari
                        score += part1 * math.log2(val)
            
            results.append((self.filenames[i], round(max(0, score), 4)))
        return sorted(results, key=lambda x: x[1], reverse=True)

# --- TAMPILAN STREAMLIT ---
st.set_page_config(page_title="DPH Search Engine", page_icon="🔍")

st.title("🔍 DPH Document Search Engine")
st.markdown("""
Sistem pencarian dokumen menggunakan model **DPH (Divergence From Randomness)**. 
Mampu membaca file **PDF, DOCX, dan TXT**.
""")

# Sidebar untuk upload atau pilih folder
st.sidebar.header("Konfigurasi")
folder_path = st.sidebar.text_input("Path Folder Dokumen", value="../data")

if st.sidebar.button("Muat Ulang Dokumen"):
    st.cache_data.clear()

@st.cache_resource
def load_data(path):
    cache_file = "metadata_cache.pkl"
    
    # Cek apakah file cache sudah ada?
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            st.info("⚡ Memuat data dari cache permanen (Instan)...")
            return pickle.load(f)
    
    # Kalau belum ada, baru baca manual (Lama)
    if not os.path.exists(path): return None
    
    reader = DocReader()
    data = {}
    progress_bar = st.progress(0)
    files = os.listdir(path)
    total_files = len(files)
    
    st.write("📂 Memproses dokumen pertama kali...")
    for idx, filename in enumerate(files):
        content = reader.read(os.path.join(path, filename))
        if content:
            data[filename] = preprocess(content)
        progress_bar.progress((idx + 1) / total_files)
    
    # SIMPAN KE CACHE PERMANEN
    with open(cache_file, 'wb') as f:
        pickle.dump(data, f)
        
    return data

data = load_data(folder_path)

if data:
    st.sidebar.success(f"✅ {len(data)} Dokumen berhasil dimuat!")
    engine = DPHEngine(data)

    # Input Pencarian
    query = st.text_input("Apa yang ingin Anda cari hari ini?", placeholder="Masukkan kata kunci...")

    if query:
        rankings = engine.search(query)
        
        st.subheader(f"Hasil Pencarian untuk: '{query}'")
        
        # Filter skor > 0
        filtered_results = [r for r in rankings if r[1] > 0]
        
        if filtered_results:
            for idx, (file, score) in enumerate(filtered_results):
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"**{idx+1}. {file}**")
                    with col2:
                        st.info(f"Skor: {score}")
                    st.divider()
        else:
            st.warning("Maaf, tidak ada dokumen yang relevan.")
else:
    st.error("Folder tidak ditemukan atau kosong. Silakan periksa 'Path Folder' di sidebar.")

st.caption("Tugas Besar Information Retrieval - Model DPH (Hypergeometric)")