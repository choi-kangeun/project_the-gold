from pickletools import read_uint1
from flask import Flask, render_template, request, session, flash
import mod_dbconn
import pickle
import joblib
import json

app = Flask(__name__)
app.secret_key = 'secretkey'

@app.route('/')
def home():
    if session:
        return render_template('loginhome.html')
    
    return render_template('home.html')   

@app.route('/insert')
def insert_info():
    return render_template('insert.html')

@app.route('/login')
def login():
   return render_template('login.html')

@app.route('/db/check', methods=['GET'])
def check():
    if request.method == 'GET':
        print(request.args.get('startDate'))
        startDate = request.args.get('startDate')
        endDate = request.args.get('endDate')
        db_class = mod_dbconn.Database()
        sql = f"SELECT * FROM test.gold WHERE Date BETWEEN '{startDate}%%' AND '{endDate}%%'"
        row = db_class.executeAll(sql)
        
        data_list = []
        
        data_list.append(['Years', 'Sales'])
    
        
        for col in row:
            month = str(col['Date'].month)
            day = str(col['Date'].day)
            data_temp = []
            data_temp.append(year + month + day)
            data_temp.append(col['gold_price'])
            data_list.append(data_temp)
        
        print(data_list)
        jsonString = json.dumps(data_list)
    
    return render_template('check.html', data_list=jsonString) 

@app.route('/layout')
def layout():
   return render_template('layout.html') 


@app.route('/db/click')
def click():
   return render_template('click.html') 

# 여기부터 추가
@app.route('/db')
def select():
    db_class = mod_dbconn.Database()

    sql = "SELECT * FROM test.test_tb"
    row = db_class.executeAll(sql)

    print(row)

    return render_template('db.html', resultData=row[0])


@app.route('/db/insert', methods=['GET', 'POST'])
def insert():
    db_class = mod_dbconn.Database()
    
    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['pw']
        name = request.form['name']
        nick = request.form['nick']
        sql= "INSERT INTO test.test_tb VALUES('{}','{}','{}','{}')".format(id, pw, name, nick)


        print(id)

        db_class.execute(sql)
        db_class.commit()
        
        if not(id and pw and name and nick):
            flash("입력되지 않은 정보가 있습니다.")
            return render_template('insert.html')
   
        else:       
            return render_template('inserthome.html')
            
            

@app.route('/db/login', methods=['GET', 'POST'])
def update():
    db_class = mod_dbconn.Database()

    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['pw']

        sql = "SELECT * FROM test.test_tb WHERE id = '{}' AND pw = '{}'".format(id, pw)
        
        row = db_class.executeAll(sql)        
        
        print(row)
        
        if id == "":
            flash("Please Input ID")
            return render_template("login.html")
        
        elif pw =="":
            flash("Please Input PW")
            return render_template("login.html")
        
        elif row[0]['id']:
            session['loginsuccess'] = True
            session['username'] = id
            return render_template('loginhome.html')     
        
@app.route("/logout")
def logout():
    session.pop('loginsuccess', None)
    session.pop('username', None)
    return render_template('logout.html')

@app.route('/predict')
def predict():
    model = joblib.load("lr_model.pkl")
    
    predict_value = model.predict([[25.56,1707.99,28.71,20.352,114.34,11028.74,30779.71,3785.38,3.01]])
    print(predict_value)
    
    return render_template('home.html', predict_value=predict_value)

    # if request.method == "POST":
    #     date = request.form['date']
        
    #     sql = "SELECT * FROM test.gold WHERE Date = '{}'".format(date)
        
    #     row = db_class.executeAll(sql) 


# 여기까지 추가


if __name__=='__main__':
    app.run(debug=True)
