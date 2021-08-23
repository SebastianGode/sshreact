import mysql.connector as database
import os
import time
import openstack
import json

dbpass = json.load(open('api/auth.json', 'r'))
username = dbpass["username"]
password = dbpass["password"]
# DB Connect
connection = database.connect(
    user=username,
    password=password,
    host="10.0.1.190",
    database="auth"
)
cursor = connection.cursor(buffered=True)

conn = openstack.connect(
    cloud="otc"
)

def servers():
    statement = "SELECT creation_time, instance_id, floating_ip_id, email FROM servers"
    cursor.execute(statement)
    for (creation_time, instance_id, floating_ip_id, email) in cursor:
        if (int(time.time()) - int(creation_time) > 1800):
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
            dbpass = json.load(open('api/auth.json', 'r'))
            username = dbpass["username"]
            password = dbpass["password"]
            connection2 = database.connect(
                user=username,
                password=password,
                host="10.0.1.190",
                database="auth"
            )
            cursor2 = connection2.cursor(buffered=True)
            statement = "DELETE FROM servers WHERE email = %s"
            data = (email,)
            cursor2.execute(statement, data)
            connection2.commit()
            connection2.close()


def emailtoken():
    statement = "SELECT email, creation_time FROM emailtoken"
    cursor.execute(statement)
    for (email, creation_time) in cursor:
        if (int(time.time()) - int(creation_time) > 86400):
            dbpass = json.load(open('api/auth.json', 'r'))
            username = dbpass["username"]
            password = dbpass["password"]
            connection2 = database.connect(
                user=username,
                password=password,
                host="10.0.1.190",
                database="auth"
            )
            cursor2 = connection2.cursor(buffered=True)
            statement = "DELETE FROM emailtoken WHERE email = %s"
            data = (email,)
            cursor2.execute(statement, data)
            connection2.commit()
            connection2.close()


def authtoken():
    statement = "SELECT email, creation_time FROM authtoken"
    cursor.execute(statement)
    for (email, creation_time) in cursor:
        if (int(time.time()) - int(creation_time) > 3600):
            dbpass = json.load(open('api/auth.json', 'r'))
            username = dbpass["username"]
            password = dbpass["password"]
            connection2 = database.connect(
                user=username,
                password=password,
                host="10.0.1.190",
                database="auth"
            )
            cursor2 = connection2.cursor(buffered=True)
            statement = "DELETE FROM authtoken WHERE email = %s"
            data = (email,)
            cursor2.execute(statement, data)
            connection2.commit()
            connection2.close()

def auth():
    statement = "SELECT email, creation_time FROM auth"
    cursor.execute(statement)
    for row in cursor:
        if (int(time.time()) - int(row[1]) > 604800):
            dbpass = json.load(open('api/auth.json', 'r'))
            username = dbpass["username"]
            password = dbpass["password"]
            connection2 = database.connect(
                user=username,
                password=password,
                host="10.0.1.190",
                database="auth"
            )
            cursor2 = connection2.cursor(buffered=True)
            statement = "DELETE FROM auth WHERE email = %s"
            data = (row[0],)
            cursor2.execute(statement, data)
            connection2.commit()
            connection2.close()


servers()
emailtoken()
authtoken()
auth()
