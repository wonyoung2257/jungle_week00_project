
from datetime import timedelta
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_jwt_extended import *
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config.update(
  DEBUG = True,
  JWT_SECRET_KEY = 'SUPER KEY',
  JWT_TOKEN_LOCATION = 'cookies',
  JWT_ACCESS_TOKEN_RXPIRES = timedelta(hours = 1)
)
jwt = JWTManager(app)
# from bson.json_util import dumps
import json
from pymongo import MongoClient
# client = MongoClient('localhost', 27017)
import certifi
client = MongoClient('mongodb+srv://test:test@cluster0.b9rhp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority', tlsCAFile=certifi.where())
db = client.junglewordle
import random
# data = {
#   'name': '류석영',
#   'answer': 'ㅅㅓㄱㅇㅕㅇ',
#   'img': 'https://ca.slack-edge.com/T01FZU4LB4Y-U01GRGKDBFA-e83b97b839d9-512'}

# db.answers.insert_one(data)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/singup', methods = ['POST'])
def singup():
  if request.method =='POST':
    id = request.form.get('id')
    pw = request.form.get('pw')
    if(db.users.find_one({'id': id})): #아이디 이미 있을 때
      return jsonify({'result': 'exist', 'msg':'아이디가 이미 있음'})
    
    pw_hash = bcrypt.generate_password_hash(pw)
    doc = {'id': id, 'pwd': pw_hash}
    db.users.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '회원가입 되었습니다.'})
    
  else:
    return redirect(url_for('index'))

@app.route('/login', methods = ['POST'])
def login():
  userId = request.form.get('id')
  userPW = request.form.get('pwd')
  dbUser = db.users.find_one({'id': userId})
  checkPW = bcrypt.check_password_hash(dbUser['pwd'], userPW)
  
  if(not dbUser):
    return jsonify({'result': 'fail', 'msg': '존재하지 않는 아이디 입니다.'})
  if(not checkPW):
    return jsonify({{'result': 'fail', 'msg': '비밀번호가 일치하지 않습니다..'}})
  if(dbUser and checkPW):
    access_token = create_access_token(identity=userId , expires_delta=False)
    resp = jsonify({'login': True})
    set_access_cookies(resp, access_token)
    return resp, 200
  else:
    return jsonify(result = 'Fail')


@app.route('/main')
@jwt_required(optional=True)

def home():
  current_identity = get_jwt_identity()
  if current_identity :
    userList = list(db.users.find({'cnt_success': { '$exists': True}}))
    rank = sorted(userList, key=lambda user: (user['cnt_success']), reverse=True)
    rank_list = []
    for data in rank:
      cnt_fail = 0
      if ('cnt_fail' in data): cnt_fail = data['cnt_fail']
      rank_list.append({
        'id': data['id'],
        'cnt_success': data['cnt_success'],
        'cnt_fail': cnt_fail,
        'cnt_rate': round(data['cnt_success'] / (data['cnt_success'] + cnt_fail) * 100)
      })
    answers_list = list(db.answers.find({}))
    random_num = random.randrange(0,len(answers_list))
    answers = {
      'name': answers_list[random_num]['name'],
      'answer': answers_list[random_num]['answer'],
      'img': answers_list[random_num]['img']
    }
    
    return render_template('main.html', ranking=rank_list, answers= json.dumps(answers, ensure_ascii=False))
  else:
    return redirect(url_for('index'))

  

@app.route('/success', methods=['POST'])
def add_count_success():
  id = request.form['id']
  old_cnt_success = 0
  if ('cnt_success' in db.users.find_one({'id': id})): old_cnt_success = db.users.find_one({'id': id})['cnt_success']
  new_cnt_success = old_cnt_success + 1
  db.users.update_one({'id': id}, {'$set': {'cnt_success': new_cnt_success}})

  return jsonify({'result': 'success'})

@app.route('/fail', methods=['POST'])
def add_count_fail():
  id = request.form['id']
  old_cnt_fail = 0
  if ('cnt_fail' in db.users.find_one({'id': id})): old_cnt_fail = db.users.find_one({'id': id})['cnt_fail']
  new_cnt_fail = old_cnt_fail + 1
  db.users.update_one({'id': id}, {'$set': {'cnt_fail': new_cnt_fail}})

  return jsonify({'result': 'success'})




if __name__ == '__main__':
  app.run('0.0.0.0', port=9432, debug =True)