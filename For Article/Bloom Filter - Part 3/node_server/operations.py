import pymysql
from bitarray import bitarray
from flask import json
import requests


def register_with_main_server(config):  # Yet to test
    endpoint = config['MAIN_SERVER'] + 'register_node'
    node_data = {"NODE_NAME": config['NODE_NAME'], "NODE_URL": config['NODE_URL']}
    json_node_data = json.dumps(node_data)
    result = requests.post(url=endpoint, json=node_data)
    print(f"{config['NODE_NAME']} - Registered with main server")


def initialize_local_bloom_filter_from_database(db, local_bf, config):
    sql_statement = "SELECT * FROM sync_filter ORDER BY ID DESC LIMIT 1;"
    with db.cursor() as cursor:
        cursor.execute(sql_statement)
        result = cursor.fetchone()

    calibrate_bloom_filter(result, local_bf)

    result = update_sync_filter(result['id'], result['updated_by'], db, config)
    print(f"{config['NODE_NAME']} - Initialized local bloom filter from DB")


def check_bf_add_user_update_pending_users(username, bf, config, db):
    # checking local bloom filter
    exists = bf.data_exist(username)
    if exists:
        message = {'status': 'error', 'message': f"User name [{username}] already taken. Please select a new one"}
        json_message = json.dumps(message)
        return json_message, 409

    # adding a new user
    result = add_new_user(username, config, db)
    bf.add_new_data(username)

    indices = bf.get_bit_array_indices(username)  # Might not need this.

    # updating pending users table
    if result[1] == 200:  # User added successfully
        return update_pending_users(username, config, db)
    return result


def add_new_user(username, config, db):
    sql_statement = """INSERT INTO users(username, created_by) VALUES(%s, %s)"""
    values_list = [username, config['NODE_NAME']]

    try:
        with db.cursor() as cursor:
            cursor.execute(sql_statement, values_list)

    except pymysql.IntegrityError as e:
        error_code, message = e.args
        if error_code == 1062:  # Duplicate entry. MySQL Error code
            message = {'status': 'error',
                       'message': f"User name [{username}] already taken. Please select a new one"}
        else:
            message = {'status': 'error',
                       'message': f"Some error has occurred while adding [{username}]"}

        json_message = json.dumps(message)
        return json_message, 409

    message = {'status': 'success', 'message': f"New user {username} created"}
    json_message = json.dumps(message)
    return json_message, 200


def update_pending_users(username, config, db):
    sql_statement = """INSERT INTO pending_users (username, updated_by) VALUES(%s, %s)"""
    values_list = [username, config['NODE_NAME']]
    try:
        with db.cursor() as cursor:
            cursor.execute(sql_statement, values_list)

    except pymysql.IntegrityError as e:
        error_code, message = e.args
        if error_code == 1062:  # Duplicate entry. MySQL Error code
            message = {'status': 'error', 'message': f"User name [{username}] already exist in Pending Users."}
        else:
            message = {'status': 'error', 'message': f"Error occurred while updating Pending Users with [{username}]"}

        json_message = json.dumps(message)
        return json_message, 409

    message = {'status': 'success', 'message': f"Pending Users updated with {username}"}
    json_message = json.dumps(message)
    return json_message, 200


def update_local_bf_with_main_server_bf(bf, config, db):
    sql_statement = ("SELECT * FROM sync_filter WHERE \n"
                     "updated_by NOT LIKE(%s) and \n"
                     "id = (select MAX(id) FROM sync_filter) ORDER BY ID DESC LIMIT 1")
    value = f"%{config["NODE_NAME"]}%"
    values_list = [value]
    with db.cursor() as cursor:
        cursor.execute(sql_statement, values_list)
        result = cursor.fetchone()

    if result:
        calibrate_bloom_filter(result, bf)

        result = update_sync_filter(result['id'], result['updated_by'], db, config)
        print(f"{config['NODE_NAME']} - Updated local bloom filter from main server")


def update_sync_filter(id, updated_by, db, config):
    sql_statement = """UPDATE sync_filter SET updated_by = %s WHERE id = %s"""
    if len(updated_by):
        updated = f"{updated_by}, {config['NODE_NAME']}"
    else:
        updated = f"{config['NODE_NAME']}"
    values_list = [updated, id]

    try:
        with db.cursor() as cursor:
            cursor.execute(sql_statement, values_list)

    except pymysql.IntegrityError as e:
        error_code, message = e.args
        if error_code == 1062:  # Duplicate entry. MySQL Error code
            message = {'status': 'error', 'message': message}
            json_message = json.dumps(message)
            return json_message, error_code

    message = {'status': 'success', 'message': f"Main server Bloom filter in sync for {config['NODE_NAME']}"}
    json_message = json.dumps(message)
    return json_message, 200


def calibrate_bloom_filter(result, bf):
    arr = str(result['bloom_filter'])
    arr = arr[(arr.find("'") + 1): -1]
    bits_arr = bitarray(arr)
    bf.bloom_filter_array |= bits_arr
    bf.entries_added = result['entries']
