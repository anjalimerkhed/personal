from flask import Flask, render_template, jsonify, request, url_for, redirect, session
from flask_cors import CORS
from datetime import datetime
from database import mydb,cursor
import os
from werkzeug.utils import secure_filename

app = Flask(__name__) 
CORS(app)


@app.route('/', methods=['GET', 'POST'])
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

              # Insert data into the database
            sql = "INSERT INTO enterprise (enterprisename, username, password, email, mobile, logopath, admin, datecreated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (enterprisename, username, password, email, mobile, filepath, 1, datecreated)
            cursor.execute(sql, val)
            mydb.commit()

            return "User registered successfully!"
            
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        print('username : ', username)
        cursor.execute('SELECT * FROM enterprise WHERE username = %s;', (username,))
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
            msg = 'User Not Found'
            return render_template('login1.html', msg=msg)

    return render_template('login1.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug = True)