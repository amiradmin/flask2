# app.py - a minimal flask api using flask_restful
from flask import Flask,jsonify,request,url_for,redirect,session,render_template,g
import sqlite3

app = Flask(__name__)
app.config['Debug']=True
app.config['SECRET_KEY']='thisissecret'


def connect_db():
    sql = sqlite3.connect('/app/main')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g,'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'sqlite3'):
        g.sqlite_db.close_db

@app.route('/viewresult')
def viewresults():
    db = get_db()
    cur = db.execute('select * from users2')
    result = cur.fetchall()
    # print(result[0])
    return '<h1>Hello</h1>'.format(result[0]['id'])




@app.route('/')
def index():
    return '<h1>Hello World</h1>'

@app.route('/home/',methods=['GET'],defaults={'name':'defaults'})
@app.route('/home/<name>',methods=['GET'])
def home(name):
    db = get_db()
    cur =db.execute('select * from users')
    results = cur.fetchall()

    return render_template('home.html',name=name,mylist=['one','two','three','four'],results=results)


@app.route('/json')
def json():
    return jsonify({'name':'Amir','mylist':[1,2,3,4,5]})



@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return '<h1>hi {}. You are from {}. You are on the query page</h1>'.format(name,location)


@app.route('/theform')
def theform():
    return render_template('form.html')


@app.route('/process',methods=['POST'])
def process():
    name = request.form['name']
    location = request.form['location']
    return '<h1>hello {}. You are from {}.'.format(name,location)


@app.route('/processjson',methods=['GET'])
def processjson():
    data = request.get_json()
    name = data['name']
    location = data['location']
    randomlist = data['randomlist']
    return jsonify({'result':'succsess','name':name,'location':location,'randomlist':randomlist})

if __name__ == '__main__':
    app.run( host='0.0.0.0')
