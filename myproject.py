from flask import Flask,flash, redirect, url_for, request,render_template,redirect,session
import requests
from bs4 import BeautifulSoup
from models import db, User
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'afnlb113!sl'
db.init_app(app)
db.app = app

@app.route("/")
def home():
    session['logged_in'] = False
    return render_template('index.html')
@app.route("/garry")
def garry():
    garry_info_list = get_video("https://www.youtube.com/channel/UCRpdlPk671uOMiBtf5HtB3Q/videos?view=0&sort=p&shelf_id=2")
    return render_template('video.html',garry_info_list = garry_info_list)
def get_video(target_url):
    garry = requests.get(target_url)
    soup = BeautifulSoup(garry.text,'lxml')
    lis = soup.find_all('li',{'class': 'channels-content-item yt-shelf-grid-item'})
    garry_info_list = []
    for li in lis:
        title = li.find('a',{'title' : True})['title']
        if len(title)>46:
            short_title = ""
            for t in range(len(title)):
                if t >= 44:
                    break
                else:
                    short_title = short_title + title[t]
            title = short_title + "..."
        if len(title.encode()) < 66:
            title = title + "사랑해 개리형"
        video_link = 'http://www.youtube.com' + li.find('a',{'href' : True})['href']
        img_link = li.find('img', {'src' : True})['src']
        play_time = li.find('span',{'class' : 'video-time'}).text
        hits = li.find_all('li')[0].text
        updated_time = li.find_all('li')[1].text
        garry_video_info = {
                'title' : title,
                'video_link' : video_link,
                'img_link' : img_link,
                'play_time' : play_time,
                'hits' : hits,
                'updated_time' : updated_time
                }
        garry_info_list.append(garry_video_info)
    return garry_info_list
@app.route("/logging", methods = ['GET','POST'])
def logging():
    if request.method == 'GET':
        return render_template('logging.html')
    else:
        name = request.form['userid']
        passw = request.form['password']
        if len(name)>0 and len(passw) > 0:
            try:
                data = User.query.filter_by(userid = name).first()
                if data.check_password(passw):
                    session['logged_in'] = True
                    return redirect(url_for('test'))
                else:
                    return 'Dont login'
            except:
                return "except Dont login"
        else:
            return render_template('logging.html')
@app.route('/test',methods = ["GET","POST"])
def test():
    if session['logged_in']:
        if request.method == 'POST':
            session['logged_in'] = False
            return redirect(url_for('logging'))
        return render_template('test.html')
    else:
        return redirect(url_for('logging'))
@app.route('/register',methods = ["GET","POST"])
def register():
    if request.method == 'POST':
        uname = request.form['username']
        uid = request.form['userid']
        pword = request.form['password']
        el1 = request.form['email01']
        el2 = request.form['email02']
        if(len(uname)>0 and len(uid) > 0 and len(pword) > 0 and len(el1) > 0 and len(el2) > 0 ):
            new_user = User(username=uname,userid = uid,password = pword,email = el1 + el2)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('logging'))
        else:
            len_error = '빈칸을 채워주세요'
            return render_template('register.html',error = len_error)

    return render_template('register.html')
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
    if len(ret)>2:
        Points =ret[2].text.replace('\n','')
        Points = Points.replace('\t','')
        LeageName = ret[3].text.replace('\n','')
        LeageName = LeageName.replace('\t','')
    else:
        TierRank = "Unranked 1"
        Points = ""
        LeageName = "none"
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
