
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
# from bson.json_util import dumps
import json
from pymongo import MongoClient
# client = MongoClient('localhost', 27017)
import certifi
client = MongoClient('mongodb+srv://test:test@cluster0.b9rhp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority', tlsCAFile=certifi.where())
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

@app.route('/')
def home():
  userList = list(db.users.find({}))
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
  
  return render_template('main.html', ranking=rank_list, answers= json.dumps(answers, ensure_ascii=False))

@app.route('/success', methods=['POST'])
def add_count_success():
  id = request.form['id']
  new_cnt_success = int(db.users.find_one({'id': id})['cnt_success']) + 1
  db.users.update_one({'id': id}, {'$set': {'cnt_success': new_cnt_success}})

  return jsonify({'result': 'success'})

@app.route('/fail', methods=['POST'])
def add_count_fail():
  id = request.form['id']
  new_cnt_fail = int(db.users.find_one({'id': id})['cnt_fail']) + 1
  db.users.update_one({'id': id}, {'$set': {'cnt_fail': new_cnt_fail}})

  return jsonify({'result': 'success'})

@app.route('/makeid', methods=['POST'])
def post_memo():

    id_receive =request.form['id_give']  
    pw_receive = request.form['pw_give']  
    pw_receive2 = request.form['pw_give2'] 
    user = {'id': id_receive, 'pw': pw_receive, 'cnt_success':0, 'cnt_fail':0}
    userList = list(db.users.find({}))

    if id_receive == "":
        return jsonify({'result': 'false'}) 
    elif id_receive == "":
        return jsonify({'result': 'false'})

    elif pw_receive == "":
        return jsonify({'result': 'false2'})

    elif pw_receive == pw_receive2:
        db.users.insert_one(user)
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'false3'})
    

    # for i in userList :
  
    #     if id_receive == i['id']:
    #         return jsonify({'result': 'same'})
            
    #     elif id_receive == "":
    #         return jsonify({'result': 'false'})

    #     elif pw_receive == "":
    #         return jsonify({'result': 'false2'})
        
    #     elif pw_receive == pw_receive2:
    #         db.users.insert_one(user)
    #         return jsonify({'result': 'success'})

    #     else:
    #         return jsonify({'result': 'false3'})


if __name__ == '__main__':
  app.run('0.0.0.0', port=9432, debug =True)