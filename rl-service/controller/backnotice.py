# 通知的基本操作
from flask import Blueprint, render_template, request
from config import get_data, send_cc, send_data, isVaildDate


from models.backnoticemodel import BackNotice

backnoticeapp = Blueprint('backnoticeapp', __name__)

# 发布通知
@backnoticeapp.route('/api/back/notice/addnotice', methods=['post'])
def add_notice():
    # 获取客户端发来的表单信息
    reqinfo = get_data(request.form)
    if reqinfo == [] or reqinfo == {} or reqinfo == '' or len(reqinfo) < 1:
        return send_cc('无效输入')
    notice_title = ''
    notice_detail = ''
    try:
        notice_title = reqinfo['notice_title']
        notice_detail = reqinfo['notice_detail']
    except Exception as e:
        notice_title = ''
        notice_detail = ''
    if notice_title == '' or notice_detail == '': return send_cc('无效输入')
    # 查询数据库是否存在通知标题
    exist_notice_title = BackNotice.exist_notice_title(notice_title)
    if exist_notice_title == True: return send_cc('已存在该通知')
    # 发布通知
    BackNotice.add_notice(notice_title, notice_detail)
    return send_cc('发布成功', 0)

# 列表显示通知
@backnoticeapp.route('/api/back/notice/getnoticelist', methods=['post'])
def get_notice_list():
    # 获取客户端发来的表单信息
    info = get_data(request.form)
    if info == [] or info == {} or info == '' or len(info) < 1:
        return send_cc('无效输入')
    page_no = 0
    page_size = 0
    notice_title = ''
    try:
        page_no = int(info['page_no'])
        page_size = int(info['page_size'])
        notice_title = info['notice_title']
    except Exception as e:
        page_no = 0
        page_size = 0
        notice_title = ''
    if page_no == 0 or page_size == 0: return send_cc('无效参数')
    # 查询通知列表
    noticelist = BackNotice.get_notice_list(page_no, page_size, notice_title)
    # 获取全部通知数量
    notice_count = BackNotice.get_notice_count(notice_title)
    return send_data({'status': 0, 'msg': '查询通知列表成功', 'data': noticelist, 'notice_count': notice_count})

@backnoticeapp.route('/api/back/notice/delnotice/<notice_id>', methods=['get'])
def del_notice(notice_id):
    try:
        notice_id = int(notice_id)
    except Exception as e:
        notice_id = 0
    if notice_id == 0: return send_cc('无效参数')
    # 查询通知是否存在
    exist_notice = BackNotice.exist_notice(notice_id)
    if exist_notice == False: return send_cc('通知不存在')
    # 删除通知
    BackNotice.del_notice(notice_id)
    return send_cc('通知已被删除!', 0)

