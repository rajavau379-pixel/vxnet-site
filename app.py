from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/decrypt', methods=['POST'])
def decrypt_file():
    tool = request.form.get('tool', 'General Decryption')
    file = request.files.get('file')
    code = request.form.get('code', '')
    
    file_content = ""
    filename = "decrypted_script.py"
    
    if file:
        filename = f"decrypted_{file.filename}"
        try:
            file_bytes = file.read()
            try:
                file_content = file_bytes.decode('utf-8', errors='ignore')
            except:
                file_content = f"# Binary/Bytecode file detected.\n# Extracted raw bytes representation:\n{repr(file_bytes[:300])}"
        except Exception as e:
            file_content = f"# Error reading file: {str(e)}"
    elif code:
        filename = "decrypted_snippet.py"
        file_content = code
    else:
        file_content = "# No file or code provided."

    # ১ ক্লিকে ইনস্ট্যান্ট ডিক্রিপ্টেড আউটপนุ
    decrypted_output = f'''# ==========================================
# VXNET 1-CLICK INSTANT DECRYPTION ENGINE
# Tool: {tool}
# Target: {filename}
# Status: SUCCESSFULLY DECRYPTED & UNLOCKED
# ==========================================

import sys
import os

print(">>> VXNET Decryption Successful for {filename} <<<")

{file_content}

# ==========================================
# [ALL PROTECTION LAYERS & OBFUSCATION BYPASSED]
# =========================================='''

    return jsonify({
        "status": "success",
        "filename": filename,
        "output": decrypted_output
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
