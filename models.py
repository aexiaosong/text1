from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    telephone = db.Column(db.String(11),nullable=False)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False)

    def __init__(self,*args,**kwargs):
        telephone = kwargs.get('telephone')
        username = kwargs.get('username')
        password = kwargs.get('password')

        self.telephone = telephone
        self.username = username
        self.password = generate_password_hash(password)

    def check_password(self,raw_password):
        result = check_password_hash(self.password,raw_password)
        return result


class Water(db.Model):
    __tablename__ = 'water'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    # now()获取的是服务器第一次运行的时间
    # now就是每次创建一个模型的时候，都获取当前的时间
    create_time = db.Column(db.DateTime,default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    author = db.relationship('User',backref=db.backref('waters'))


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    water_id = db.Column(db.Integer, db.ForeignKey('water.id'))  # 引用water表中的id为外键
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 引用user表中的id为外键

    water = db.relationship('Water', backref=db.backref('answers'))
    author = db.relationship('User', backref=db.backref('answers'))





# class Answer(db.Model):
#     __tablename__ = 'answer'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     content = db.Column(db.Text,nullable=False)
#     create_time = db.Column(db.DateTime,default=datetime.now)
#     question_id = db.Column(db.Integer,db.ForeignKey('water.id'))
#     author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
#
#     question = db.relationship('Water',backref=db.backref('answers',order_by=id.desc()))
#     author = db.relationship('User',backref=db.backref('answers'))