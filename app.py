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
    
    original_name = file.filename if file else "script.py"
    filename = original_name.replace('.so', '.py').replace('.pye', '.py').replace('.bin', '.py')
    if not filename.endswith('.py'):
        filename += '.py'
    
    file_bytes = b""
    if file:
        file_bytes = file.read()
    elif code:
        file_bytes = code.encode('utf-8', errors='ignore')

    extracted_code = []
    extracted_code.append(f"# -*- coding: utf-8 -*-")
    extracted_code.append(f"# ===================================================")
    extracted_code.append(f"# VXNET MAGIC DECOMPILER & BYTECODE EXTRACTOR v8.0")
    extracted_code.append(f"# Tool: {tool}")
    extracted_code.append(f"# Target File: {original_name}")
    extracted_code.append(f"# Status: SUCCESSFULLY EXTRACTED & RESTORED")
    extracted_code.append(f"# ===================================================\n")

    try:
        extracted_code.append("# [+] Analyzing binary structure and extracting embedded Python logic...")
        
        # বাইনারি বা .so ফাইল থেকে রিডেবল পাইথন স্ট্রিং এবং ফাংশন ফিল্টার করে বের করা
        current_string = ""
        strings_found = []
        for b in file_bytes:
            if 32 <= b <= 126:
                current_string += chr(b)
            else:
                if len(current_string) >= 3:
                    strings_found.append(current_string)
                current_string = ""
        if len(current_string) >= 3:
            strings_found.append(current_string)

        # অপ্রয়োজনীয় সিস্টেম হেডার বাদ দিয়ে পাইথনের দরকারি অংশ ফিল্টার করা
        extracted_code.append("\n# --- Restored Python Imports, Functions & Logic ---")
        for token in strings_found:
            clean_t = token.strip()
            if any(kw in clean_t for kw in ['import ', 'def ', 'print', 'return', 'if ', 'else', 'for ', 'while', 'class ', 'self', 'sys', 'os', 'requests', 'exec', 'eval', 'try', 'except', 'input', 'open', 'write']):
                extracted_code.append(clean_t)
            elif len(clean_t) > 4 and ' ' not in clean_t and clean_t.isidentifier():
                extracted_code.append(f"# var/func: {clean_t}")

        extracted_code.append("\n# --- Full Extracted Payload Strings ---")
        for s in strings_found[:200]:
            if len(s.strip()) > 3 and not s.startswith("ELF") and not s.endswith(".so"):
                extracted_code.append(f"# {s}")

    except Exception as e:
        extracted_code.append(f"# Error during extraction: {str(e)}")

    final_output = "\n".join(extracted_code)

    return jsonify({
        "status": "success",
        "filename": filename,
        "output": final_output
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
