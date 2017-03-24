from flask import Flask, render_template, redirect, url_for, flash, request
from flask_socketio import SocketIO, send
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
# URI format: dialect+driver://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/vlc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

Bootstrap(app)

db = SQLAlchemy(app)

socketio = SocketIO(app)


class History(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    message = db.Column('message', db.String(100))


@socketio.on('message')
def hadleMessage(msg):
    print msg
    message = History(message=msg)
    db.session.add(message)
    db.session.commit()

    send(msg, broadcast=True)


@app.route('/')
def index():
    messages = History.query.all()
    return render_template('chatroom.html', title="Index", messages=messages)


if __name__ == '__main__':
    # app.run(debug=True, port=9527) can not work!!
    socketio.run(app, port=9527)
