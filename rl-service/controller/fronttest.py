# 用户的基本操作，蓝图的定义，用户功能模块的定义
from flask import Blueprint, render_template, request
from config import get_data, send_cc, send_data, isVaildDate, user_status_true, user_status_false, user_status_all
from models.backusermodel import BackUser

from models.fronttestmodel import FrontTest

from models.testdetailmodel import TestDetail
fronttestapp = Blueprint('fronttestapp', __name__)


# 添加实验
@fronttestapp.route('/api/front/test/addtest', methods=['post'])
def add_test():
    # return '124'
    testinfo = get_data(request.form)
    if testinfo == [] or testinfo == {} or testinfo == '' or len(testinfo) < 1:
        return send_cc('无效1111输入')
    try:
        test_name = testinfo['account']
        user_name = testinfo['username']
        test_status = testinfo['test_status']
        create_name = testinfo['create_name']
    except Exception as e:
        test_name = ''
        user_name = ''
        test_status = ''
        create_name = ''
    if test_name == '' or user_name == '' or test_status == '':
        return send_cc('无效输入')
    # return testinfo
    # 添加用户
    FrontTest.add_test(test_name, user_name, test_status,create_name)
    return send_cc('创建实验成功', 0)

# 获取实验列表
@fronttestapp.route('/api/front/test/gettestlist', methods=['post'])
def get_test_list():

    # 获取客户端发来的表单信息
    info = get_data(request.form)

    if info == [] or info == {} or info == '' or len(info) < 1:
        return send_cc('无效输入')
    try:
        page_no = int(info['page_no'])
        page_size = int(info['page_size'])
        test_name = info['account']
        user_name = info['username']
        test_status = info['test_status']
        # test_status = ''
    except Exception as e:
        page_no = 0
        page_size = 0
        test_name = ''
        user_name = ''
        test_status = ''
    if page_no == 0 or page_size == 0: return send_cc('无效参数')

    # 查询实验列表
    testlist = FrontTest.get_test_list(page_no, page_size, test_name, user_name, test_status)
    # print(testlist)
    # 获取全部用户数量
    test_count = FrontTest.get_test_count(test_name, user_name, test_status)
    return send_data({'status': 0, 'msg': '查询实验列表成功', 'data': testlist, 'test_count': test_count})

# 修改实验信息
@fronttestapp.route('/api/front/test/updatetestinfo', methods=['post'])
def updatetestinfo():
    # 获取客户端发来的表单信息

    testinfo = get_data(request.form)
    # print(testinfo)
    if testinfo == [] or testinfo == {} or testinfo == '' or len(testinfo) < 1:
        return send_cc('无效输入')
    test_id = 0
    test_name = ''
    user_name = ''
    test_status =  ''
    try:
        test_id = int(testinfo['test_id'])
        test_name = testinfo['test_name']
        user_name = testinfo['user_name']
        test_status = testinfo['test_status']
    except Exception as e:
        test_id = 0
        test_name = ''
        user_name = ''
        test_status =''
    if test_status == '' or test_id == 0:
        return send_cc('无效输入')

    FrontTest.updatetestinfo(test_id, test_name,user_name,test_status)

    return send_cc('实验信息修改成功', 0)
# 获取实验列表
@fronttestapp.route('/api/front/test/gettestDetail', methods=['post'])
def get_test_detail():
    # 获取客户端发来的表单信息

    info = get_data(request.form)
    print(info)
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
        test_name = info['account']
        user_name = info['username']
        test_status = info['test_status']
        parent_id = info['parent_id']
    except Exception as e:
        page_no = 0
        page_size = 0
        test_name = ''
        user_name = ''
        test_status = ''
        parent_id = ''
    if page_no == 0 or page_size == 0: return send_cc('无效参数')
    # 查询实验列表
    testlist = TestDetail().get_test_detail(page_no, page_size, test_name, user_name, test_status, parent_id)
    print(testlist)
    # 获取全部用户数量
    test_count = FrontTest.get_test_count(test_name, user_name, test_status)
    return send_data({'status': 0, 'msg': '查询实验列表成功', 'data': testlist, 'test_count': test_count})

@fronttestapp.route('/api/front/test/sendForm', methods=['post'])
def send_form():
    # 获取客户端发来的表单信息
    print("724")
    file = request.files['file']
    print(file)
    return send_data({'status': 0, 'msg': '成功'})

    # return send_data({'status': 0, 'msg': '成功', 'data': testlist, 'test_count': test_count})
