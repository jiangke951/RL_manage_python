# 通知的基本操作
from flask import Blueprint, render_template, request
from config import get_data, send_cc, send_data, isVaildDate


from models.frontreadmodel import FrontRead
from models.usermodel import User
from models.frontnoticemodel import FrontNotice

frontreadapp = Blueprint('frontreadapp', __name__)


# 根据用户id和通知id设置阅读字段为已读
@frontreadapp.route('/api/front/notice/set_read/<user_id>/<notice_id>', methods=['get'])
def set_read(user_id, notice_id):
    try:
        user_id = int(user_id)
        notice_id = int(notice_id)
    except Exception as e:
        user_id = 0
        notice_id = 0
    if user_id == 0 or notice_id == 0: return send_cc('无效参数')
    # 判断用户是否存在
    exist_user = User.exist_user(user_id)
    if exist_user == False: return send_cc('用户不存在')
    # 查询通知是否存在
    exist_notice = FrontNotice.exist_notice(notice_id)
    if exist_notice == False: return send_cc('通知不存在')
    # 设置字段为已读
    FrontRead.set_read(user_id, notice_id)
    return send_cc('已读', 0)

# 根据用户id设置该用户的通知全部已读
@frontreadapp.route('/api/front/notice/all_set_read/<user_id>', methods=['get'])
def all_set_read(user_id):
    try:
        user_id = int(user_id)
    except Exception as e:
        user_id = 0
    if user_id == 0: return send_cc('无效参数')
    # 判断用户是否存在
    exist_user = User.exist_user(user_id)
    if exist_user == False: return send_cc('用户不存在')
    # 设置该用户全部通知为已读
    FrontRead.all_set_read(user_id)
    return send_cc('全部已读', 0)