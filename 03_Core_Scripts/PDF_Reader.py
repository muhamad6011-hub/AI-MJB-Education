import PyPDF2
import json
import os
from datetime import datetime

# Konfigurasi Folder - Menggunakan r"" agar aman dari karakter backslash
input_folder = r"D:\Mr\Proyek Ai\Ai-MJB-Edu\05_Knowledge_Base"
output_folder = r"D:\Mr\Proyek Ai\Ai-MJB-Edu\01_Mining_Raw"

def extract_all_pdfs():
    # Pastikan folder output ada
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List semua file di folder knowledge base
    files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]

    if not files:
        print(f"❌ Tidak ada file PDF ditemukan di: {input_folder}")
        return

    for file_name in files:
        pdf_path = os.path.join(input_folder, file_name)
        print(f"📖 Sedang memproses: {file_name}...")

        try:
            with open(pdf_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                text = ""
                # Ambil teks dari setiap halaman
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
                
                # Bungkus jadi data JSON
                data = {
                    "Source": "Book Knowledge",
                    "Title": file_name,
                    "Content": text,
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Simpan hasil
                json_name = f"BOOK_{file_name.replace('.pdf', '')}.json"
                output_path = os.path.join(output_folder, json_name)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                
                print(f"✅ Berhasil! Data buku disimpan ke: {json_name}")

        except Exception as e:
            print(f"⚠️ Gagal memproses {file_name}: {e}")

if __name__ == "__main__":
    extract_all_pdfs()