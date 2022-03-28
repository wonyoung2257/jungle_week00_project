
from unittest import result
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo import MongoClient
# client = MongoClient('mongodb://won:ekdms198@3.38.247.48', 27017)
client = MongoClient('localhost', 27017)
db = client.dbexam

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/memo', methods = ['GET'])
def listing():
  result = list(db.memos.find())
  print(dumps(result))

  return jsonify({'result':'success', 'memos': dumps(result)})

@app.route('/memo', methods = ['POST'])
def save():
  title = request.form.get('title')
  content = request.form.get('content')
  print('title1'+ title)
  doc = {
    'title' : title,
    'content' : content
  }
  print(doc)
  db.memos.insert_one(doc)

  return jsonify({'result':'success'})

@app.route('/card', methods= ['DELETE'])
def delete():
  id = request.form.get('id')
  db.memos.delete_one({'_id':ObjectId(id)})
  return jsonify({'result': 'success'})

@app.route('/card', methods= ['POST'])
def update():
  

  id = request.form.get('id')
  title = request.form.get('title')
  text = request.form.get('text')
  dbMemo = db.memos.find_one({'_id':ObjectId(id)})
  print(dbMemo['title'])
  if dbMemo['title'] != title:
    db.memos.update_one({'_id':ObjectId(id)},{'$set':{'title':title}})  
  if dbMemo['content'] != text:
    db.memos.update_one({'_id':ObjectId(id)},{'$set':{'content': text}})
  
  return jsonify({'result': 'success'})

if __name__ == '__main__':
  app.run('0.0.0.0', port=5000, debug =True)