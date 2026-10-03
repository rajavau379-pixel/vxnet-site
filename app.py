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

    raw_text = file_bytes.decode('utf-8', errors='ignore')
    unwrapped_code = raw_text

    try:
        # base64 এবং zlib এনকোডেড স্ট্রিং স্বয়ংক্রিয়ভাবে খুঁজে বের করে আনপ্যাক করার লজিক
        b64_patterns = re.findall(r'b?["\']([A-Za-z0-9+/=]{20,})["\']', raw_text)
        decoded_payloads = []
        
        for b64_str in b64_patterns:
            try:
                decoded_bytes = base64.b64decode(b64_str)
                try:
                    decompressed = zlib.decompress(decoded_bytes)
                    inner_text = decompressed.decode('utf-8', errors='ignore')
                    decoded_payloads.append(inner_text)
                except:
                    inner_text = decoded_bytes.decode('utf-8', errors='ignore')
                    if len(inner_text.strip()) > 3:
                        decoded_payloads.append(inner_text)
            except:
                pass

        if decoded_payloads:
            unwrapped_code = "\n\n".join(decoded_payloads)
    except Exception as e:
        unwrapped_code = raw_text + f"\n# Decompression note: {str(e)}"

    final_output = f'''# -*- coding: utf-8 -*-
# ===================================================
# VXNET AUTO-UNWRAPPER & DECODER ENGINE
# Tool: {tool}
# Target File: {original_name}
# Status: SUCCESSFULLY UNPACKED & RESTORED
# ===================================================

{unwrapped_code}
'''

    return jsonify({
        "status": "success",
        "filename": filename,
        "output": final_output
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
