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

@app.route('/msg/fbm/list', methods=['GET'])
def fbm_msg():
  db = get_db()
  q = db.query("select * from fbm_txn order by createdtime desc limit 10").dictresult()
  return jsonify({"count":len(q),"data":q})

@app.route('/msg/fbm', methods=['POST'])
def fbm_msg_insert():
  db = get_db()
  print (req.get_json())
  return jsonify(db.insert('fbm_txn',req.get_json()))




@app.route('/user/fbm/<fbmid>', methods=['GET','POST'])
def fbm_user(fbmid):
  db = get_db()
  q = db.query("select * from fb_users where fbmid = '%s'"%fbmid).dictresult()
  if req.method == "GET":
    return jsonify(q)
  elif req.method == "POST":    
    data = req.get_json()    
    try:
      data['fbmid'] = fbmid
    except KeyError:
      return jsonify([])
    if len(q) == 0 :
      r = getFBMUserInfo(fbmid)
      data['fbmimgurl'] = r['profile_pic']
      data['gender'] = r['gender'].strip()
      data['fbname'] = "%s %s"%(r['last_name'],r['first_name'])
    
      return jsonify(db.insert('fb_users',data))
    elif len(q) == 1 :
      data["uid"] = q[0]["uid"]
      return jsonify(db.update('fb_users',data))
  # 如果都沒有輸出的話      
  return jsonify([])
    

def getFBMUserInfo(user_id):
  token = os.environ.get('AHA_FB_PAGE_ACCESS_TOKEN')
  href =  "https://graph.facebook.com/v2.6/%s?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=%s"%(user_id,token)
  r = requests.get(href).json()
  return r


if __name__ == "__main__":
  app.run(debug=True)