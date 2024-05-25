from flask import render_template, request, redirect, url_for, make_response
from flask_cors import CORS
from datetime import datetime
import json
from flask_sqlalchemy import SQLAlchemy
import re
import time
from app import create_app


app = create_app()  # 创建flask应用程序
CORS(app, supports_credentials=True)  # 配置全局路由




if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=4057)

