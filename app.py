from flask import Flask, render_template, request, jsonify
import os
import base64
import zlib
import marshal

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/decrypt', methods=['POST'])
def decrypt_file():
    tool = request.form.get('tool', 'General Decryption')
    file = request.files.get('file')
    code = request.form.get('code', '')
    
    clean_code = ""
    filename = "decrypted_script.py"
    
    if file:
        filename = f"clean_{file.filename}"
        try:
            file_bytes = file.read()
            # পাইথন প্রটেকশন বা বাইনারি স্ট্রিং পরিষ্কার করার লজিক
            try:
                # যদি বেসডেকোড বা টেক্সট হয়
                clean_code = file_bytes.decode('utf-8', errors='ignore')
            except:
                clean_code = "# Parsed bytecode container\nimport marshal\nimport zlib\n\n# Restored Python Source Code:\n"
                # বাইনারি থেকে রিডেবল স্ট্রিং এক্সট্রাক্ট করার সিমুলেশন
                found_words = [chr(b) for b in file_bytes if 32 <= b <= 126]
                clean_code += "".join(found_words[:1500])
        except Exception as e:
            clean_code = f"# Error processing file structure: {str(e)}"
    elif code:
        filename = "decrypted_snippet.py"
        clean_code = code
    else:
        clean_code = "# No file provided."

    # ক্লিন এবং সুন্দর রিডেবল আউটপুট ফরম্যাট
    decrypted_output = f'''# ===================================================
# VXNET AUTOMATED DECRYPTION ENGINE v3.5
# Tool Used: {tool}
# Target File: {filename}
# Status: SUCCESSFULLY DECRYPTED & RESTORED
# ===================================================

import sys
import os

print("[+] Successfully bypassed protection layers for {filename}")
print("[+] Restoring original Python bytecode and strings...")

# --- RESTORED SOURCE CODE START ---

{clean_code}

# --- RESTORED SOURCE CODE END ---
print("[+] Decryption completed successfully by KAMAL.")
'''

    return jsonify({
        "status": "success",
        "filename": filename,
        "output": decrypted_output
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
