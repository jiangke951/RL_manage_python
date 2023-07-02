# 用户的基本操作，蓝图的定义，用户功能模块的定义
from flask import Blueprint, render_template, request
from config import get_data, send_cc, send_data, isVaildDate, user_status_true, user_status_false, user_status_all


from models.backusermodel import BackUser

backuserapp = Blueprint('backuserapp', __name__)

# 添加用户
@backuserapp.route('/api/back/user/adduser', methods=['post'])
def add_user():
    # 获取客户端发来的表单信息
    userinfo = get_data(request.form)
    if userinfo == [] or userinfo == {} or userinfo == '' or len(userinfo) < 1:
        return send_cc('无效输入')
    account = ''
    username = ''
    pwd = ''
    user_status = ''
    try:
        account = userinfo['account']
        username = userinfo['username']
        pwd = userinfo['password']
        user_status = userinfo['user_status']
    except Exception as e:
        account = ''
        username = ''
        pwd = ''
        user_status = ''
    if account == '' or pwd == '' or username == '' or user_status == '':
        return send_cc('无效输入')
    # 查询数据库是否存在账号
    exist_account = BackUser.exist_account(account)
    if exist_account == True: return send_cc('账号已存在')
    # 添加用户
    BackUser.add_user(account, username, pwd, user_status)
    return send_cc('创建用户信息成功', 0)

# 列表显示用户
@backuserapp.route('/api/back/user/getuserlist', methods=['post'])
def get_user_list():
    # 获取客户端发来的表单信息
    info = get_data(request.form)
    if info == [] or info == {} or info == '' or len(info) < 1:
        return send_cc('无效输入')
    page_no = 0
    page_size = 0
    account = ''
    username = ''
    user_status = ''
    try:
        page_no = int(info['page_no'])
        page_size = int(info['page_size'])
        account = info['account']
        username = info['username']
        user_status = info['user_status']
    except Exception as e:
        page_no = 0
        page_size = 0
        account = ''
        username = ''
        user_status = ''
    if page_no == 0 or page_size == 0: return send_cc('无效参数')
    if user_status != user_status_true and user_status != user_status_false and user_status != user_status_all: return send_cc('请选择用户状态')
    # 查询用户列表
    userlist = BackUser.get_user_list(page_no, page_size, account, username, user_status)
    # 获取全部用户数量
    user_count = BackUser.get_user_count(account, username, user_status)
    return send_data({'status': 0, 'msg': '查询用户列表成功', 'data': userlist, 'user_count': user_count})

# 修改用户信息
@backuserapp.route('/api/back/user/updateuserinfo', methods=['post'])
def back_update_userinfo():
    # 获取客户端发来的表单信息
    userinfo = get_data(request.form)
    if userinfo == [] or userinfo == {} or userinfo == '' or len(userinfo) < 1:
        return send_cc('无效输入')
    user_id = 0
    pwd = ''
    user_status = ''
    try:
        user_id = int(userinfo['user_id'])
        pwd = userinfo['password']
        user_status = userinfo['user_status']
    except Exception as e:
        user_id = 0
        pwd = ''
        user_status = ''
    if user_status == '' or user_id == 0:
        return send_cc('无效输入')
    if user_status != user_status_true and user_status != user_status_false: return send_cc('无效输入')
    # 查询数据库是否存在该用户
    exist_user = BackUser.exist_user(user_id)
    if exist_user == False: return send_cc('用户不存在')
    # 修改用户信息
    if pwd == '':
        BackUser.back_update_user_status(user_id, user_status)
    else:
        BackUser.back_update_userinfo(user_id, pwd, user_status)
    return send_cc('用户信息修改成功', 0)

# 封禁用户
@backuserapp.route('/api/back/user/deluser/<user_id>', methods=['get'])
def del_user(user_id):
    try:
        user_id = int(user_id)
    except Exception as e:
        user_id = 0
    if user_id == 0: return send_cc('无效参数')
    # 查询用户是否存在
    exist_user = BackUser.exist_user(user_id)
    if exist_user == False: return send_cc('用户不存在')
    # 封禁用户
    BackUser.del_user(user_id)
    return send_cc('用户已被封禁!', 0)

#
