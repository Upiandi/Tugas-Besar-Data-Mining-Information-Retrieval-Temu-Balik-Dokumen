from preprocessor import Preprocessor

p = Preprocessor()
kata_kotor = "Mahasiswa sedang MENGERJAKAN Tugas Besar di Lab. Komputer 101! kampus Tsinghua"

kata_bersih = p.clean_text(kata_kotor)
print(f'Kata Bersih: {kata_bersih}')

kata_dasar = p.do_stemming(kata_bersih)
print(f'Kata Dasar: {kata_dasar}')