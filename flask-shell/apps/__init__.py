from flask import Flask
from flask_session import Session
from flask_login import LoginManager

# 关联数据模型和视图,所以使用全局空对象
login_manager = LoginManager()


def register_db(app):
    from apps.models import db
    db.init_app(app=app)


def register_bp(app):
    from apps.cms import cms_bp
    app.register_blueprint(cms_bp)


def create_app(congig_file: Flask):
    # 创建flask项目对象,配置静态文件
    app = Flask(__name__, static_url_path="/static", static_folder="my_static")
    # 加载orm配置文件
    app.config.from_object(congig_file)
    # session的配置文件加载
    Session(app=app)
    # 初始化login插件,注册到app上
    login_manager.init_app(app=app)
    login_manager.login_view = "cms.login"
    # 初始化数据库
    register_db(app)
    # 将蓝图中的路由表进行注册
    register_bp(app)
    return app


def register_api_bp(app):
    from apps.api import api_bp
    app.register_blueprint(api_bp)


def create_api_add(congig_file: Flask):
    api_app = Flask(__name__, static_folder="web_client", static_url_path="")
    api_app.config.from_object(congig_file)
    register_db(api_app)
    # 注册蓝图
    register_api_bp(api_app)
    return api_app