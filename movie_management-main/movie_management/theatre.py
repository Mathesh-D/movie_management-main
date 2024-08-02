from flask import Flask, render_template, request, redirect, url_for, flash
import cx_Oracle

app = Flask(__name__)
app.secret_key = 'your_secret_key'

username = 'scott'
password = 'tiger'
dsn = cx_Oracle.makedsn('localhost', 1521, service_name='orcl')

instant_client_dir = r'C:\Users\Mathava_roopan\Downloads\instantclient-basic-windows.x64-19.21.0.0.0dbru\instantclient_19_21'
cx_Oracle.init_oracle_client(lib_dir=instant_client_dir)

global_connection = cx_Oracle.connect(username, password, dsn)
global_cursor = global_connection.cursor()

@app.route('/')
def home():
    return render_template('theatrelogin.html')

@app.route('/theatre/login', methods=['POST'])
def theatre_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        authenticated = authenticate_theatre(username, password)
        if authenticated:
            return render_template('theatre_dashboard.html', username=username)
        else:
            return render_template('theatrelogin.html', error='Invalid username or password')

@app.route('/theatre/signup', methods=['GET', 'POST'])
def theatre_signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        seats = request.form['seats']
        address = request.form['address']
        phone = request.form['phone']
        # Check if the username already exists
        if is_theatre_username_exists(username):
            flash('Username already exists. Choose a different username.', 'error')
        else:
            # Insert the new theatre into the database
            insert_theatre(username, password, seats, address, phone)
            flash('Sign-up successful. You can now log in.', 'success')
            return redirect(url_for('home'))

    return render_template('theatre_signup.html')

def authenticate_theatre(username, password):
    global_cursor.execute(
        'SELECT COUNT(*) FROM theatre WHERE theatre_name = :username AND password = :password',
        username=username, password=password
    )
    count = global_cursor.fetchone()[0]

    return count > 0

def is_theatre_username_exists(username):
    global_cursor.execute('SELECT COUNT(*) FROM theatre WHERE theatre_name = :username', username=username)
    count = global_cursor.fetchone()[0]

    return count > 0

def insert_theatre(username, password, seats, address, phone):
    global_cursor.execute(
        'INSERT INTO theatre (theatre_name, password, no_of_seats, address, phone) VALUES (:username, :password, :seats, :address, :phone)',
        username=username, password=password, seats=seats, address=address, phone=phone
    )
    global_connection.commit()



if __name__ == '__main__':
    app.run(debug=True)
