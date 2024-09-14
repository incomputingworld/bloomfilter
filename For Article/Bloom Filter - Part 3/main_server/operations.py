import pymysql
import json
import random
import requests


def add_this_bf_to_sync_filter(bf, db, config):
    sql_statement = """INSERT INTO sync_filter (bloom_filter, entries, updated_by) values(%s, %s, %s)"""
    arr = str(bf.bloom_filter_array)
    arr = arr[(arr.find("'") + 1): -2]
    values_list = [arr, bf.entries_added, config['MAIN_SERVER_NAME']]

    try:
        with db.cursor() as cursor:
            cursor.execute(sql_statement, values_list)
    except pymysql.Error as e:
        error_code, message = e.args
        message = {'status': 'error', 'message': message}
        return message, error_code

    message = {'status': 'success', 'message': f"New row added to Sync filter"}
    json_message = json.dumps(message)
    return json_message, 200


async def check_bf_add_new_user(username, bf, nodes, config, db):
    # Check if any node is available or not.
    if len(nodes) == 0:
        message = {'status': 'error', 'message': f"Server is not available to take your request. Please try after "
                                                 f"some time."}
        json_message = json.dumps(message)
        return json_message, 503

    # checking local bloom filter
    exists = bf.data_exist(username)
    if exists:
        message = {'status': 'error', 'message': f"User name [{username}] already taken. Please select a new one"}
        json_message = json.dumps(message)
        return json_message, 409

    # Forward the request to one of the node server.
    node_index = random.randrange(0, len(nodes))
    node = nodes[node_index]
    endpoint = f"{node[1]}new_user/{username}"
    result = requests.post(url=endpoint)
    if result.status_code == 200:
        message = {'status': 'success', 'message': f"New user {username} created"}
        json_message = json.dumps(message)
        return json_message, 200
    return result.text, result.status_code


def periodic_update_to_sync_filter(bf, db, config):
    result = add_this_bf_to_sync_filter(bf, db, config)
    print(f"{config['MAIN_SERVER_NAME']} - Sycn filter updated")


def periodic_update_from_pending_users(bf, db, config):
    sql_statement = "SELECT id, username from pending_users where update_status = 'PENDING'"
    with db.cursor() as cursor:
        cursor.execute(sql_statement)
        rows = cursor.fetchall()

    if rows:
        ids = []
        for row in rows:
            ids.append(row['id'])
            bf.add_new_data(row['username'])

        sql_statement = "UPDATE pending_users SET update_status = 'COMPLETE' where ID in "
        params = f"({"%s," * len(ids)}"
        params = params[:-1]
        params += ")"
        sql_statement += params
        try:
            with db.cursor() as cursor:
                cursor.execute(sql_statement, ids)
        except pymysql.Error as e:
            error_code, message = e.args
            message = {'status': 'error', 'message': message}
            print(f"{config['MAIN_SERVER_NAME']} - Pending users issue - {message}, {error_code}")
        print(f"{config['MAIN_SERVER_NAME']} - Pending users updated ")
    print(f"{config['MAIN_SERVER_NAME']} - No Pending users to update ")