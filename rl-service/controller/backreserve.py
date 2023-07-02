# 预约座位的基本操作
from flask import Blueprint, request
from config import get_data, send_cc, send_data, reserve_status_normal, reserve_status_out, reserve_status_all


from models.backreservemodel import BackReserve
from models.backseatmodel import BackSeat

backreserveapp = Blueprint('backreserveapp', __name__)

# 获取预约信息列表
@backreserveapp.route('/api/back/reserve/getreservelist', methods=['post'])
def get_reserve_list():
    # 获取客户端发来的表单信息
    reqinfo = get_data(request.form)
    if reqinfo == [] or reqinfo == {} or reqinfo == '' or len(reqinfo) < 1:
        return send_cc('无效输入')
    page_no = 0
    page_size = 0
    account = ''
    seat_no = ''
    reserve_status = ''
    try:
        page_no = int(reqinfo['page_no'])
        page_size = int(reqinfo['page_size'])
        account = reqinfo['account']
        seat_no = reqinfo['seat_no']
        reserve_status = reqinfo['reserve_status']
    except Exception as e:
        page_no = 0
        page_size = 0
        account = ''
        seat_no = ''
        reserve_status = ''
    if page_no == 0 or page_size == 0: return send_cc('无效参数')
    if reserve_status != reserve_status_normal and reserve_status != reserve_status_out and reserve_status != reserve_status_all: return send_cc('请选择预约状态')
    # 获取预约列表
    reserve_list = BackReserve.get_reserve_list(page_no,page_size,account,seat_no,reserve_status)
    # 获取数量
    reserve_count = BackReserve.get_reserve_count(account, seat_no, reserve_status)
    # 发送
    return send_data({'status': 0, 'msg': '查询预约信息列表成功', 'data': reserve_list, 'reserve_count': reserve_count})

# 删除超时的预约信息
@backreserveapp.route('/api/back/reserve/delreserve/<reserve_id>/<seat_id>', methods=['get'])
def del_reserve(reserve_id, seat_id):
    try:
        reserve_id = int(reserve_id)
        seat_id = int(seat_id)
    except Exception as e:
        reserve_id = 0
        seat_id = 0
    if reserve_id == 0 or seat_id == 0: return send_cc('无效参数')
    # 查询座位是否存在
    exist_seat = BackSeat.exist_seat(seat_id)
    if exist_seat == False: return send_cc('座位不存在')
    # 查询预约信息是否存在 且超时
    exist_reserve = BackReserve.exist_reserve(reserve_id)
    if exist_reserve == False: return send_cc('预约信息不存在或尚未超时')
    # 删除预约信息
    BackReserve.del_reserve(reserve_id, seat_id)
    return send_cc('预约信息删除成功, 座位已被释放', 0)

# 删除全部的超时预约
@backreserveapp.route('/api/back/reserve/delallreserve', methods=['get'])
def del_all_reserve():
    # 查询是否存在超时预约
    query_all_exist_timeout_reserve = BackReserve.query_all_exist_timeout_reserve()
    if query_all_exist_timeout_reserve == False: return send_cc('没有超时记录')
    # 删除
    BackReserve.del_all_reserve()
    return send_cc('超时记录已清空', 0)

