# 通知的基本操作
from flask import Blueprint, render_template, request
from config import get_data, send_cc, send_data, isVaildDate


from models.frontnoticemodel import FrontNotice
from models.usermodel import User

frontnoticeapp = Blueprint('frontnoticeapp', __name__)


# 列表显示通知
@frontnoticeapp.route('/api/front/notice/getnoticelist/<user_id>', methods=['get'])
def get_notice_list(user_id):
    try:
        user_id = int(user_id)
    except Exception as e:
        user_id = 0
    if user_id == 0: return send_cc('无效参数')
    # 判断用户是否存在
    exist_user = User.exist_user(user_id)
    if exist_user == False: return send_cc('用户不存在')
    # 查询通知列表
    noticelist = FrontNotice.get_notice_list(user_id)
    return send_data({'status': 0, 'msg': '查询通知列表成功', 'data': noticelist})



