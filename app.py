from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from document_processor import extract_text_from_pdf
from search_engine import chunk_text, find_relevant_chunks
import requests

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'


N8N_WEBHOOK_URL = "http://localhost:5678/webhook/study-assistant"


@app.route('/process-document', methods=['POST'])
def process_document():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    query = request.form.get('query', '')

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # 1. Extract Text
        extracted_text = extract_text_from_pdf(file_path)

        # 2. Chunk and Search
        text_chunks = chunk_text(extracted_text)
        relevant_context = find_relevant_chunks(query, text_chunks)

        # 3. Prepare Payload for n8n
        payload = {
            "query": query,
            "context": relevant_context
        }

        # Sending to n8n (Currently wrapped in a try/except so the server doesn't crash before n8n is set up)
        try:
            n8n_response = requests.post(N8N_WEBHOOK_URL, json=payload)
            return jsonify({
                "status": "success",
                "extracted_context_length": len(relevant_context),
                "n8n_status": "sent"
            }), 200
        except requests.exceptions.RequestException as e:
            return jsonify({
                "status": "partial_success",
                "message": "Files processed, but n8n is not running yet.",
                "extracted_context_preview": relevant_context[:200] + "..."
            }), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
