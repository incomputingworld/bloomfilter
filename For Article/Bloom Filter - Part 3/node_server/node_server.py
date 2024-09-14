import os
import sys
from flask import Flask
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
app.config.from_pyfile(bf_config_file)

db = pymysql.connect(host="localhost", user='root', password='acer@411028!',
                     database="dist_bf", cursorclass=pymysql.cursors.DictCursor, autocommit=True)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

from bf.bloom_filter import BloomFilter

local_bloom_filter = BloomFilter(app.config['EXPECTED_ENTRIES'], app.config['ERROR_RATE'])

from operations import (initialize_local_bloom_filter_from_database,
                        register_with_main_server,
                        check_bf_add_user_update_pending_users, add_new_user,
                        update_local_bf_with_main_server_bf)

register_with_main_server(app.config)

initialize_local_bloom_filter_from_database(db, local_bloom_filter, app.config)


@scheduler.task('interval', id='update_bf', seconds=app.config['SYNC_FILTER_FREQ'])
def update_local_bloom_filter():
    update_local_bf_with_main_server_bf(local_bloom_filter, app.config, db)


@scheduler.task('interval', id='show_stats', seconds=5)
def show_stats():
    message = f"Node Server - {app.config['NODE_NAME']}\n {str(local_bloom_filter)}"
    print(message)


@app.route("/")
def start_app():
    message = (f"<p>Node Server - {app.config['NODE_NAME']} is up and running <br>"
               f"{str(local_bloom_filter)} <br>"
               f"{local_bloom_filter.bloom_filter_array}</p>")
    return message


@app.route("/new_user/<username>", methods=["POST"])
def new_user(username):
    return check_bf_add_user_update_pending_users(username, local_bloom_filter, app.config, db)


#
@app.route("/test_add_new_user/<username>")
def test_add_new_user(username):
    return add_new_user(username, app.config, db)


if __name__ == "main":
    app.run(debug=False)
