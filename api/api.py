import mysql.connector as database
import os
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

    connection = database.connect(
        user=username,
        password=password,
        host="192.168.10.218",
        database="auth"
    )
    cursor = connection.cursor()

    def add_data(email, passwordhash):
        try:
            statement = "INSERT INTO auth (email, passwordhash, verified) VALUES (%s, %s, %s)"
            data = (email, passwordhash, 0)
            cursor.execute(statement, data)
            connection.commit()
            return 0
        except database.Error as err:
            return err

    dbstatus = add_data(record["auth"]["email"], record["auth"]["password"])

    connection.close()
    if (dbstatus != 0):
        return str(dbstatus.errno), 500
    else:
        return jsonify(record), 200