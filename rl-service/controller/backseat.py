# 座位的基本操作
from flask import Blueprint, render_template, request
from config import get_data, send_cc, send_data, isVaildDate, seat_status_use, seat_status_free, seat_status_all


from models.backseatmodel import BackSeat

backseatapp = Blueprint('backseatapp', __name__)

# 添加座位
# @backseatapp.route('/api/back/seat/addseat', methods=['post'])
# @backseatapp.route('/api/front/test/addtest', methods=['post'])
def add_seat():
    # 获取客户端发来的表单信息
    reqinfo = get_data(request.form)
    if reqinfo == [] or reqinfo == {} or reqinfo == '' or len(reqinfo) < 1:
        return send_cc('无效输入')
    seat_no = ''
    try:
        seat_no = reqinfo['seat_no']
    except Exception as e:
        seat_no = ''
    if seat_no == '': return send_cc('无效输入')
    # 查询数据库是否存在座位编号
    exist_seat_no = BackSeat.exist_seat_no(seat_no)
    if exist_seat_no == True: return send_cc('座位编号已被占用')
    # 添加座位
    BackSeat.add_seat(seat_no)
    return send_cc('座位添加成功', 0)

# 列表显示座位
@backseatapp.route('/api/back/seat/getseatlist', methods=['post'])
def get_seat_list():
    # 获取客户端发来的表单信息
    info = get_data(request.form)
    if info == [] or info == {} or info == '' or len(info) < 1:
        return send_cc('无效输入')
    page_no = 0
    page_size = 0
    seat_no = ''
    seat_status = ''
    try:
        page_no = int(info['page_no'])
        page_size = int(info['page_size'])
        seat_no = info['seat_no']
        seat_status = info['seat_status']
    except Exception as e:
        page_no = 0
        page_size = 0
        seat_no = ''
        seat_status = ''
    if page_no == 0 or page_size == 0: return send_cc('无效参数')
    if seat_status != seat_status_use and seat_status != seat_status_free and seat_status != seat_status_all: return send_cc('请选择座位状态')
    # 查询座位列表
    seatlist = BackSeat.get_seat_list(page_no, page_size, seat_no, seat_status)
    # 获取全部座位数量
    seat_count = BackSeat.get_seat_count(seat_no, seat_status)
    return send_data({'status': 0, 'msg': '查询座位列表成功', 'data': seatlist, 'seat_count': seat_count})

# 修改座位信息
@backseatapp.route('/api/back/seat/updateseatinfo', methods=['post'])
def back_update_seatinfo():
    # 获取客户端发来的表单信息
    reqinfo = get_data(request.form)
    if reqinfo == [] or reqinfo == {} or reqinfo == '' or len(reqinfo) < 1:
        return send_cc('无效输入')
    seat_id = 0
    seat_no = ''
    try:
        seat_id = int(reqinfo['seat_id'])
        seat_no = reqinfo['seat_no']
    except Exception as e:
        seat_id = 0
        seat_no = ''
    if seat_id == 0: return send_cc('无效输入')
    # 查询数据库是否存在该座位
    exist_seat = BackSeat.exist_seat(seat_id)
    if exist_seat == False: return send_cc('座位不存在')
    # 查询座位编号是否存在
    exist_seat_no = BackSeat.exist_seat_no(seat_no)
    if exist_seat_no == True: return send_cc('座位编号已被占用')
    # 修改座位信息
    BackSeat.back_update_seatinfo(seat_id, seat_no)
    return send_cc('修改成功', 0)

# 移除座位
@backseatapp.route('/api/back/seat/delseat/<seat_id>', methods=['get'])
def del_seat(seat_id):
    try:
        seat_id = int(seat_id)
    except Exception as e:
        seat_id = 0
    if seat_id == 0: return send_cc('无效参数')
    # 查询座位是否存在
    exist_seat = BackSeat.exist_seat(seat_id)
    if exist_seat == False: return send_cc('座位不存在')
    # 移除座位
    BackSeat.del_seat(seat_id)
    return send_cc('座位已被移除!', 0)


