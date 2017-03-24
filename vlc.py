'''
Virtual learning center demo
'''
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
# URI format: dialect+driver://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/vlc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

Bootstrap(app)

db = SQLAlchemy(app)

socketio = SocketIO(app)


class Pool(db.Model):
    __tablename__ = "student_pool"
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.String(50))
    user_name = db.Column('user_name', db.String(50))
    start_ts = db.Column('start_ts', db.DateTime, default=datetime.utcnow)


@app.route('/db_test')
def db_test():
    data = Pool.query.all()
    return render_template('vlc_db_test.html', title="DB Test", data=data)


@app.route('/')
def index():
    return render_template('vlc_index.html', title="Index")


@app.route('/student')
def student():
    return render_template('vlc_student.html', title="Student")


@app.route('/tutor')
def tutor():
    data = Pool.query.all()
    return render_template('vlc_tutor.html', title="Tutor", data=data)


@socketio.on('action')
def hadleMessage(msg):
    arg = msg.split(" ")
    action = arg[0]
    user_name = arg[1]
    if action == "start":
        p = Pool(user_id=user_name, user_name=user_name)
        db.session.add(p)
        db.session.commit()
        notify_tutor()
    elif action == "end":
        p = Pool.query.filter_by(user_name=user_name).first()
        db.session.delete(p)
        db.session.commit()
        notify_tutor

    send(msg, broadcast=True)


def notify_tutor():
    data = Pool.query.all()
    result = []
    for row in data:
        result.append(row2dict(row))
    emit("student_changed", result, broadcast=True)

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d
if __name__ == '__main__':
    socketio.run(app, port=9527)
