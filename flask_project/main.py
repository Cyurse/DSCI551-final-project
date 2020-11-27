from flask import Flask, render_template, request
import requests
from data_processor import process_data
import json

app = Flask(__name__)


@app.route('/')
def initial():
    # return r.text
    return app.send_static_file("search.html")

@app.route('/second', methods=['GET'])
def get_value():
    x = 0
    keywords = request.args.get('keywords')
    sort_order = request.args.get('sortby')
    print(keywords)
    print(sort_order)
    r = process_data(keywords, sort_order)
    temp = json.loads(r)
    print(temp[0])
    return r

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
