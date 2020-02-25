from flask import Flask, redirect, url_for, request,render_template
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html') 
@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/check',methods = ['POST','GET'])
def check():
    value = request.form['test']
    url = 'https://www.op.gg/summoner/userName=' + value
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'lxml')
    rank = soup.find("div",class_="TierRankInfo")
    ret = []
    for tier in rank.find_all('div'):
        ret.append(tier)
    RankType = ret[0].text
    TierRank = ret[1].text
    Points =ret[2].text.replace('\n','')
    Points = Points.replace('\t','')
    LeageName = ret[3].text.replace('\n','')
    LeageName = LeageName.replace('\t','')
    TierRankInfo = {
            'RankType' : RankType,
            'TierRank' : TierRank,
            'Points' : Points,
            'LeageName' : LeageName
            }
    TierRankInfo_list= []
    TierRankInfo_list.append(TierRankInfo)
    Tier = TierRank.split(" ")
    return render_template('check.html',TierRankInfo_list = TierRankInfo_list,Tier = Tier) 
