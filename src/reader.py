# membaca folder pdf, docs, dan txt

import os
import fitz
import docx

def baca_semua_file(path_folder):
    daftar_teks = []
    daftar_nama_file = []
    
    if not os.path.exists(path_folder):
        print(f'folder {path_folder} tidak ditemukan')
        return daftar_teks, daftar_nama_file
    
    for nama_file in os.listdir(path_folder):
        path_lengkap = os.path.join(path_folder, nama_file)
        teks_dokumen = ''

        # cek txt
        if nama_file.endswith('.txt'):
            with open(path_lengkap, 'r', encoding='utf-8', errors='ignore') as f:
                teks_dokumen = f.read()
                pass

        # cek pdf
        elif nama_file.endswith('.pdf'):
            with fitz.open(path_lengkap) as doc:
                try:
                    for halaman in doc:
                        teks_dokumen += halaman.get_text()
                    pass
                except Exception as e:
                    print(f'Gagal membaca file PDF {nama_file}: {e}')

        # cek docs
        elif nama_file.endswith('.docx'):
            try:
                doc = docx.Document(path_lengkap)
                teks_dokumen = '\n'.join([paragraf.text for paragraf in doc.paragraphs])
            except Exception as e:
                print(f'Gagal membaca file Docs {nama_file}: {e}')

        if teks_dokumen:
            daftar_teks.append(teks_dokumen)
            daftar_nama_file.append(nama_file)
        
    return daftar_teks, daftar_nama_file

hasil, nama = baca_semua_file('../data')
print(f'Total jumlah dokumen terbaca: {len(hasil)}')
for nama_file, isi_teks in zip(nama, hasil):
    print(f'Nama file: {nama_file}')
    print(f'Isi teks: {isi_teks[:200]}')
    print('-'*50)