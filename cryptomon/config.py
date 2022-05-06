import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = os.path.abspath(os.path.dirname(__file__))

# Create the connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app

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
    database = 'cmc'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@127.0.0.1:4306/%s' % (user,password,database)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@www.wxwroger.top:4306/%s' % (user,password,database)
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


