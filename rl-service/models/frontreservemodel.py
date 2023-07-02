from app import db
from config import get_cur_time, User, Echarts, Seat, reserve_isdel_no, reserve_isdel_yes, seat_status_use, seat_status_free

# 前台预约座位表
class FrontReserve(db.Model):
    __tablename__ = 'reserve_seat'
    __table_args__ = {
        'autoload': True,
        'autoload_with': db.engine
    }

    @classmethod
    def reserve_seat(self, user_id, seat_id, end_time): # 预约座位
        # 获取当前时间
        begin_time = get_cur_time()
        # 根据用户id获取用户账号
        account = db.session.query(User).filter(User.id==user_id).first().account
        # 获取座位编号
        seat_no = db.session.query(Seat).filter(Seat.id==seat_id).first().seat_no
        # 插入预约信息
        reserve = FrontReserve(user_id=user_id, seat_id=seat_id,begin_time=begin_time,end_time=end_time,account=account,seat_no=seat_no)
        db.session.add(reserve)
        db.session.commit()
        # 修改座位的使用次数和座位状态
        seat = db.session.query(Seat).filter(Seat.id == seat_id).first()
        seat.use_count = seat.use_count + 1
        seat.seat_status = seat_status_use
        db.session.commit()
        # 修改楼层座位使用情况
        echarts = db.session.query(Echarts).first()
        seat_floor = int(seat_no[:1])
        if seat_floor == 1:
            echarts.one_floor_count = echarts.one_floor_count + 1
            db.session.commit()
        elif seat_floor == 2:
            echarts.two_floor_count = echarts.two_floor_count + 1
            db.session.commit()
        elif seat_floor == 3:
            echarts.three_floor_count = echarts.three_floor_count + 1
            db.session.commit()
        elif seat_floor == 4:
            echarts.four_floor_count = echarts.four_floor_count + 1
            db.session.commit()
        elif seat_floor == 5:
            echarts.five_floor_count = echarts.five_floor_count + 1
            db.session.commit()
        # 修改预约时间段次数情况
        m_time = str(begin_time[11:13])
        if m_time == '09':
            echarts.nine_time_count = echarts.nine_time_count + 1
            db.session.commit()
        elif m_time == '10':
            echarts.ten_time_count = echarts.ten_time_count + 1
            db.session.commit()
        elif m_time == '11':
            echarts.eleven_time_count = echarts.eleven_time_count + 1
            db.session.commit()
        elif m_time == '12':
            echarts.twelve_time_count = echarts.twelve_time_count + 1
            db.session.commit()
        elif m_time == '13':
            echarts.thirteen_time_count = echarts.thirteen_time_count + 1
            db.session.commit()
        elif m_time == '14':
            echarts.fourteen_time_count = echarts.fourteen_time_count + 1
            db.session.commit()
        elif m_time == '15':
            echarts.fifteen_time_count = echarts.fifteen_time_count + 1
            db.session.commit()
        elif m_time == '16':
            echarts.sixteen_time_count = echarts.sixteen_time_count + 1
            db.session.commit()
        elif m_time == '17':
            echarts.seventeen_time_count = echarts.seventeen_time_count + 1
            db.session.commit()
        elif m_time == '18':
            echarts.eighteen_time_count = echarts.eighteen_time_count + 1
            db.session.commit()
        elif m_time == '19':
            echarts.nineteen_time_count = echarts.nineteen_time_count + 1
            db.session.commit()
        elif m_time == '20':
            echarts.twenty_time_count = echarts.twenty_time_count + 1
            db.session.commit()
        elif m_time == '21':
            echarts.twenty_one_time_count = echarts.twenty_one_time_count + 1
            db.session.commit()



    @classmethod
    def exist_reserve(self, user_id): # 判断用户是否已经预约
        query_reserve = db.session.query(FrontReserve).filter(FrontReserve.is_delete==reserve_isdel_no).filter(FrontReserve.user_id==user_id).first()
        if query_reserve == None: return False
        else: return True

    @classmethod
    def get_reserve_info(self, user_id): # 获取用户预约信息
        query_reserve = db.session.query(FrontReserve).filter(FrontReserve.is_delete==reserve_isdel_no).filter(FrontReserve.user_id==user_id).first()
        if query_reserve == None: return {}
        reserve_id = query_reserve.id
        seat_id = query_reserve.seat_id
        begin_time = query_reserve.begin_time
        end_time = query_reserve.end_time
        seat_no = query_reserve.seat_no
        # 座位楼层
        seat_floor = seat_no[:1] + '楼'
        return {'reserve_id': reserve_id, 'user_id': user_id, 'seat_id': seat_id, 'begin_time': begin_time, 'end_time': end_time, 'seat_no': seat_no, 'seat_floor': seat_floor}
    
    @classmethod
    def leave_seat(self, user_id, seat_id): # 离开座位
        query_reserve = db.session.query(FrontReserve).filter(FrontReserve.is_delete==reserve_isdel_no).filter(FrontReserve.user_id==user_id).filter(FrontReserve.seat_id==seat_id).first()
        query_reserve.is_delete = reserve_isdel_yes
        db.session.commit()
        # 修改座位信息
        query_seat = db.session.query(Seat).filter(Seat.id==seat_id).first()
        query_seat.seat_status = seat_status_free
        db.session.commit()
