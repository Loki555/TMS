from flask import Flask, render_template
from views import *
import pymysql
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:taskgogo1234@122.51.132.193:3306/TMS2"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['DEBUG'] = True
db = SQLAlchemy(app)

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


class UserInfo(db.Model):
    __tablename__ = 'userinfo'
    id = db.Column(db.Integer, primary_key=True)
    tel = db.Column(db.String(11))
    email = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(32))
    dept = db.Column(db.String(32))
    title = db.Column(db.String(32))
    created_time = db.Column(db.DateTime, default=datetime.now)
    updated_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    tasks_pub = db.relationship('TaskInfo', backref='user_pub', lazy='dynamic')
    tasks_charge = db.relationship('TaskInfo', backref='user_charge', lazy='dynamic')


class TaskInfo(db.Model):
    __tablename__ = 'taskinfo'
    id = db.Column(db.Integer, primary_key=True)
    user_charge = db.Column(db.Integer, db.ForeignKey('userinfo.id'))
    user_pub = db.Column(db.Integer, db.ForeignKey('userinfo.id'))
    title = db.Column(db.String(32))
    isFinish = db.Column(db.Boolean, default=False)
    pb_content = db.Column(db.Text)
    pb_time = db.Column(db.DateTime)
    ddl = db.Column(db.DateTime)
    sb_content = db.Column(db.Text)
    sd_time = db.Column(db.DateTime)
    attachments = db.relationship('AttachmentInfo', backref='task_id', lazy='dynamic')


class AttachmentInfo(db.Model):
    __tablename__ = 'attachment'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('taskinfo.id'))
    filename = db.Column(db.String(64))
    path = db.Column(db.String(64))


@app.route('/index')
def index():
    return index_view()


@app.route('/login')
def login():
    return login_view()


@app.route('/register')
def register():
    return register_view()


@app.route('/mdf_user')
def mdf_user():
    return mdf_user_view()


if __name__ == '__main__':
    manager.run()
