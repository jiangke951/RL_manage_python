# 预约座位的基本操作
from flask import Blueprint, render_template, request
from config import get_data, send_cc, send_data, is_vaild_date, is_vaild_big15min


from models.frontreservemodel import FrontReserve
from models.usermodel import User
from models.frontseatmodel import FrontSeat

frontreserveapp = Blueprint('frontreserveapp', __name__)

# 预约座位
@frontreserveapp.route('/api/front/reserve/reserveseat', methods=['post'])
def reserve_seat():
    # 获取客户端发来的表单信息
    reqinfo = get_data(request.form)
    if reqinfo == [] or reqinfo == {} or reqinfo == '' or len(reqinfo) < 1:
        return send_cc('无效输入')
    user_id = 0
    seat_id = 0
    end_time = ''
    try:
        user_id = int(reqinfo['user_id'])
        seat_id = int(reqinfo['seat_id'])
        end_time = reqinfo['end_time']
    except Exception as e:
        user_id = 0
        seat_id = 0
        end_time = ''
    if user_id == 0 or seat_id == 0 or end_time == '': return send_cc('无效输入')
    # 判断用户是否存在
    exist_user = User.exist_user(user_id)
    if exist_user == False: return send_cc('用户不存在')
    # 判断座位是否存在
    exist_seat = FrontSeat.exist_seat(seat_id)
    if exist_seat == False: return send_cc('座位不存在')
    # 判断用户是否已经预约
    exist_reserve = FrontReserve.exist_reserve(user_id)
    if exist_reserve == True: return send_cc('请不要重复预约')
    # 判断时间格式
    if is_vaild_date(end_time) != True: return send_cc('时间格式不正确')
    # 时间应大于当前时间15分钟
    if is_vaild_big15min(end_time) == False: return send_cc('预约时间应不少于15分钟')
    # 预约座位
    FrontReserve.reserve_seat(user_id, seat_id, end_time)
    return send_cc('预约成功', 0)

# 获取预约信息
@frontreserveapp.route('/api/front/reserve/getreserveinfo/<user_id>', methods=['get'])
def get_reserve_info(user_id):
    try:
        user_id = int(user_id)
    except Exception as e:
        user_id = 0
    if user_id == 0: return send_cc('无效参数')
    # 判断用户是否存在
    exist_user = User.exist_user(user_id)
    if exist_user == False: return send_cc('用户不存在')
    # 获取预约信息
    reserve_info = FrontReserve.get_reserve_info(user_id)
    return send_data({'status': 0, 'msg': '获取预约信息成功', 'data': reserve_info})

# 离开座位
@frontreserveapp.route('/api/front/reserve/leaveseat/<user_id>/<seat_id>', methods=['get'])
def leave_seat(user_id, seat_id):
    try:
        user_id = int(user_id)
        seat_id = int(seat_id)
    except Exception as e:
        user_id = 0
        seat_id = 0
    if user_id == 0 or seat_id == 0: return send_cc('无效参数')
    # 判断用户是否存在
    exist_user = User.exist_user(user_id)
    if exist_user == False: return send_cc('用户不存在')
    # 判断座位是否存在
    exist_seat = FrontSeat.exist_seat(seat_id)
    if exist_seat == False: return send_cc('座位不存在')
    # 判断用户是否正在预约
    exist_reserve = FrontReserve.exist_reserve(user_id)
    if exist_reserve == False: return send_cc('没有预约记录')
    # 离开座位
    FrontReserve.leave_seat(user_id, seat_id)
    return send_cc('已离开座位', 0)
