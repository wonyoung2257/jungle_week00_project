
from unittest import result
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo import MongoClient
# client = MongoClient('localhost', 27017)
client = MongoClient('mongodb+srv://test:test@cluster0.b9rhp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.junglewordle
# data = {
#   'name': '허원영',
#   'answer': 'ㅇㅜㅓㄴㅇㅕㅇ',
#   'img': 'https://ca.slack-edge.com/T01FZU4LB4Y-U038VG9V6M9-2ec7f2a14209-512'}
# data = {
#   'id': '아이유',
#   'pwd': '1234',
#   'cnt_success': '8',
#   'cnt_fail': '5'
# }
# db.users.insert_one(data)
userList = list(db.users.find({}))

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/rank', methods=['GET'])
def rank_list():
  rank = sorted(userList, key=lambda user: (user['cnt_success']), reverse=True)
  rank_list = []
  for data in rank:
    rank_list.append({
      'id': data['id'],
      'cntSuccess': data['cnt_success'],
      'failSuccess': data['cnt_fail']
    })

  return jsonify({'result': 'success', 'rank_list': rank_list})

if __name__ == '__main__':
  app.run('0.0.0.0', port=5000, debug =True)