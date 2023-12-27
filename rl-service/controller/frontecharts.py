# 用户的基本操作，蓝图的定义，用户功能模块的定义
from flask import Blueprint, render_template, request
from config import get_data, send_cc, send_data, isVaildDate, user_status_true, user_status_false, user_status_all

from models.frontechartsmodel import FrontEcharts

frontechartsapp = Blueprint('frontechartsapp', __name__)



# 获取实验列表
@frontechartsapp.route('/api/front/echarts/getechartslist', methods=['post'])
def get_echarts():
    # 获取客户端发来的表单信息
    info = get_data(request.form)
    print(info)
    test_detail_id = 1
    episode_id = 1
    if isinstance(info, int):
        # 处理整数的情况
        print("info 是整数")
    elif isinstance(info, dict) or isinstance(info, object):
        # 处理对象的情况
        if 'test_detail_id' in info:

            test_detail_id = info['test_detail_id']
        if 'episode_id' in info:

            episode_id = info['episode_id']
    else:
        print("未知类型")

    # try:
    #     echarts_id = int(info)
    # except Exception as e:
    #     echarts_id = 0
    # if echarts_id == 0:
    #     return send_cc('无效参数')
    find_echartsinfo = FrontEcharts.get_echarts(test_detail_id,episode_id)
    print(find_echartsinfo)
    return send_data({'status': 0, 'msg': '查询数据成功', 'data': find_echartsinfo})

