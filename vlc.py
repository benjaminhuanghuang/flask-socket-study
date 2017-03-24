from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_wtf import Form

from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import InputRequired, Email, Length

from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'

app.config['MONGO_URI'] = 'mongodb://localhost:27017/MathJoy'
app.config['MONGO_DBNAME'] = 'MathJoy'

mongo = PyMongo(app)

Bootstrap(app)


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
