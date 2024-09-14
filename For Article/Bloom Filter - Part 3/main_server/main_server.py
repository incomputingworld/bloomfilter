import os
import sys
import json
from flask import Flask, request
from flask_apscheduler import APScheduler
import pymysql

app = Flask(__name__)

base_dir = os.path.abspath(".")
bf_path = os.path.join(base_dir, "bf")
sys.path.append(bf_path)

parent_dir = os.path.abspath("..")
schema_path = os.path.join(parent_dir, 'database')

bf_config_file = os.path.join(base_dir, 'config.py')

app.config['DEBUG'] = False
app.config['ENV'] = 'development'
app.config['SCHEMA'] = schema_path
app.config['FLASK_ENV'] = 'development'
app.config['SECRET_KEY'] = 'ItShouldBeALongStringOfRandomCharacters'
app.config['MAIN_SERVER'] = 'http://127.0.0.1:5000/'
app.config['MAIN_SERVER_NAME'] = 'main_server'
app.config.from_pyfile(bf_config_file)

# DB connection
db = pymysql.connect(host="localhost", user='root', password='acer@411028!',
                     database="dist_bf", cursorclass=pymysql.cursors.DictCursor, autocommit=True)

# Scheduler initialization
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

from bf.bloom_filter import BloomFilter

# Initializing bloom filter
centralized_bloom_filter = BloomFilter(app.config['EXPECTED_ENTRIES'], app.config['ERROR_RATE'])
centralized_bloom_filter.load_all_data()

from operations import (add_this_bf_to_sync_filter, check_bf_add_new_user,
                        periodic_update_to_sync_filter, periodic_update_from_pending_users)

registered_nodes = {}
node_count = 0

result = add_this_bf_to_sync_filter(centralized_bloom_filter, db, app.config)
if result[1] != 200:
    print(result)


# scheduling task
@scheduler.task('interval', id='update_pending_users_and_sync', seconds=app.config['UPDATE_FREQ'])
def update_from_pending_users():
    periodic_update_from_pending_users(centralized_bloom_filter, db, app.config)
    periodic_update_to_sync_filter(centralized_bloom_filter, db, app.config)


@scheduler.task('interval', id='show_stats', seconds=5)
def show_status():
    message = f"Main Server - {app.config['MAIN_SERVER_NAME']}\n{str(centralized_bloom_filter)}"
    print(message)


@app.route("/")
def start_app():
    message = (f"<p> Main Server - {app.config['MAIN_SERVER_NAME']} is up and running <br>"
               f"{str(centralized_bloom_filter)} <br>"
               f"{centralized_bloom_filter.bloom_filter_array}</p>")
    return message


@app.route("/register_node", methods=['POST'])
def register_node_server():
    global node_count
    json_data = request.get_json()
    # registered_nodes[json_data["NODE_NAME"]] = json_data["NODE_URL"]
    registered_nodes[node_count] = [json_data["NODE_NAME"], json_data["NODE_URL"]]
    node_count += 1
    message = {'status': 'success', 'message': f"New Node registered."}
    json_message = json.dumps(message)
    return json_message, 200


@app.route("/new_user/<username>", methods=["POST"])
async def new_user(username):
    res = await check_bf_add_new_user(username, centralized_bloom_filter, registered_nodes, app.config, db)
    return res


if __name__ == "__main__":
    app.run(debug=False)
