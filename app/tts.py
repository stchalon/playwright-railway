from flask import request, send_file, jsonify
from gtts import gTTS
import tempfile

def tts_handler():
    data = request.json
    text = data.get("text", "")
    lang = data.get("lang", "en")  # Default to English

    if not text:
        return jsonify({"error": "Missing 'text' field"}), 400

    try:
        tts = gTTS(text=text, lang=lang)

        # Save to a temp file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        temp_file.close()

        return send_file(temp_file.name, mimetype="audio/mpeg")

    except Exception as e:
        return jsonify({"error": str(e)}), 500
