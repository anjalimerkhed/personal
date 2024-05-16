from flask import Flask, render_template, jsonify, request, url_for, redirect, session
from flask_cors import CORS
from paho.mqtt import client as mqtt_client
import mysql.connector
from datetime import datetime
from MQTT_file import mydb,cursor
import os
from werkzeug.utils import secure_filename

app = Flask(__name__) 
CORS(app)
app.secret_key = 'your_secret_key'

username = None
all_data = []

class SessionNames:
    user_id = 'user_id'
    img_path = 'img_path'
    acc_name = 'acc_name'


def get_data(user_id):
    query_string = "SELECT d.id AS dpth_id, d.device_name, d.dp_value, d.temp_value, d.hum_value, d.timestamp AS dpth_timestamp, dv.id AS device_id, dv.user_id FROM dpth_reading d JOIN (SELECT MAX(id) AS max_id, device_name FROM dpth_reading GROUP BY device_name) AS x ON d.id = x.max_id AND d.device_name = x.device_name JOIN device dv ON d.device_name = dv.device_name AND dv.user_id = %s ;"
    cursor.execute(query_string, (user_id,))
    data = cursor.fetchall()
    return data

@app.route('/register', methods=['GET', 'POST'])
def register():
        if request.method == 'POST':
            enterprisename = request.form['enterprisename']
            print(enterprisename)
            username = request.form['username']
            print(username)
            password = request.form['password']
            print(password)
            email = request.form['email']
            print(email)
            mobile = request.form['mobile']
            print(mobile)
            logopath = request.files['file']
            filename = secure_filename(logopath.filename)  # Ensures secure filename
            filepath = os.path.join('static/uploads/', filename)
            logopath.save(filepath)
            print(filepath)
            datecreated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(datecreated)
            # Check if the username or email already exists in the database
            cursor.execute("SELECT * FROM enterprise WHERE username = %s or email = %s or mobile = %s", (username, email, mobile))
            existing_user = cursor.fetchall()
            if existing_user:
                error_message = "User already exists."
                return render_template('register.html', error=error_message)
              # Insert data into the database
            sql = "INSERT INTO enterprise (enterprisename, username, password, email, mobile, logopath, admin, datecreated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (enterprisename, username, password, email, mobile, filepath, 0, datecreated)
            cursor.execute(sql, val)
            mydb.commit()
            session['alert'] = "User Registered Successfully."
            return redirect (url_for('login'))
       
        return render_template('register.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    alert = session.pop('alert', None)
    if request.method == 'POST':
        username = request.form['username']
        print(username)
        password = request.form['password']
        print(password)
        cursor.execute('SELECT * FROM enterprise WHERE username = %s AND password = %s ;', (username, password))
        account = cursor.fetchall()
        print('account', account)

        if account:
            user_id = account[0][0]
            session['user_id'] = user_id    
            img_path = account[0][6]
            session['img_path'] = img_path
            acc_name = account[0][2]
            session['acc_name'] = acc_name
            return redirect(url_for('home'))
        if not account:
            msg = 'Invalid username or password'
            return render_template('login1.html', msg=msg)

    return render_template('login1.html',alert=alert)

@app.route('/test', methods = ['GET','POST'])
def test(): 
    global all_data
    user_id = session.get('user_id', None)

    data = get_data(user_id)
    
    all_data = []
    for row in data:
        result = row
        all_data.append({
                'user_id': user_id,
                'name': result[1],
                'dp': result[2],
                'temp': result[3],
                'hum': result[4],
                'time': result[5]
        })
    mydb.commit()
    # print('all_data : ', all_data)
    return jsonify(all_data)
 
@app.route('/home', methods = ['GET','POST'])
def home():
    img_path = session.get('img_path', None)
    acc_name = session.get('acc_name', None)
    user_id = session.get('user_id', None)
    all_data = test().json  # Call the /test endpoint and get the JSON data
    print('img_path : ', img_path)
    print('acc_name : ', acc_name)
    print('user_id : ', user_id)
    print('all_data : ', all_data)
    return render_template('temp_hum_dp.html', img = img_path, acc_name = acc_name, all_data = all_data, user_id = user_id)


@app.route('/add_device', methods=['GET', 'POST'])
def add_device():
     img_path = session.get('img_path', None)
     if request.method == 'POST':
        devicename = request.form['devicename']
        # print("devicename", devicename)
        # Retrieve user ID from the session
        user_id = session.get('user_id')
    
        if user_id is None:
            # Handle the case where user_id is not found in the session
            return redirect(url_for('login')) 
        
        time = datetime.now()

        cursor.execute('INSERT INTO device (user_id, device_name, timestamp) VALUES (%s, %s, %s);', (user_id, devicename, time))
        mydb.commit()  # Commit the transaction
        print(f"Device '{devicename}' added successfully!")
        return redirect(url_for('home'))
     
     return render_template('add-device.html', img = img_path)

@app.route('/delete_device', methods=['GET','POST'])  
def delete_device(): 
        img_path = session.get('img_path', None)
        user_id = session.get('user_id') 
        cursor.execute('SELECT * FROM device  WHERE user_id = %s ;', (user_id,))
        devices = cursor.fetchall()
        return render_template('delete_device.html' ,new = devices, img = img_path)

@app.route('/delete/<string:id>', methods=['GET', 'POST'])
def delete(id):
    cursor.execute("UPDATE device SET user_id = 4 where id = %s;", (id,))
    mydb.commit()
    return redirect(url_for('home'))

@app.route('/logout', methods=['GET','POST'])
def logout():
    session.pop(SessionNames.user_id, None)
    session.pop(SessionNames.img_path, None)
    session.pop(SessionNames.acc_name, None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug = True)