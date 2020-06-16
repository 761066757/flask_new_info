# -*- coding: utf-8 -*-
# @Time    : 2020/6/15 17:43
# @Author  : Eric Lee
# @Email   : li.yan_li@neusoft.com
# @File    : manage.py 只负责基本的启动工作，
# app 的创建在 info 下的__init__ 中
# @Software: PyCharm
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'index'

if __name__ == '__main__':
    app.run()