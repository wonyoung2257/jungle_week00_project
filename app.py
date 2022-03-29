
from unittest import result
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo import MongoClient
# client = MongoClient('localhost', 27017)
client = MongoClient('mongodb+srv://test:test@cluster0.b9rhp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.junglewordle
import random
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
  rank = sorted(userList, key=lambda user: (user['cnt_success']), reverse=True)
  rank_list = []
  for data in rank:
    rank_list.append({
      'id': data['id'],
      'cnt_success': data['cnt_success'],
      'cnt_fail': data['cnt_fail']
    })
  answers_list = list(db.answers.find({}))
  random_num = random.randrange(0,3)
  answers = {
    'name': answers_list[random_num]['name'],
    'answer': answers_list[random_num]['answer'],
    'img': answers_list[random_num]['img']
  }
  return render_template('main.html', ranking=rank_list, answers=answers)

@app.route('/success', methods=['POST'])
def add_count_success():
  id = request.form['id']
  new_cnt_success = int(db.users.find_one({'id': id})['cnt_success']) + 1
  new_cnt_fail = int(db.users.find_one({'id': id})['cnt_fail']) - 1
  db.users.update_one({'id': id}, {'$set': {'cnt_success': new_cnt_success}})
  db.users.update_one({'id': id}, {'$set': {'cnt_fail': new_cnt_fail}})

  return jsonify({'result': 'success'})

@app.route('/fail', methods=['POST'])
def add_count_fail():
  id = request.form['id']
  new_cnt_fail = int(db.users.find_one({'id': id})['cnt_fail']) + 1
  db.users.update_one({'id': id}, {'$set': {'cnt_fail': new_cnt_fail}})

  return jsonify({'result': 'success'})

if __name__ == '__main__':
  app.run('0.0.0.0', port=5000, debug =True)