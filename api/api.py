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
import time
import openstack

app = Flask(__name__)

def token_valid(token):
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

        statement = "SELECT email, creation_time FROM authtoken WHERE token=%s"
        data = (token,)
        cursor.execute(statement, data)
        for (email, creation_time) in cursor:
            if (int(time.time()) - creation_time < 3600):
                if email is None:
                    connection.close()
                    return False
                else:
                    connection.close()
                    return email
            else:
                statement = "DELETE FROM authtoken WHERE email = %s"
                data = (email,)
                cursor.execute(statement, data)
                connection.commit()
                connection.close()
                return False

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
            statement = "INSERT INTO emailtoken (email, token, creation_time) VALUES (%s, %s, %s)"
            data = (email, token, int(time.time()))
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
        statement = "SELECT email, creation_time FROM emailtoken WHERE token=%s"
        data = (token,)
        cursor.execute(statement, data)
        for (email, creation_time) in cursor:
            if (int(time.time()) - creation_time < 86400):
                if email is None:
                    return None
                else:
                    return email
            else:
                statement = "DELETE FROM emailtoken WHERE email = %s"
                data = (email,)
                cursor.execute(statement, data)
                connection.commit()

                statement = "DELETE FROM auth WHERE email = %s"
                data = (email,)
                cursor.execute(statement, data)
                connection.commit()
                return -2

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
    if (email != None and email != -2):
        verified = update_data(email)
        returnvalue = {
          "verification": {
            "successful": verified
          }
        }
        connection.close()
        return returnvalue, 200
    elif email is None:
        returnvalue = {
          "verification": {
            "successful": verified,
            "error": "Token is invalid, please check the validity of your link!"
          }
        }
        connection.close()
        return returnvalue, 500
    elif email == -2:
        returnvalue = {
          "verification": {
            "successful": verified,
            "error": "Token is expired, please register again!"
          }
        }
        connection.close()
        return returnvalue, 500

@app.route('/api/login', methods=['POST'])
def login():
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

    def get_data(email):
        statement = "SELECT passwordhash FROM auth WHERE email=%s"
        data = (email,)
        cursor.execute(statement, data)
        for (passwordhash) in cursor:
            if passwordhash is None:
                return None
            else:
                return passwordhash

    passwordhash = get_data(record["auth"]["email"])

    if (record["auth"]["password"] == passwordhash[0]):
        # Generating a random token based on random string hash
        def random_string_generator(str_size, allowed_chars):
            return ''.join(random.choice(allowed_chars) for x in range(str_size))
        chars = string.ascii_letters + string.punctuation
        stringvar = random_string_generator(128, chars)
        token = hashlib.sha3_512(stringvar.encode("utf-8")).hexdigest()

        def add_data(email, token):
            def check_data(email):
                statement = "SELECT email, creation_time FROM authtoken WHERE email=%s"
                data = (email,)
                cursor.execute(statement, data)
                for (email, creation_time) in cursor:
                    statement = "DELETE FROM authtoken WHERE email = %s"
                    data = (email,)
                    cursor.execute(statement, data)
                    connection.commit()

            try:
                result = check_data(email)
                statement = "INSERT INTO authtoken (email, token, creation_time) VALUES (%s, %s, %s)"
                data = (email, token, int(time.time()))
                cursor.execute(statement, data)
                connection.commit()
                return 0
            except database.Error as err:
                return err

        dbstatus = add_data(record["auth"]["email"], token)

        if (dbstatus != 0):
            returnjson = {
            "verification": {
                "successful": "false",
                "error": "An unknown error ocurred!"
                }
            }
            return returnjson, 500

        # Returning the token
        else: 
            returnjson = {
            "verification": {
                "successful": "true",
                "token": token
                }
            }
            return returnjson
    
    else:
        returnjson = {
        "verification": {
            "successful": "false",
            "error": "E-Mail or Password wrong!"
          }
        }
        return returnjson, 500

@app.route('/api/verifylogin', methods=['POST'])
def verifylogin():
    record = json.loads(request.data)

    validation = token_valid(record["verify"]["token"])
    
    if (validation is not False):
        returnvalue = {
          "verification": {
            "successful": True
          }
        }
        return returnvalue, 200
    else:
        returnvalue = {
          "verification": {
            "successful": False,
            "error": "Token is invalid"
          }
        }
        return returnvalue, 500

@app.route('/api/createinstance', methods=['POST'])
def createinstance():
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
    
    validation = token_valid(record["verify"]["token"])

    if (validation is not False):
        email = validation

        def check_data(email):
            statement = "SELECT email, creation_time, instance_id, keypair_id, floating_ip_id FROM servers WHERE email=%s"
            data = (email,)
            cursor.execute(statement, data)
            for (email, creation_time, instance_id, keypair_id, floating_ip_id) in cursor:
                conn = openstack.connect(
                    cloud="otc"
                )
                server = conn.compute.find_server(instance_id)
                if server:
                    conn.compute.wait_for_server(server)
                    ip = conn.network.find_ip(name_or_id=floating_ip_id)
                    if ip:
                        conn.compute.remove_floating_ip_from_server(
                            server=instance_id,
                            address=ip.floating_ip_address
                        )
                        conn.network.delete_ip(ip)
                    conn.compute.delete_server(
                        server=instance_id
                    )

                statement = "DELETE FROM servers WHERE email = %s"
                data = (email,)
                cursor.execute(statement, data)
                connection.commit()

        def add_data(email):
            # Generating a random name based on random string hash to assign random names to Keypair and server
            def random_string_generator(str_size, allowed_chars):
                return ''.join(random.choice(allowed_chars) for x in range(str_size))
            chars = string.ascii_letters + string.punctuation
            stringvar = random_string_generator(128, chars)
            name = hashlib.md5(stringvar.encode("utf-8")).hexdigest()
            
            # Connect to OTC
            conn = openstack.connect(
                cloud="otc"
            )

            # Generate keypair and get flavor id and create floating ip
            keypair = conn.compute.create_keypair(name=name)
            flavor = conn.compute.find_flavor("s3.medium.1")
            floating_ip = conn.network.create_ip(name=name)

            # Check whether Server already exists and delete it
            check_data(email)

            # Create new Server
            instance = conn.compute.create_server(
                name=name,
                image_id="020c14d5-6529-47fc-af6d-e3e979dcc5f0",
                flavor_id=flavor.id,
                networks=[{"uuid": "f80955e7-bd2b-4ab5-ae83-ebf6d2c3804a"}],
                key_name=keypair.name
            )
            # Delete keypair immediatly as it is unecessary
            conn.compute.delete_keypair(keypair.id)

            # Update Database
            statement = "INSERT INTO servers (email, instance_id, creation_time, keypair_id, floating_ip_id) VALUES (%s, %s, %s, %s, %s)"
            data = (email, instance.id, int(time.time()), keypair.id, floating_ip.id)
            cursor.execute(statement, data)
            connection.commit()
            return {
                "instance_id": instance.id,
                "keypair_id": keypair.id,
                "keypair_key": keypair.private_key,
                "floating_ip": floating_ip.floating_ip_address
            }
        
        server = add_data(email)
        returnjson = {
            "private_key": server.keypair_key,
        }
        return returnjson, 200

    else:
        return "Autherr", 500
    
    