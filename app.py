from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors 
import MySQLdb
import re
import os
from model import getLLamaresponse
from course import  get_course
from pdf import get_pdf
import requests

  
  
app = Flask(__name__)

"""# Set secret key for session management
app.secret_key = 'xyzsdfg'

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'myappdb'

# Initialize MySQL
mysql = MySQL(app)

# Define function to create MySQL connection
def create_connection():
    return mysql.connection

# Define function to create MySQL cursor
def create_cursor():
    with app.app_context():
        conn = create_connection()
        return conn.cursor()

# Create cursor for database operations
cursor = create_cursor()

# Example usage of the cursor
cursor.execute("SELECT * FROM user")
rows = cursor.fetchall()




# Create users table if it doesn't exist
#cursor.execute('''CREATE TABLE IF NOT EXISTS users
                 # (username VARCHAR(255) PRIMARY KEY, email VARCHAR(255), password VARCHAR(255))''')

def create_user(username, email, password):
    # Hash the password before storing it
    # hashed_password = hashlib.sha256(password.encode()).hexdigest()
    # Insert user data into the database
    cursor.execute("INSERT INTO user (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
    conn.commit()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'myappdb'
 """ 

  
@app.route('/running')
def running():
       return  render_template('running.html')

@app.route('/pcd_login', methods=['GET', 'POST'])
def login():
    message = ''
    """if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()
        
        if user:
            session['loggedin'] = True
            session['userid'] = user[0]
            session['username'] = user[1]
            session['email'] = user[2]
            message = 'Logged in successfully!'
            return redirect(url_for('homepage'))
        else:
            message = 'Please enter correct email/password!'"""
    return render_template('pcd_login.html', message=message)

  

  
@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        email = request.form['email']
        
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
        account = cursor.fetchone()
        
        if account:
            message = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address!'
        elif not username or not password or not email:
            message = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO user (username, email, password) VALUES (%s, %s, %s)', (username, email, password))
            conn.commit()
            message = 'You have successfully registered!'
    return render_template('register.html', message=message)

    
mysql = MySQL(app)
@app.route('/')
def home():
    return render_template('pcd_homepage.html')

@app.route('/homepage')
def home_again():
    return render_template('pcd_homepage.html')


@app.route('/pcd_service')
def service():
    return render_template('pcd_service.html')

@app.route('/index_course', methods=['GET', 'POST'])
def index_course():
    if request.method == 'POST':
        keyword = request.form['keyword']
        response = get_course(keyword)
        return render_template('pcd_generate_course.html', keyword=keyword, response=response)
    return render_template('pcd_generate_course.html', keyword=None, response=None)


@app.route('/index_pdf', methods=['GET', 'POST'])
def index_pdf():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            return render_template('pdc_pdf.html', error_message="No file part")
        
        pdf_file = request.files['pdf_file']
        
        if pdf_file.filename == '':
            return render_template('pcd_pdf.html', error_message="No selected file")
        
        # Create the 'uploads' directory if it doesn't exist
        uploads_dir = os.path.join(os.getcwd(), 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        
        # Save the uploaded PDF file
        uploaded_pdf_path = os.path.join(uploads_dir, pdf_file.filename)
        pdf_file.save(uploaded_pdf_path)
        
        # Generate summary using your model
        summary = get_pdf(uploaded_pdf_path)  # Replace 'get_pdf' with your actual function
        
        if summary:
            return render_template('pcd_pdf.html', pdf_url=uploaded_pdf_path, summary=summary)
        else:
            return render_template('pcd_pdf.html', pdf_url=uploaded_pdf_path, error_message="Error processing PDF")
    
    return render_template('pcd_pdf.html', pdf_url=None, summary=None, error_message=None)





# Route for model_page.html
@app.route('/model_page', methods=['GET', 'POST'])
def model_page():
        if request.method == 'POST':
            input_data = request.form['input_data']
            response = getLLamaresponse(input_data)
         
            return render_template('result.html', response=response)
        return render_template('model_page.html')
@app.route('/profil')
def profil():
     return render_template('profil.html')
@app.route('/pdf')
def profilze():
     return render_template('pdf.html')
@app.route('/test')
def profilee():
     return render_template('test.html')
@app.route('/admin')
def admin():
     return render_template('admin.html')








if __name__ == '__main__':
    app.run(debug=True)
"""app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'myappdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Use dictionary cursor for easier data retrieval

# Initialize MySQL
mysql = MySQL(app)

# Function to create MySQL connection
def create_connection():
    return mysql.connection

# Function to create MySQL cursor
def create_cursor():
    with app.app_context():
        conn = create_connection()
        return conn.cursor()

# Example route to demonstrate MySQL query
@app.route('/index')
def index():
    try:
        cursor = create_cursor()
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()
        cursor.close()
        return str(users)
    except MySQLdb.OperationalError as e:
        return f"Error connecting to MySQL: {e}"

if __name__ == '__main__':
    app.run(debug=True) 
    """