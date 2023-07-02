# 座位的基本操作
from flask import Blueprint, render_template, request
from config import get_data, send_cc, send_data, isVaildDate, seat_status_use, seat_status_free, seat_status_all


from models.frontseatmodel import FrontSeat
from models.usermodel import User

frontseatapp = Blueprint('frontseatapp', __name__)


# 获取座位列表
@frontseatapp.route('/api/front/seat/getseatlist/<seat_floor>', methods=['get'])
def get_seat_list(seat_floor):
    try:
        seat_floor = int(seat_floor)
    except Exception as e:
        seat_floor = 0
    # 获取座位列表
    seatlist = FrontSeat.get_seat_list(seat_floor)
    return send_data({'status': 0, 'msg': '获取座位列表成功', 'data': seatlist})