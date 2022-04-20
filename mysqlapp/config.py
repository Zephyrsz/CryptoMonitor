import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = os.path.abspath(os.path.dirname(__file__))

# Create the connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app
#
# # Build the Sqlite ULR for SqlAlchemy
# sqlite_url = "sqlite:///" + os.path.join(basedir, "people.db")
#
# # Configure the SqlAlchemy part of the app instance
# app.config["SQLALCHEMY_ECHO"] = True
# app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_url
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#
# # Create the SqlAlchemy db instance
# db = SQLAlchemy(app)
#
# # Initialize Marshmallow
# ma = Marshmallow(app)


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

# app = Flask(__name__)

class Config(object):
    """配置参数"""
    # 设置连接数据库的URL
    user = 'root'
    password = 'rootpwd123'
    database = 'test'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@127.0.0.1:4306/%s' % (user,password,database)

    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 查询时会显示原始SQL语句
    app.config['SQLALCHEMY_ECHO'] = True

    # 禁止自动提交数据处理
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False

# 读取配置
app.config.from_object(Config)

# 创建数据库sqlalchemy工具对象
db = SQLAlchemy(app)
# Initialize Marshmallow
ma = Marshmallow(app)
# class Role(db.Model):
#     # 定义表名
#     __tablename__ = 'roles'
#     # 定义字段
#     id = db.Column(db.Integer, primary_key=True,autoincrement=True)
#     name = db.Column(db.String(64), unique=True)
#     users = db.relationship('User',backref='role') # 反推与role关联的多个User模型对象
#
# class User(db.Model):
#     # 定义表名
#     __tablename__ = 'users'
#     # 定义字段
#     id = db.Column(db.Integer, primary_key=True,autoincrement=True)
#     name = db.Column(db.String(64), unique=True, index=True)
#     email = db.Column(db.String(64),unique=True)
#     pswd = db.Column(db.String(64))
#     role_id = db.Column(db.Integer, db.ForeignKey('roles.id')) # 设置外键

