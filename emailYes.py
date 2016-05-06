from flask import Flask, request, redirect, render_template, session, flash
from mysql_email import MySQLConnector
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
app = Flask(__name__)
app.secret_key = "ThisIsSecret!"
mysql = MySQLConnector(app,'email_validation')
@app.route('/', methods=['GET'])
def index(): 
    return render_template('email.html') 
@app.route('/success')
def show():
	query = "SELECT * FROM users"
	users = mysql.query_db(query)
	return render_template('success.html', all_users = users)
@app.route('/process', methods = ['POST'])
def submit():
  if len(request.form['email']) < 1:
        flash("Email cannot be blank!")
  elif not EMAIL_REGEX.match(request.form['email']):
      flash ("Email is not valid!")
  else:
      add()
      session['email'] = request.form['email'] 
      # flash ("The email address you entered (____) is a VALID email address! Thank you!")
      return redirect ('/success')
  return redirect ('/')
def add():
  query = "INSERT INTO users (email_address, created_at, updated_at) VALUES (:email_address, NOW(), NOW())"
  data = {
         'email_address': request.form['email']
         }
  mysql.query_db(query,data)
  return redirect ('/')
@app.route('/delete/<id>')
def delete(id):
    query = "DELETE FROM users WHERE users.id = :id"
    data = {
           'id': id
           }
    mysql.query_db(query, data)
    return redirect('/success')

app.run(debug=True)