from pg import DB
import datetime
from urllib.parse import quote
import requests
import json

class NEWS:
  def __init__(self,db):
    self.channel = "fbm"
    self.db = db

  def getNewsUrl(self,fbmid):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    return "http://52.42.108.66:5000/api/v1/list?startdate=%s&enddate=%s&type=json&channel=%s&id=%s"%(yesterday,today,self.channel,fbmid)

  def getRedirectNewsLink(self,fbmid,original_link,news_no):
    return "http://ntuaha.github.io/AI_SCRIPT/line.html?target="+quote(original_link)+"&info="+quote("http://52.42.108.66:5000/api/v1/contexts?no="+news_no+"&id="+fbmid+"&type=json&channel="+self.channel)
  
  def getNews(self):
    return requests.get(self.getNewsUrl('1234567')).json()
  

  def getFBMmsg(self,fbmid,data):
    msg = {}
    msg['recipient'] = {"id":fbmid}
    msg["message"] = {"attachment":{"type":"template","payload":{"template_type":"generic","elements":[]}}}
    for news in data["news"]:
      if "img" not in news:
        news["img"] = "https://upload.wikimedia.org/wikipedia/commons/6/65/%E5%B7%A5%E5%95%86%E6%99%82%E5%A0%B1LOGO.jpg"
      msg_ele = {}
      msg_ele = {"title":news["title"],"item_url":self.getRedirectNewsLink(fbmid,news["link"],news["no"]),"image_url":news["img"]}
      msg_ele["subtitle"] = "來源:%s, 點擊數:%d, 時間:%s"%(news["source"],news["hits"],news["dt"].split(".")[0].replace("T"," ")) 
      msg["message"]["attachment"]["payload"]["elements"].append(msg_ele)      
    return msg


  def sendNews(self,token,fbmids):  
    news = self.getNews()
    fb_api_url = "https://graph.facebook.com/v2.6/me/messages?access_token=%s"%token
    for fbmid in fbmids:        
      r = requests.post(fb_api_url,json=self.getFBMmsg(fbmid,news))


if __name__ == "__main__":
  import os
  token = os.environ.get('AHA_FB_PAGE_ACCESS_TOKEN')
  PG_INFO = {}
  PG_INFO["user"] = os.environ.get('AHA_PG_USER')
  PG_INFO["passowrd"] = os.environ.get('AHA_PG_PWD') 
  PG_INFO["ip"] = os.environ.get('AHA_PG_IP')
  PG_INFO["port"] = os.environ.get('AHA_PG_PORT')
  db = DB(dbname='esb', host=PG_INFO["ip"], port=int(PG_INFO["port"]),user=PG_INFO["user"], passwd=PG_INFO["passowrd"])
  news = NEWS(db)  
  q = db.query("select fbmid from fb_users where pushnewsflag = true").dictresult()
  fbmids = [d["fbmid"] for d in q]
  news.sendNews(token,fbmids)
  db.close()

    


    
  
