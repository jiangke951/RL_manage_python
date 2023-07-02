# app.py中初始化创建app的工厂函数，在工厂函数中创建Flask()这个app核心对象，并配置相关参数，注册蓝图。
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
class Config(object):  # 配置信息
    JSON_AS_ASCII = False  # 中文不转为ascii码
    # 数据库配置
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    # 连接数据库、其中username为你的登录的用户名，password则为登录密码
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:12345678@localhost:3306/library?charset=utf8'


db = SQLAlchemy()


def create_app():
    # 获取当前文件名，实例化flask对象
    app = Flask(__name__)
    app.app_context().push()
    app.jinja_env.auto_reload = True
    myconfig = Config()
    app.config.from_object(myconfig)
    db.init_app(app)
    from controller.user import userapp  # flask应用程序中注册蓝图
    app.register_blueprint(userapp)
    # 后台管理
    from controller.backuser import backuserapp
    app.register_blueprint(backuserapp)
    from controller.backseat import backseatapp
    app.register_blueprint(backseatapp)
    from controller.backnotice import backnoticeapp
    app.register_blueprint(backnoticeapp)
    from controller.backreserve import backreserveapp
    app.register_blueprint(backreserveapp)
    # 前台显示
    from controller.frontnotice import frontnoticeapp
    app.register_blueprint(frontnoticeapp)
    from controller.frontread import frontreadapp
    app.register_blueprint(frontreadapp)
    from controller.frontseat import frontseatapp
    app.register_blueprint(frontseatapp)
    from controller.frontreserve import frontreserveapp
    app.register_blueprint(frontreserveapp)
    from controller.fronttest import fronttestapp
    app.register_blueprint(fronttestapp)
    return app
