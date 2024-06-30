from flask import Flask, request, jsonify
# local storage
import os
import json
import requests
from tools import *


app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json
    print('Received data:', data)
    # Process the data as needed
    setLocalData('title', data['title'])
    setLocalData('url', data['url'])
    # setLocalData('content', data['content'])

    return jsonify({'status': 'success'})

@app.route('/launch', methods=['POST'])
def launch():
    setLocalData('launch', 'true')
    return jsonify({'status': 'success'})
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)