from flask import Flask, render_template, request, redirect, url_for
import os
from flaskext.mysql import MySQL
from execSQL import *
from hashlib import md5

app = Flask(__name__, template_folder="templates", static_folder="static")

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
#app.config['MYSQL_DATABASE_DB'] = 'Database'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor =conn.cursor()
cursor.execute("use covidtest_fall2020")
# exec_sql_file(cursor, './db_init.sql')
#cursor.execute("SELECT * FROM STUDENT")
#data = cursor.fetchall()
#print(data)
# exec_proc_file(cursor, './db_procedure.sql')
#cursor.callproc('view_testers')
#cursor.execute("SELECT * FROM view_testers_result")
#data = cursor.fetchall()
#print(data)


# screen 1
@app.route("/", methods=['GET', 'POST'])
def index():
    line = ""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = md5(request.form['password'].encode('utf-8')).hexdigest()

        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM user WHERE username = %s AND user_password = %s', (username, password))
        account = cursor.fetchone()
        # we can now get the username and password here
        # after checking, we need to find the user type and redirect to home
        is_student = cursor.execute('SELECT * FROM student WHERE student_username = %s',(username))
        if is_student:
            return redirect(url_for("home", user_type='Student', user_name=username))
        is_admin = cursor.execute('SELECT * FROM administrator WHERE admin_username = %s',(username))
        if is_admin:
            return redirect(url_for("home", user_type='Admin', user_name=username))
        is_labtech = cursor.execute('SELECT * FROM labtech WHERE labtech_username = %s',(username))
        is_sitetester = cursor.execute('SELECT * FROM sitetester WHERE sitetester_username = %s',(username))
        if is_labtech==1 and is_sitetester==1:
            return redirect(url_for("home", user_type='Lab Technician/Tester', user_name=username))
        elif is_labtech==1 and is_sitetester == 0:
            return redirect(url_for("home", user_type='Lab Technician', user_name=username))
        elif is_labtech ==0 and is_sitetester==1: 
            return redirect(url_for("home", user_type='Tester', user_name=username))
        else:
            line = "Incorrect username/password!"

    return render_template("index.html", msg=line)

# screen 2 
@app.route("/register", methods=['GET', 'POST'])
def register():
    # do the similar as the function above 
    if request.method == 'POST':
        print(request.form)
        username = request.form['username']
        email = request.form['email']
        fname = request.form['fname']
        lname = request.form['lname']
        password = md5(request.form['password'].encode('utf-8'))
        if "lab_tech" in request.form:
            print("lab_tech")
    return render_template('register.html')

# screen 3
@app.route("/home", methods=['GET', 'POST'])
def home():
    user_type = ""
    user_name = ""
    if request.method == 'GET':
        user_type = request.args.get('user_type')
        user_name = request.args.get('user_name')

    return render_template("home.html", user_type = user_type, user_name = user_name)

# screen 4
@app.route("/student_test_results", methods=['GET','POST'])
def student_test_results():
    data = ()
    student_name = '' # to get student_name 
    if request.method == 'GET':
        student_name = request.args.get('user_name')
   
    if request.method == 'POST':
        student_name = request.form['student_name']
        status = request.form["status"]
        startDate = request.form["startDate"]
        if startDate == '':
            startDate = None
        endDate = request.form["endDate"]
        if endDate == '':
            endDate = None
        # sql = 'call student_view_results(%s, %s, %s, %s)', (student_name,status, startDate, endDate)
        # print(sql)
        search_count = cursor.execute('call student_view_results(%s, %s, %s, %s)', (student_name,status, startDate, endDate))
        cursor.execute('select * from student_view_results_result')
        data = cursor.fetchall()
        return render_template("student_test_results.html", data_dict = data, user_name = student_name)

    return render_template("student_test_results.html", data_dict = data, user_name=student_name)

#  screen 5
@app.route("/explore_test_result")
def explore_test_result():
    return render_template("explore_test_result.html")

#  screen 6
@app.route("/aggregate_results")
def aggregate_results():
    return render_template("aggregate_results.html")

#  screen 7
@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")

#screen 8
@app.route("/labtech_tests_processed",methods=['GET', 'POST'])
def labtech_tests_processed():
    # simulate the data
    data = {
        1:['1', '22332','8/17/20','8/29/20','Negative'],
        2:['1', '22332','8/17/20','8/29/20','Negative'],
    }
    return render_template("labtech_tests_processed.html", data_dict=data)

#screen 9
@app.route("/view_pools", methods=['GET', 'POST'])
def view_pools():
    data = {
        1:['23332', '1,2,3','8/17/20','jim123','Negative'],
        2:['2332', '4,5,6','8/17/20','jim456','Negative'],
    }
    return render_template("view_pools.html",data_dict=data)

# screen 10
@app.route("/create_pool")
def create_pool():
    return render_template("create_pool.html")

#screen 11
@app.route("/process_pool", methods=["GET", "POST"])
def process_pool():
    pool_id = 1234
    data = {
        1:['1','8/17/20','Negative'],
        2:['2','8/19/20','Negatve'],
    }
    return render_template("process_pool.html", pool_id = pool_id, data_dict=data)

# screen 12
@app.route("/create_appointment")
def create_appointment():
    return render_template("create_appointment.html")


# screen 15
@app.route("/create_testing_site")
def create_testing_site():
    return render_template("create_testing_site.html")

# screen 16
@app.route("/explore_pool_result")
def explore_pool_result():
    return render_template("explore_pool_result.html")

# screen 17
@app.route("/change_testing_site")
def change_testing_site():
    return render_template("change_testing_site")

# screen 18
@app.route("/daily_results")
def daily_results():
    return render_template("daily_results.html")



if __name__ == '__main__':
    app.run(debug=True)