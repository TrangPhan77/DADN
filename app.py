from __future__ import division
from flask import Flask, jsonify, render_template, redirect, url_for, make_response, session
from flask_cors import CORS
from flask import g
from flask import Response
from flask import request
from flask_mysqldb import MySQL
import json
import MySQLdb
import math
import MySQLdb.cursors
import re  
import time


app = Flask(__name__)
CORS(app)
app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123123123'
app.config['MYSQL_DB'] = 'sfarm'
mysql = MySQL(app)
    

@app.route('/', methods =['GET', 'POST'])
def login():
    mesage=""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE UserName = % s AND PassWord = % s', (username, password, ))
        user = cursor.fetchone()
        if user:            
            session['loggedin'] = True
            session['userid'] = user['U_ID']
            session['UserName'] = user['UserName']
            return redirect(url_for('home'))
        else:
            mesage = 'Tên đăng nhập hoặc mật khẩu không chính xác !'
    return render_template('login.html', mesage = mesage)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        return render_template("profile.html")
    return redirect(url_for('login'))

@app.route('/control_pump')
def control_pump():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM `area`')
        area = cursor.fetchall()  
        return render_template("control-pump.html", area=area)
    return redirect(url_for('login'))

@app.route('/period')
def period():
    if 'loggedin' in session:
        return render_template("period-watering.html")
    return redirect(url_for('login'))

@app.route('/statis')
def statis():
    if 'loggedin' in session:
        return render_template("statistic.html")
    return redirect(url_for('login'))

@app.route('/auto')
def auto():
    if 'loggedin' in session:
        return render_template("auto-watering.html")
    return redirect(url_for('login'))

@app.route('/period_response_schedual', methods= ['POST', 'GET'])
def period_response_schedual():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql1 = 'SELECT * FROM watering_schedual WHERE SST = ' + request.form['SST']
    cursor.execute(sql1)
    mysql.connection.commit()
    result = cursor.fetchall()
    sendlist = []
    for i in result:
        a = {'SST': i['SST'], 'Time': i['Time'], 'Cycle': i['Cycle'], 'Duration': i['Duration']}
        sendlist.append(a)
    data = json.dumps(sendlist)
    resp = Response(data, status=200, mimetype='application/json')
    return resp

@app.route("/period_remove", methods= ['POST', 'GET'])
def period_remove():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = 'DELETE FROM watering_schedual WHERE SST = ' + request.form['SST']
    cursor.execute(sql)
    mysql.connection.commit()
    return ''

@app.route("/period_watering_response", methods = ['GET', 'POST'])
def period_watering_response():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = 'SELECT * FROM watering_schedual WHERE A_ID = ' + request.form['A_ID']
    cursor.execute(sql)
    mysql.connection.commit()
    result = cursor.fetchall()
    sendlist = []
    for i in result:
        a = {'SST': i['SST'], 'Time': i['Time'], 'Cycle': i['Cycle'], 'Duration': i['Duration']}
        sendlist.append(a)
    data = json.dumps(sendlist)
    resp = Response(data, status=200, mimetype='application/json')
    return resp

@app.route("/period_watering", methods = ['GET', 'POST'])
def period_watering():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    Duration = request.form['Duration']
    Time = request.form['Time']
    Cycle = request.form['Cycle']
    A_ID = request.form['A_ID']
    
    sql = 'INSERT INTO watering_schedual (Time, Cycle, Duration, A_ID) VALUES (' + Time + ',' + Cycle + ',' + Duration + ',' + A_ID + ')'
    cursor.execute(sql)
    mysql.connection.commit()
    return ''


@app.route("/auto_watering_response", methods = ["GET", "POST"])
def auto_watering_response():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = 'SELECT * FROM area'
    cursor.execute(sql)
    mysql.connection.commit()
    record = cursor.fetchall()
    sendlist = []
    for i in record:
        a = {'ID_area': i['A_ID'], 'Name': i['Name'], 'LowestHumidity': i['LowestHumidity'], 'AutoWaterDuration': i['AutoWaterDuration']}
        sendlist.append(a)
    data = json.dumps(sendlist)
    resp = Response(data, status=200, mimetype='application/json')
    return resp

@app.route("/auto_watering", methods = ['GET', 'POST'])
def auto_watering():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = 'UPDATE area SET LowestHumidity = ' + request.form['LowestHumidity'] + ', AutoWaterDuration = ' + request.form['AutoWaterDuration'] + ' WHERE A_ID = ' + request.form['A_ID']
    cursor.execute(sql)
    mysql.connection.commit()
    return ''

@app.route("/home", methods =['GET', 'POST'])
def home():
    if 'loggedin' in session:
        if request.method == 'GET':
            if request.args.get('area'):
                ID=request.args.get('area')
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM temp_record WHERE A_ID = %s ORDER BY T_ID DESC LIMIT 1',(ID,))
                temp_record = cursor.fetchall()
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM light_record WHERE A_ID = %s ORDER BY L_ID DESC LIMIT 1',(ID,))
                light_record = cursor.fetchall()
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM moist_record WHERE A_ID = %s ORDER BY M_ID DESC LIMIT 1',(ID,))
                moist_record = cursor.fetchall()
                cursor.execute('SELECT Status FROM `pumper` WHERE A_ID = %s', (ID))
                status = cursor.fetchall()
                cursor.execute('SELECT Name FROM `area` WHERE A_ID=%s', (ID))
                name = cursor.fetchall()
                cursor.execute('SELECT * FROM `area`')
                area = cursor.fetchall()     
                return render_template("homepage.html", temp_record = temp_record, light_record = light_record, moist_record = moist_record, status=status, area=area, name=name)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM temp_record WHERE A_ID = 1 ORDER BY T_ID DESC LIMIT 1')
        temp_record = cursor.fetchall()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM light_record WHERE A_ID = 1 ORDER BY L_ID DESC LIMIT 1')
        light_record = cursor.fetchall()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM moist_record WHERE A_ID = 1 ORDER BY M_ID DESC LIMIT 1')
        moist_record = cursor.fetchall()
        cursor.execute('SELECT Status FROM `pumper` WHERE A_ID = 1')
        status = cursor.fetchall()
        cursor.execute('SELECT Name FROM `area` WHERE A_ID=1')
        name = cursor.fetchall()
        cursor.execute('SELECT * FROM `area`')
        area = cursor.fetchall()     
        return render_template("homepage.html", temp_record = temp_record, light_record = light_record, moist_record = moist_record, status=status, area=area, name=name)
    return redirect(url_for('login'))

@app.route("/signin", methods =['GET', 'POST'])
def signin():
    mesage = ''
    succ=''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form :
        userName = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE UserName = % s', (userName, ))
        account = cursor.fetchone()
        if account:
            mesage = 'User already exists !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, NULL, NULL, NULL, NULL, NULL, NULL)', (userName, password))
            mysql.connection.commit()
            succ = 'New user created!'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('sign_in.html', mesage = mesage,succ=succ)


@app.route("/pump_respone", methods = ['GET', 'POST'])
def pump_respone():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = 'SELECT Status FROM pumper WHERE A_ID = ' + request.form['A_Id']
    cursor.execute(sql)
    record = cursor.fetchall()
    sendlist = []
    if (len(record) != 0):
        sendlist = [{'status': record[0]['Status']}]
    data = json.dumps(sendlist)
    resp = Response(data, status=200, mimetype='application/json')
    return resp

@app.route("/active_pump", methods=['GET', 'POST'])
def active_pump():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = 'UPDATE pumper SET Status = "Đang hoạt động", type_watering = "1" WHERE P_ID =' + request.form['A_Id']
    cursor.execute(sql)
    mysql.connection.commit()
    time_pump = int(request.form['Minus']) * 60 +  int(request.form['Second'])

    for i in range(time_pump):
        sql = 'SELECT Status FROM pumper WHERE A_ID = ' + request.form['A_Id']
        cursor.execute(sql)
        record = cursor.fetchall()
        if record[0]['Status'] == "Đang tắt": 
                return ''
        cursor.execute(sql)
        time.sleep(1)
    
    return inactive_pump()

@app.route("/inactive_pump", methods=['GET', 'POST'])
def inactive_pump():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    sql1 = 'SELECT * FROM pumper'
    cursor.execute(sql1)
    mysql.connection.commit()
    record1 = cursor.fetchall()
    print(record1)
    
    sql = 'UPDATE pumper SET Status = "Đang tắt" WHERE A_ID =' + request.form['A_Id'] 
    cursor.execute(sql)
    mysql.connection.commit()
    sql = 'SELECT * FROM pumper'
    cursor.execute(sql)
    mysql.connection.commit()
    record = cursor.fetchall()
    print(record)
    return ''



@app.route("/statistical_area/", methods=['GET', 'POST'])  
def statistical_area():
    sql = 'SELECT A_ID, SUM(amount) FROM area_record WHERE DateTime >= \'' + request.form['TimeStart'].replace("T"," ") + '\' AND DateTime <= \'' + request.form['TimeEnd'].replace("T"," ") + '\'' + 'GROUP BY A_ID;'
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(sql)
    record = cursor.fetchall()
    sendlist = []
    for item in record:
        i = {'code': str(item['A_ID']), 'pop': str(item['SUM(amount)'])}
        sendlist.append(i)
    data = json.dumps(sendlist)
    resp = Response(data, status=200, mimetype='application/json')
    return resp


@app.route("/statistical_table/", methods=['GET', 'POST'])  
def statistical_table():
    sql1 = 'SELECT '
    sql2 = ''
    sql3 = ''
    sql4 = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.form['element'] == 'Moist': 
        sql3 = ' AVG(data) FROM moist_record WHERE A_ID = ' + request.form['area'] + ' AND DateTime >= \'' + request.form['TimeStart'].replace("T"," ") + '\' AND DateTime <= \'' + request.form['TimeEnd'].replace("T"," ") + '\''
    elif request.form['element'] == 'Temp': 
        sql3 = ' AVG(data) FROM temp_record WHERE A_ID = ' + request.form['area'] + ' AND DateTime >= \'' + request.form['TimeStart'].replace("T"," ") + '\' AND DateTime <= \'' + request.form['TimeEnd'].replace("T"," ") + '\''
    elif request.form['element'] == 'Light': 
        sql3 = ' AVG(data) FROM light_record WHERE A_ID = ' + request.form['area'] + ' AND DateTime >= \'' + request.form['TimeStart'].replace("T"," ") + '\' AND DateTime <= \'' + request.form['TimeEnd'].replace("T"," ") + '\''
    else: 
        sql3 = 'AVG(Time), Type FROM pumper_record WHERE A_ID = ' + request.form['area'] + ' AND DateTime >= \'' + request.form['TimeStart'].replace("T"," ") + '\' AND DateTime <= \'' + request.form['TimeEnd'].replace("T"," ") + '\''

    if request.form['element'] == 'pumper':
        sql4 = ' GROUP BY Type;'
    elif request.form['unit'] == 'month': 
        sql2 = ' YEAR(DateTime), MONTH(DateTime),'
        sql4 = ' GROUP BY YEAR(DateTime), MONTH(DateTime);'
    elif request.form['unit'] == 'week': 
        sql2 = ' YEAR(DateTime), WEEK(DateTime),'
        sql4 = ' GROUP BY YEAR(DateTime), WEEK(DateTime);'
    elif request.form['unit'] == 'day': 
        sql2 = ' YEAR(DateTime), MONTH(DateTime), DAY(DateTime),'
        sql4 = ' GROUP BY YEAR(DateTime), MONTH(DateTime), DAY(DateTime);'
    elif request.form['unit'] == 'hour': 
        sql2 = ' YEAR(DateTime), MONTH(DateTime), DAY(DateTime), HOUR(DateTime),'
        sql4 = ' GROUP BY YEAR(DateTime), MONTH(DateTime), DAY(DateTime), HOUR(DateTime);'

    sql = sql1 + sql2 + sql3 + sql4
    cursor.execute(sql)
    record = cursor.fetchall()
    sendlist = []
    offset = 0
    sum = 0

    if request.form['element'] == 'pumper':
        for item in record:
            i = {'type': str(item['Type']), 'value': str(item['AVG(Time)'])}
            sum += item['AVG(Time)']
            sendlist.append(i)
            offset = offset + 1
        i = {'type': '4', 'value': str(100 - sum)}
        sendlist.append(i)

    elif request.form['unit'] == 'hour':
        for item in record:
            i = {'offset': offset, 'time': str(item['YEAR(DateTime)']) + "/" + str(item['MONTH(DateTime)']) + "/" + str(item['DAY(DateTime)']) + " " + str(item['HOUR(DateTime)'] + 1) + "h", 'value': str(item['AVG(data)'])}
            sendlist.append(i)
            offset = offset + 1
    
    elif request.form['unit'] == 'day':
        for item in record:
            i = {'offset': offset,'time': str(item['YEAR(DateTime)']) + "/" + str(item['MONTH(DateTime)']) + "/" + str(item['DAY(DateTime)']), 'value': str(item['AVG(data)'])}
            sendlist.append(i)
            offset = offset + 1

    elif request.form['unit'] == 'month':
        for item in record:
            i = {'offset': offset, 'time': str(item['YEAR(DateTime)']) + "/" + str(item['MONTH(DateTime)']), 'value': str(item['AVG(data)'])}
            sendlist.append(i)
            offset = offset + 1

    else: 
        for item in record:
            i = {'offset': offset, 'time': str(item['YEAR(DateTime)']) + "/" + str(item['WEEK(DateTime)']), 'value': str(item['AVG(data)'])}
            sendlist.append(i)
            offset = offset + 1
    
    time.sleep(1)
    
    data = json.dumps(sendlist)
    resp = Response(data, status=200, mimetype='application/json')
    return resp

if __name__ == '__main__':
    app.run(host ='0.0.0.0', debug=True , port=5000, use_reloader=False)