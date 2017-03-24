from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_wtf import Form

from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import InputRequired, Email, Length

from flaskext.mysql import MySQL
from bson import ObjectId

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'

app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'vlc'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'

Bootstrap(app)

mysql = MySQL()
mysql.init_app(app)


@app.route('/db_test')
def db_test():
    conn = mysql.connect()
    cur = conn.cursor()
    data = None
    try:
        cur.execute("SELECT * FROM student_pool")
        data = cur.fetchall()
    except Exception as error:
            print 'Read database failed: ', error
    finally:
            cur.close()
    return render_template('vlc_db_test.html', title="DB Test", data=data)

@app.route('/')
def index():
    return render_template('vlc_index.html', title="Index")


@app.route('/student')
def student():
    return render_template('vlc_student.html', title="Student")


@app.route('/tutor')
def tutor():
    return render_template('vlc_tutor.html', title="Tutor")


if __name__ == '__main__':
    app.run(debug=True, port=9527)
