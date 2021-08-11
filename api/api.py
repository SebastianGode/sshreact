import mysql.connector as database
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/register', methods=['POST'])
def register():
    record = json.loads(request.data)
    # with open('data.txt', 'a') as f:
    #     f.write(record["auth"]["password"] + " " + record["auth"]["email"] + "\n")
    dbpass = json.load(open('auth.json', 'r'))
    username = dbpass["username"]
    password = dbpass["password"]

    return jsonify(record)