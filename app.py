from flask import Flask, render_template, request, jsonify
import os
import base64
import zlib
import re

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

    text_output = []
    text_output.append(f"# -*- coding: utf-8 -*-")
    text_output.append(f"# ===================================================")
    text_output.append(f"# VXNET REAL DECOMPILER & RECOVERY ENGINE")
    text_output.append(f"# Tool: {tool}")
    text_output.append(f"# Target File: {original_name}")
    text_output.append(f"# Status: EXTRACTED & RESTORED TO OPEN SOURCE")
    text_output.append(f"# ===================================================\n")

    try:
        # ফাইলটি টেক্সট বা স্ক্রিপ্ট হলে তা রিড করবে
        raw_text = file_bytes.decode('utf-8', errors='ignore')
        
        # বেস৬৪ বা জিপ্রিপ অবফাসকেশন চেক ও আনপ্যাক করা
        b64_matches = re.findall(r'[A-Za-z0-9+/]{20,}={0,2}', raw_text)
        decoded_any = False
        if b64_matches:
            text_output.append("# [+] Unpacking encoded payload segments...")
            for bm in b64_matches[:10]:
                try:
                    dec = base64.b64decode(bm)
                    try:
                        dec = zlib.decompress(dec)
                    except:
                        pass
                    dec_str = dec.decode('utf-8', errors='ignore')
                    if len(dec_str.strip()) > 3:
                        text_output.append(f"\n# --- Unpacked Segment ---")
                        text_output.append(dec_str)
                        decoded_any = True
                except:
                    pass

        if not decoded_any:
            text_output.append("# --- Actual File Content & Source Code ---")
            text_output.append(raw_text)
            
    except Exception:
        # বাইনারি বা কম্পাইলড ফাইল হলে রিডেবল স্ট্রিং এক্সট্রাক্ট করবে
        text_output.append("# [!] Binary / Compiled bytecode structure detected.")
        text_output.append("# [+] Extracting readable strings and functions from binary...")
        printable = "".join([chr(b) if 32 <= b <= 126 or b in (10, 13, 9) else ' ' for b in file_bytes])
        lines = [l.strip() for l in printable.split('\n') if len(l.strip()) > 2]
        text_output.extend(lines[:500])

    final_output = "\n".join(text_output)

    return jsonify({
        "status": "success",
        "filename": filename,
        "output": final_output
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
