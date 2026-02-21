from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import shutil
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATA_DIR = './data'
BACKUP_DIR = './data/backups'
DATA_FILE = os.path.join(DATA_DIR, 'bigdata_memory.json')

@app.route('/save_memory', methods=['POST'])
def save_memory():
    try:
        # Buat folder jika belum ada
        for folder in [DATA_DIR, BACKUP_DIR]:
            if not os.path.exists(folder):
                os.makedirs(folder)

        new_data = request.json
        
        # 1. BACA DATA LAMA
        all_memory = []
        if os.path.exists(DATA_FILE):
            # BUAT BACKUP SEBELUM MODIFIKASI
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            shutil.copy2(DATA_FILE, os.path.join(BACKUP_DIR, f'backup_{timestamp}.json'))
            
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                try: all_memory = json.load(f)
                except: all_memory = []

        # 2. TAMBAH DATA BARU
        all_memory.append(new_data)

        # 3. SIMPAN PERMANEN
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_memory, f, indent=4)

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Memori Baru Disimpan & Backup Dibuat.")
        return jsonify({"status": "success", "message": "Data aman & Backup sukses"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("------------------------------------------")
    print("MJB-EDU SYSTEM: BIG DATA + AUTO BACKUP")
    print("STATUS: ONLINE")
    print("------------------------------------------")
    app.run(port=5000)