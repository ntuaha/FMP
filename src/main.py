import requests

from flask import Flask,g
from flask import request as req
from flask import jsonify # 提供json 回應的方法

from pg import DB
import os

PG_INFO = {}
PG_INFO["user"] = os.environ.get('AHA_PG_USER')
PG_INFO["passowrd"] = os.environ.get('AHA_PG_PWD') 
PG_INFO["ip"] = os.environ.get('AHA_PG_IP') 
PG_INFO["port"] = os.environ.get('AHA_PG_PORT')  

app = Flask(__name__)

def get_db():
  db = getattr(g, '_database', None)
  if db is None:
    db = DB(dbname='esb', host=PG_INFO["ip"], port=int(PG_INFO["port"]),user=PG_INFO["user"], passwd=PG_INFO["passowrd"])
    print("db runining...")
  return db

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
      db.close()


@app.route("/")
def hello():
    return "Hello World!"

#取得目前所有使用者名單
@app.route('/user/list',methods=['GET'])
def list():
  db = get_db()
  q = db.query("select * from fb_users").dictresult()
  data = {}
  data["count"] = len(q)
  data["data"] = q
  return jsonify(data)

@app.route('/user/fbm/<fbmid>', methods=['GET'])
def fbm_user(fbmid):
  db = get_db()
  q = db.query("select * from fb_users where fbmid = '%s'"%fbmid).dictresult()
  return jsonify(q)
    

@app.route('/user/fbm',methods=['POST'])
def fbm_user_insert():
  data = req.get_json()
  print(data)
  db = get_db()
  q = db.query("select uid from fb_users where fbmid = '%s'"%data['fbmid']).dictresult()
  if len(q) == 0 :    
    return jsonify(db.insert('fb_users',data))
  elif len(q) == 1 :
    data["uid"] = q[0]["uid"]
    return jsonify(db.update('fb_users',data))
    





if __name__ == "__main__":
    app.run(debug=True)