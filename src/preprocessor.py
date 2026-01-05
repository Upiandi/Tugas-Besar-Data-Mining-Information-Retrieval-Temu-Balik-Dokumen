# algoritma ECS dan cleaning

import re
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class Preprocessor:
    def __init__(self):
        stop_factory = StopWordRemoverFactory()
        self.stopword_remover = stop_factory.create_stop_word_remover()

        stem_factory = StemmerFactory()
        self.stemmer = stem_factory.create_stemmer()

        self.stem_cache = {}

    def clean_text(self, teks):
        teks = teks.lower()
        teks = re.sub(r'[^a-z\s]', ' ', teks)
        teks = self.stopword_remover.remove(teks)
        return teks.split()
    
    def do_stemming(self, list_kata):
        hasil_stem = []
        for kata in list_kata:
            if kata in self.stem_cache:
                hasil_stem.append(self.stem_cache[kata])
            else:
                akar_kata = self.stemmer.stem(kata)
                self.stem_cache[kata] = akar_kata
                hasil_stem.append(akar_kata)
        return " ".join(hasil_stem)
    