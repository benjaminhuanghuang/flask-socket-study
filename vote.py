from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
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


class Result(db.Model):
    __tablename__ = "results"
    id = db.Column('id', db.Integer, primary_key=True)
    vote = db.Column('vote', db.Integer)


@socketio.on('vote')
def handleVote(ballot):
    print ballot
    vote = Result(vote=ballot)
    db.session.add(vote)
    db.session.commit()

    result1 = Result.query.filter_by(vote=1).count()
    result2 = Result.query.filter_by(vote=2).count()

    emit("vote_result", {'result1': result1, 'result2': result2}, broadcast=True)


@app.route('/')
def index():
    return render_template('vote.html', title="vote")


if __name__ == '__main__':
    # app.run(debug=True, port=9527) can not work!!
    socketio.run(app, port=9527)
    # db.create_all()
