from flask import Flask, render_template, request, url_for, redirect, jsonify
import re
import random
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# configure the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="form_data"
)
cursor = mydb.cursor()


@app.route("/", methods=['GET', 'POST'])
def basic_form():
    return render_template("login_form.html")


@app.route("/sign_up", methods=['GET', 'POST'])
def form():
    global cursor
    cursor.execute("SELECT * FROM country")
    countries = cursor.fetchall()

    error_msgs = None  # initialize with None
    if request.method == 'POST':
        form = request.form
        name = request.form.get('name')
        print('name : ', name)

        email = request.form.get('email')
        print('email : ', email)

        phoneno = request.form.get('phoneno')
        print('phoneno : ', phoneno)

        password = request.form.get('password')
        print('password : ', password)

        country_name = request.form.get('country_name')
        print('country_name : ', country_name)

        state_name = request.form.get('state_name')
        print('state : ', state_name)

        error_msgs = {}

        # validation logic for name, email, phone
        # assign error_msgs value when there is an error
        name = form['name']
        if not name:
            error_msgs['name'] = "Name is required"
        elif not name.replace(" ", "").isalpha():
            error_msgs['name'] = "Name can only contain alphabets and spaces"

        email = form['email']
        if not email:
            error_msgs['email'] = "Email is required"
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            error_msgs['email'] = "Invalid email address"

        phoneno = form['phoneno']
        if not phoneno:
            error_msgs['phoneno'] = "Phone number is required"
        elif not phoneno.isdigit():
            error_msgs['phoneno'] = "Phone number can only contain digits"
        elif len(phoneno) != 10:
            error_msgs['phoneno'] = "Phone number should be 10 digits long"

        password = form['password']
        if not password:
            error_msgs['password'] = "Password is required"
        elif not re.match(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=])(?=\S+$).{8,}$", password):
            error_msgs['password'] = "Invalid password"

        country_name = form['country_name']
        if not country_name:
            error_msgs['country_name'] = "Please Select Country"

        state_name = form['state_name']
        if not state_name:
            error_msgs['state_name'] = "Please Select State"

        # ----- start -----------
        msg = ''
        query = "SELECT * FROM mydb WHERE  email=%s and phoneno=%s "
        cursor.execute(query, (email, phoneno))
        check_dup = cursor.fetchall()
        print('check_dup : ', check_dup)
        if check_dup:
            msg = "Data already exists"
            return render_template('form.html', msg=msg)
        # ------ end ---------

        if error_msgs:
            return render_template('form.html', errors=error_msgs, name=form['name'], email=form['email'], phoneno=form['phoneno'], password=form['password'], country_name=form['country_name'], state_name=form['state_name'])
        # process form data if there are no validation errors
        else:
            print('country_name vfgsdf', country_name)
            #
            selected_country = f"SELECT country_name FROM country WHERE country_id = {country_name};"
            cursor.execute(selected_country)
            result = cursor.fetchall()
            print("result", result[0][0])
            #
            sql = "INSERT INTO mydb (name, email, phoneno, password, country, state) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (name, email, phoneno, password, result[0][0], state_name)
            cursor.execute(sql, values)
            mydb.commit()
            return redirect(url_for('table'))

    country_len = len(countries)
    return render_template("form.html", countries=countries, country_len=country_len)


@app.route("/country", methods=["POST", "GET"])
def country():
    if request.method == 'POST':
        category_id = request.form['category_id']
        print('category_id ',  category_id)
        cursor.execute(
            "SELECT * FROM state WHERE country_id = %s", [category_id])
        state = cursor.fetchall()
        OutputArray = []
        for row in state:
            print('row  : ', row)
            outputObj = {
                # 'id': row[1],
                'name': row[2]}
            OutputArray.append(outputObj)
    return jsonify(OutputArray)


@app.route('/table', methods=['GET', 'POST'])
def table():
    global cursor
    cursor.execute("SELECT * FROM mydb")
    rows = cursor.fetchall()
    # Render the HTML template with the data
    return render_template('index.html', rows=rows)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    print("id", id)
    select_sql = "SELECT * FROM mydb WHERE id = %s; "
    cursor.execute(select_sql, (id,))
    rows = cursor.fetchall()

    cursor.execute("SELECT * FROM country")
    countries = cursor.fetchall()
    country_len = len(countries)

    if request.method == 'POST':
        name = request.form['name']
        print(' name: ', name)
        email = request.form['email']
        print(' email: ', email)
        phoneno = request.form['phoneno']
        print(' phoneno: ', phoneno)
        country_name = request.form['country_name']
        print(' country_name: ', country_name)
        state_name = request.form['state_name']
        print(' state_name: ', state_name)

        if not country_name:
            if not state_name:
                get_country = f"SELECT country,state FROM mydb WHERE id = {id};"
                cursor.execute(get_country)
                get_country = cursor.fetchall()
                print("get_country: ", get_country[0][0], get_country[0][1])

                update_user_sql = "UPDATE mydb set name = %s, email = %s, phoneno = %s, country = %s, state = %s where id = %s;"
                updated_values = (name, email, phoneno,
                                  get_country[0][0], get_country[0][1], id)
                cursor.execute(update_user_sql, updated_values)
                mydb.commit()
                return redirect(url_for('table'))
        else:
            update_country = f"SELECT country_name FROM country WHERE country_id = {country_name};"
            cursor.execute(update_country)
            update_result = cursor.fetchall()
            print("update_result", update_result[0][0])
            update_user_sql = "UPDATE mydb set name = %s, email = %s, phoneno = %s, country = %s, state = %s where id = %s;"
            updated_values = (name, email, phoneno,
                              update_result[0][0], state_name, id)
            cursor.execute(update_user_sql, updated_values)
            mydb.commit()
            return redirect(url_for('table'))

    return render_template("update_form.html", rows=rows, id=id, countries=countries, country_len=country_len)


@app.route('/delete/<string:id>', methods=['GET', 'POST'])
def delete(id):
    delete_sql = "DELETE FROM mydb WHERE id = %s ;"
    delete_values = (id)
    cursor.execute(delete_sql, [delete_values])
    mydb.commit()
    return redirect(url_for('table'))


email = None
account = None
username = None


@app.route('/login', methods=['GET', 'POST'])
def login():
    global email, account, username
    msg = ''
    if email:
        msg = 'Already Logged In !'
    
        cursor.execute("SELECT * FROM device_type")
        device = cursor.fetchall()

        cursor.execute("SELECT * FROM brand")
        b_name = cursor.fetchall()

        cursor.execute("SELECT * FROM permission")
        per = cursor.fetchall()

        cursor.execute("SELECT * FROM rating")
        rate = cursor.fetchall()

        device_len = len(device)
        b_len = len(b_name)
        p_len = len(per)
        r_len = len(rate)

        return render_template("home.html", msg=msg, username=username, device=device, device_len=device_len, b_name=b_name, b_len=b_len, per=per, p_len=p_len, rate=rate, r_len=r_len)

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor.execute(
            'SELECT * FROM mydb WHERE email = %s AND password = %s;', (email, password,))
        account = cursor.fetchall()
        print('account', account)
        print('account : ', account[0][1])
        username = account[0][1]

        if not account:
            msg = 'Data Not Found'
            return render_template('login_form.html', msg=msg)
        if account:
            # msg = 'Logged in successfully !'
            return redirect(url_for('home'))

    return render_template('login_form.html')


@app.route('/logout')
def logout():
    global email, username
    email = None
    username = None
    return redirect(url_for('login'))


@app.route('/home')
def home():
    if email != None:
        msg = 'Logged in successfully !'
        print("username :", username)

    global account
    cursor.execute("SELECT * FROM device_type")
    device = cursor.fetchall()

    cursor.execute("SELECT * FROM brand")
    b_name = cursor.fetchall()

    cursor.execute("SELECT * FROM permission")
    per = cursor.fetchall()

    cursor.execute("SELECT * FROM rating")
    rate = cursor.fetchall()

    device_len = len(device)
    b_len = len(b_name)
    p_len = len(per)
    r_len = len(rate)

    return render_template('home.html', device=device, device_len=device_len, b_name=b_name, b_len=b_len, per=per, p_len=p_len, rate=rate, r_len=r_len, username=username, msg=msg)


@app.route('/add_device', methods=['GET', 'POST'])
def add_device():
    global account
    cursor.execute("SELECT * FROM device_type")
    device = cursor.fetchall()

    cursor.execute("SELECT * FROM brand")
    b_name = cursor.fetchall()

    cursor.execute("SELECT * FROM permission")
    per = cursor.fetchall()

    cursor.execute("SELECT * FROM rating")
    rate = cursor.fetchall()

    if request.method == 'POST':
        user_id = account[0][0]
        print('user_id: ', user_id)

        device_name = request.form.get('device_name')
        print('device_name: ', device_name)

        device_type = request.form.get('device_type')
        print('device_type: ', device_type)

        capacity = request.form.get('capacity')
        print('capacity: ', capacity)

        brand = request.form.get('brand')
        print('brand: ', brand)

        permission = request.form.get('permission')
        print('permission: ', permission)

        star = request.form.get('star')
        print('star: ', star)

        serial_num = "evzsp" + str(random.randint(0, 99999))
        print("serial_num: ", serial_num)

        select_device = f"SELECT device_name FROM device_type WHERE device_id = {device_name};"
        cursor.execute(select_device)
        res = cursor.fetchall()
        print("result: ", res[0][0])

        add_sql = "INSERT INTO smart_device (user_id, device_name, device_type, capacity, brand, permission, star, serial_num) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        add_values = (user_id, res[0][0], device_type,
                      capacity, brand, permission, star, serial_num)
        cursor.execute(add_sql, add_values)
        mydb.commit()
        return redirect(url_for('device_data'))
    
    device_len = len(device)
    b_len = len(b_name)
    p_len = len(per)
    r_len = len(rate)
    
      
    return render_template('home.html', device=device, device_len=device_len, b_name=b_name, b_len=b_len, per=per, p_len=p_len, rate=rate, r_len=r_len)

@app.route('/device_data', methods=['GET', 'POST'])
def device_data():
    global cursor
    cursor.execute("SELECT * FROM smart_device")
    rows = cursor.fetchall()
    # Render the HTML template with the data
    return render_template('device_data.html', rows=rows)

@app.route('/get_subtype_options', methods=["POST", "GET"])
def get_subtype_options():
    if request.method == "POST":
        category_id = request.form["category_id"]
        cursor.execute(
            "SELECT * FROM device_subtype WHERE device_id = %s", [category_id])
        subtype = cursor.fetchall()
        OutputArray = []
        for row in subtype:
            print("row", row)
            outputObj = {
                "name": row[2]}
            OutputArray.append(outputObj)
    return jsonify(OutputArray)


@app.route('/get_capacity_options', methods=["POST", "GET"])
def get_capacity_options():
    if request.method == "POST":
        category_id = request.form["category_id"]
        print("category_id", category_id)
        cursor.execute(
            "SELECT * FROM capacity WHERE device_id = %s", [category_id])
        capacity = cursor.fetchall()
        OutputArray = []
        for row in capacity:
            print("row", row)
            outputObj = {
                "name": row[2]}
            OutputArray.append(outputObj)
    return jsonify(OutputArray)


@app.route('/update_device', methods=['GET', 'POST'])
def update_device():
    print("id", id)
    select_sql = "SELECT * FROM smart_device WHERE id = %s; "
    cursor.execute(select_sql)
    rows = cursor.fetchall()
    return render_template("update_form.html", rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
