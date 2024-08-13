# 用户的基本操作，蓝图的定义，用户功能模块的定义
from flask import Blueprint, render_template, request
from config import get_data, send_cc, send_data, isVaildDate, mail

from models.usermodel import User
from models.frontreservemodel import FrontReserve


userapp = Blueprint('userapp', __name__)


# 用户登录
@userapp.route('/api/user/login', methods=['post'])
def user_login():
    # 获取客户端发来的表单信息
    userinfo = get_data(request.form)

    if userinfo == [] or userinfo == {} or userinfo == '' or len(userinfo) < 1:
        return send_cc('无效输入')
    account = ''
    pwd = ''
    try:
        account = userinfo['account']
        pwd = userinfo['password']
    except Exception as e:
        account = ''
        pwd = ''
    if account == '' or pwd == '':
        return send_cc('无效输入')
    #
    user_id = 0
    username = ''
    identity = ''
    user_status = ''
    create_time = ''
    login_time = ''
    # 查询数据库
    find_userinfo = User.user_login(account, pwd)
    if find_userinfo == {} or len(find_userinfo) < 1:
        return send_cc('登录失败, 账号或密码错误')
    else:
        # 访问量+1
        User.add_login_count()
        # 用户信息
        user_id = find_userinfo['user_id']
        username = find_userinfo['username']
        identity = find_userinfo['identity']
        user_status = find_userinfo['user_status']
        create_time = find_userinfo['create_time']
        login_time = find_userinfo['login_time']
        return send_data({
            'status': 0,
            'msg': '登录成功',
            'data': {
                'user_id': user_id,
                'username': username,
                'identity': identity,
                'account': account,
                'password': '',
                'user_status': user_status,
                'create_time': create_time,
                'login_time': login_time
            }
        })

# 获取登录的用户信息
@userapp.route('/api/user/getuserinfo/<user_id>', methods=['get'])
def getuserinfo(user_id):
    try:
        user_id = int(user_id)
    except Exception as e:
        user_id = 0
    if user_id == 0: return send_cc('无效参数')
    #
    username = ''
    account = ''
    identity = ''
    user_status = ''
    create_time = ''
    login_time = ''
    email = ''
    # 
    readlist = []
    #
    echarts_info = {}
    get_time_dict = {}
    # 
    reserve_info = FrontReserve.get_reserve_info(user_id)
    # 查询数据库
    find_userinfo = User.getuserinfo(user_id)
    if find_userinfo == {} or len(find_userinfo) < 1:
        return send_cc('用户id无效')
    else:
        # 用户信息
        username = find_userinfo['username']
        account = find_userinfo['account']
        identity = find_userinfo['identity']
        user_status = find_userinfo['user_status']
        create_time = find_userinfo['create_time']
        login_time = find_userinfo['login_time']
        email = find_userinfo['email']
        # 通知阅读列表
        readlist = User.get_read(user_id)
        # 图表数据
        echarts_info = User.get_echarts_info()
        # 预约时间段数据
        get_time_dict = User.get_time_dict()
        return send_data({
            'status': 0,
            'msg': '获取用户信息成功',
            'data': {
                'user_id': user_id,
                'username': username,
                'identity': identity,
                'account': account,
                'password': '',
                'email': email,
                'user_status': user_status,
                'create_time': create_time,
                'login_time': login_time
            },
            'readlist': readlist,
            'reserve_info': reserve_info,
            'echarts_info': echarts_info,
            'get_time_dict': get_time_dict
        })

# 用户修改密码
@userapp.route('/api/user/updatepwd', methods=['post'])
def update_pwd():
    # 获取客户端发来的表单信息
    userinfo = get_data(request.form)
    if userinfo == [] or userinfo == {} or userinfo == '' or len(userinfo) < 1:
        return send_cc('无效输入')
    user_id = 0
    oldpwd = ''
    newpwd = ''
    try:
        user_id = int(userinfo['user_id'])
        oldpwd = userinfo['oldpwd']
        newpwd = userinfo['newpwd']
    except Exception as e:
        user_id = 0
        oldpwd = ''
        newpwd = ''
    if user_id == 0 or oldpwd == '' or newpwd == '': return send_cc('无效输入')
    # 判断用户是否存在
    exist_user = User.exist_user(user_id)
    if exist_user == False: return send_cc('用户不存在')
    # 与数据库比较密码
    compare_pwd = User.compare_pwd(user_id, oldpwd)
    if compare_pwd == False: return send_cc('旧密码错误')
    # 与新密码比较
    if oldpwd == newpwd: return send_cc('新密码不能与旧密码相同')
    # 修改密码
    User.update_pwd(user_id, newpwd)
    return send_cc('密码修改成功, 请重新登录', 0)

# 用户设置/修改邮箱
@userapp.route('/api/user/setemail', methods=['post'])
def set_email():
    # 获取客户端发来的表单信息
    userinfo = get_data(request.form)
    if userinfo == [] or userinfo == {} or userinfo == '' or len(userinfo) < 1:
        return send_cc('无效输入')
    user_id = 0
    email = ''
    try:
        user_id = int(userinfo['user_id'])
        email = userinfo['email']
    except Exception as e:
        user_id = 0
        email = ''
    if user_id == 0 or email == '': return send_cc('无效输入')
    # 判断用户是否存在
    exist_user = User.exist_user(user_id)
    if exist_user == False: return send_cc('用户不存在')
    # 设置邮箱
    User.set_email(user_id, email)
    return send_cc('保存成功', 0)

# 用户提交问题反馈给开发者
@userapp.route('/api/user/sendfeedback', methods=['post'])
def send_feedback():
    # 获取客户端发来的表单信息
    reqinfo = get_data(request.form)
    if reqinfo == [] or reqinfo == {} or reqinfo == '' or len(reqinfo) < 1:
        return send_cc('无效输入')
    account = ''
    username = ''
    feedback_info = ''
    try:
        account = reqinfo['account']
        username = reqinfo['username']
        feedback_info = reqinfo['feedback_info']
    except Exception as e:
        account = ''
        username = ''
        feedback_info = ''
    if account == '' or username == '' or feedback_info == '': return send_cc('无效输入')
    # 判断账号和用户名是否存在
    exist_account_and_name = User.exist_account_and_name(account, username)
    if exist_account_and_name == False: return send_cc('用户不存在')
    # 邮件标题和邮件内容
    title = f'{username}的反馈信息'
    feedback_info = f""" 
    账号: {account},
    用户名: {username},
    反馈信息: {feedback_info}
    """
    # 发送邮件给开发者
    ret = mail(feedback_info, title)
    if ret: return send_cc('反馈已提交', 0)
    else: return send_cc('提交失败')

@userapp.route('/api/hello', methods=['get'])
def hello():
    return 'Hello'

# if __name__ == '__main__':
#     user_login()

