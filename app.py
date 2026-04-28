from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()

app = Flask(__name__)

# Load OpenAI API key from environment
# client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# In-memory storage for events (in production, use a database)
events = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/events', methods=['GET', 'POST'])
def handle_events():
    if request.method == 'POST':
        data = request.json
        event = {
            'id': len(events) + 1,
            'name': data['name'],
            'targetDateTime': data['targetDateTime'],
            'notes': data.get('notes', ''),
            'totalDuration': calculate_total_duration(data['targetDateTime'])
        }
        events.append(event)
        return jsonify(event), 201
    else:
        return jsonify(events)

@app.route('/api/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    global events
    events = [e for e in events if e['id'] != event_id]
    return '', 204

@app.route('/api/ai/suggest', methods=['POST'])
def ai_suggest():
    # data = request.json
    # prompt = f"Suggest a futuristic event name and description for: {data.get('theme', 'general')}"
    
    # try:
    #     response = client.chat.completions.create(
    #         model="gpt-3.5-turbo",
    #         messages=[{"role": "user", "content": prompt}],
    #         max_tokens=100
    #     )
    #     suggestion = response.choices[0].message.content.strip()
    #     return jsonify({'suggestion': suggestion})
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500
    return jsonify({'suggestion': 'AI not configured'})

def calculate_total_duration(target_datetime_str):
    target = datetime.fromisoformat(target_datetime_str.replace('Z', '+00:00'))
    now = datetime.now(target.tzinfo)
    return int((target - now).total_seconds())

if __name__ == '__main__':
    app.run(debug=False)