"""
Web UI Integration for RASA Chatbot
Flask-based web interface to interact with the RASA bot.
"""
import requests
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500", "http://localhost:5500"])

# RASA server configuration
RASA_URL = "http://localhost:5005"
RASA_API_ENDPOINT = f"{RASA_URL}/webhooks/rest/webhook"


@app.route('/')
def index():
    """Render the chat interface."""
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    """
    Handle chat messages from the web UI.
    
    Expects JSON: {"message": "user message", "sender": "user_id"}
    Returns: {"recipient_id": "user_id", "text": "bot response"}
    """
    data = request.json
    user_message = data.get('message', '')
    sender_id = data.get('sender', 'web_user')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    try:
        # Send message to RASA
        payload = {
            "sender": sender_id,
            "message": user_message
        }
        
        response = requests.post(
            RASA_API_ENDPOINT,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            bot_responses = response.json()
            if bot_responses:
                return jsonify(bot_responses[0])
            return jsonify({"text": "I didn't get a response. Please try again."})
        else:
            return jsonify({"error": "RASA server error"}), 500
            
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Cannot connect to RASA server. Make sure it's running."}), 503
    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        # Check if RASA is running
        response = requests.get(f"{RASA_URL}/version", timeout=5)
        rasa_status = "online" if response.status_code == 200 else "offline"
    except:
        rasa_status = "offline"
    
    return jsonify({
        "status": "healthy",
        "rasa_server": rasa_status
    })


if __name__ == '__main__':
    print("=" * 50)
    print("Starting Web Chat Interface")
    print("=" * 50)
    print(f"RASA URL: {RASA_URL}")
    print(f"Web UI: http://localhost:5500")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5500, debug=True)
