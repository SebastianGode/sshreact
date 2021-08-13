import mysql.connector as database
import os
import json
import random
import string
import hashlib
import smtplib
import ssl
from flask import Flask, request, jsonify
from email.mime.text import MIMEText

app = Flask(__name__)


@app.route('/api/register', methods=['POST'])
def register():
    record = json.loads(request.data)
    dbpass = json.load(open('auth.json', 'r'))
    username = dbpass["username"]
    password = dbpass["password"]
    connection = database.connect(
        user=username,
        password=password,
        host="10.0.1.190",
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
        errorjson = {
          "error": {
            "errornumber": dbstatus.errno,
            "sqlstate": dbstatus.sqlstate,
            "message": dbstatus.msg
          }
        }
        return errorjson, 500
    else:
        return jsonify(record), 200

@app.route('/api/mail', methods=['POST'])
def mail():
    record = json.loads(request.data)

    # Generating a random token based on random string hash
    def random_string_generator(str_size, allowed_chars):
        return ''.join(random.choice(allowed_chars) for x in range(str_size))
    chars = string.ascii_letters + string.punctuation
    stringvar = random_string_generator(128, chars)
    token = hashlib.sha3_512(stringvar.encode("utf-8")).hexdigest()

    dbpass = json.load(open('auth.json', 'r'))
    username = dbpass["username"]
    password = dbpass["password"]
    # DB Connect
    connection = database.connect(
        user=username,
        password=password,
        host="10.0.1.190",
        database="auth"
    )
    cursor = connection.cursor()

    def add_data(email, token):
        try:
            statement = "INSERT INTO emailtoken (email, token) VALUES (%s, %s)"
            data = (email, token)
            cursor.execute(statement, data)
            connection.commit()
            return 0
        except database.Error as err:
            return err

    dbstatus = add_data(record["auth"]["email"], token)

    
    if (dbstatus != 0):
        errorjson = {
          "error": {
            "errornumber": dbstatus.errno,
            "sqlstate": dbstatus.sqlstate,
            "message": dbstatus.msg
          }
        }
        connection.close()
        return errorjson, 500
    else:
        connection.close()
        context = ssl.create_default_context()
        msg = MIMEText("Please verify your new Account using the following link: https://react.otc.ddnss.org/verify?token=" + token)
        msg['Subject'] = 'Verify your E-Mail address'
        msg['From'] = 'no-reply@ddnss.org'
        msg['To'] = record["auth"]["email"]

        def sendmail(msg, context, mailuser, mailpass, targetmail):
            try:
                server = smtplib.SMTP('login-cloud.mms.t-systems-service.com')
                server.set_debuglevel(1)
                server.starttls(context=context)
                server.login(mailuser,mailpass)
                server.sendmail("no-reply@ddnss.org", targetmail, msg.as_string())
                server.quit()
                return 0
            except Exception as err:
                return err
        
        mailstatus = sendmail(msg, context, dbpass["usernamemail"], dbpass["passwordmail"], record["auth"]["email"])
        if (mailstatus != 0):
            return "Error", 500
        else:
            return jsonify(record), 200

@app.route('/api/verify', methods=['POST'])
def verify():
    record = json.loads(request.data)
    dbpass = json.load(open('auth.json', 'r'))
    username = dbpass["username"]
    password = dbpass["password"]
    connection = database.connect(
        user=username,
        password=password,
        host="10.0.1.190",
        database="auth"
    )
    cursor = connection.cursor()

    def get_data(token):
        statement = "SELECT email FROM emailtoken WHERE token=%s"
        data = (token,)
        cursor.execute(statement, data)
        for (email) in cursor:
            return email

    email = get_data(record["verify"]["token"])
    

    def update_data(email):
        statement = "UPDATE auth SET verified = %s WHERE email = %s"
        data = (1, email)
        cursor.execute(statement, data)
        connection.commit()

        statement = "DELETE FROM emailtoken WHERE email = %s"
        data = (email,)
        cursor.execute(statement, data)
        connection.commit()
        return "true"
    
    verified = "false"
    if email != None:
        verified = update_data(email[0])
        returnvalue = {
          "verfication": {
            "successful": verified
          }
        }
        connection.close()
        return returnvalue, 200
    else:
        returnvalue = {
          "verfication": {
            "successful": verified
          }
        }
        connection.close()
        return returnvalue, 500
    