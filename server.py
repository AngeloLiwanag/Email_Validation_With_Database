from flask import Flask, render_template, request, redirect, session, flash
# import the function that will return an instance of a connection 
from mysqlconnection import connectToMySQL
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
app.secret_key = "Secret"

@app.route('/')
def index():
    mysql = connectToMySQL('email_validation')
    users = mysql.query_db('SELECT * FROM users;')
    print(users)
    return render_template('index.html')

@app.route('/email', methods = ['POST'])
def email():
    is_valid = True # assume True
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid email address!")
        is_valid = False
    if not is_valid:
        return redirect('/')
    else:
        flash("Thank you for a vaild email!")
        mysql = connectToMySQL('email_validation')
        query = "INSERT INTO users (email) VALUES (%(em)s);"
        data = {
            'em' : request.form['email']
        }
        user_id = mysql.query_db(query, data)
        print(user_id)
        return redirect("/show_submitted")

@app.route('/show_submitted')
def show_submitted():
    mysql = connectToMySQL('email_validation')
    query = "SELECT * FROM users"
    user_id = mysql.query_db('SELECT * FROM users;')
    return render_template ('email_page.html', users = user_id)

if __name__ == "__main__":
    app.run(debug=True)