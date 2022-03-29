
from unittest import result
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbexam

@app.route('/')
def home():
  return render_template('main.html')

if __name__ == '__main__':
  app.run('0.0.0.0', port=5000, debug =True)