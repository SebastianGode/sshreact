import time
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/api/register', methods=['POST'])
def register():
    record = json.loads(request.data)
    with open('data.txt', 'a') as f:
        f.write(record["auth"]["password"] + " " + record["auth"]["email"] + "\n")
    return jsonify(record)