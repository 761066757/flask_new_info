# -*- coding: utf-8 -*-
# @Time    : 2020/6/15 17:43
# @Author  : Eric Lee
# @Email   : li.yan_li@neusoft.com
# @File    : manage.py 只负责基本的启动工作
# app 的创建在 info 下的__init__ 中
# @Software: PyCharm
import redis
from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from config import Config,config_dict
import logging
from logging.handlers import RotatingFileHandler
from flask_wtf.csrf import generate_csrf


db = SQLAlchemy()
redis_store = None

def create_app(config_name):
    """通过传入不同的配置名,切换不同的环境"""
    app = Flask(__name__)

    config = config_dict.get(config_name)

    # 设置日志级别
    log_file(config.LEVEL)
    app.config.from_object(Config)
    # app.config.from_object(Config)要 init_app之前
    # SQLAlchemy对象关联app
    db.init_app(app)

    # 创建redis对象
    global redis_store
    redis_store = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
    # 初始化数据库
    # 初始化redis 对象
    # 开启csrf保护，只做服务器验证功能，
    # TODO
    CSRFProtect(app)
    # 设置session保存指定位置
    Session(app)

    # 注册蓝图时，导入和注册写在一起
    from info.modules.index import index_blu
    app.register_blueprint(index_blu)

    from info.modules.news import news_blu
    app.register_blueprint(news_blu)

    from info.modules.passport import passport_blu
    app.register_blueprint(passport_blu)

    from info.utils.common import do_index_class
    app.add_template_filter(do_index_class, "index_class")

    @app.after_request
    def after_request(response):
        # 调用生成csrf 的函数
        csrf_token = generate_csrf()
        # 通过cookie传递给前台
        response.set_cookie("csrf_token", csrf_token)
        return response
    return app

# 记录日志
def log_file(level):
    # 设置日志的记录等级,常见等级有: DEBUG<INFO<WARING<ERROR
    logging.basicConfig(level=level)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)