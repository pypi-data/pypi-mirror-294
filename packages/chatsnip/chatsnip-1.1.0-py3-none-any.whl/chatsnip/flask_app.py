from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
from chatsnip.extractor import extract_chat_from_json_stream  # Import from extractor.py
from chatsnip.file_splitter import split_and_save_chat  # Import from file_splitter.py

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

@app.route('/extract_chat', methods=['POST'])
def extract_chat():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Ensure that multi-word chat names are properly processed
        chat_name = request.form['chat_name'].strip('"')
        print(f"Extracting chat with name: {chat_name}")  # Debugging output
        extracted_text = extract_chat_from_json_stream(file_path, chat_name)
        
        if extracted_text:
            try:
                total_files_created = split_and_save_chat(extracted_text, output_dir=app.config['OUTPUT_FOLDER'], base_filename=chat_name)
                return f"Chat extracted and split into {total_files_created} files.", 200
            except Exception as e:
                print(f"Error during splitting chat: {e}")  # Debugging output
                return f"Error during splitting chat: {e}", 500
        else:
            return "Chat not found or content could not be extracted.", 400

if __name__ == "__main__":
    app.run(debug=True)