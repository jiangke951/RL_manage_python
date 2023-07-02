from app import db
from config import get_cur_time, seat_isdel_no, Echarts

# 前台座位表
class FrontSeat(db.Model):
    __tablename__ = 'seat'
    __table_args__ = {
        'autoload': True,
        'autoload_with': db.engine
    }

    @classmethod
    def get_seat_list(self, seat_floor): # 获取座位列表
        # 搜索座位次数+1
        echarts = db.session.query(Echarts).first()
        echarts.search_seat_count = echarts.search_seat_count + 1
        db.session.commit()
        # 获取座位列表
        query_seat = None
        if seat_floor == 0:
            query_seat = db.session.query(FrontSeat).filter(FrontSeat.is_delete==seat_isdel_no).all()
        else:
            query_seat = db.session.query(FrontSeat).filter(FrontSeat.is_delete==seat_isdel_no).filter(FrontSeat.seat_no.like(f'%{str(seat_floor)}-%')).all()
        seatlist = []
        if query_seat == None: return []
        for seat in query_seat:
            seatlist.append({'seat_id': seat.id, 'seat_no': seat.seat_no, 'seat_status': seat.seat_status, 'seat_floor': seat.seat_no[:1]+'楼'})
        return seatlist

    @classmethod
    def exist_seat(self, seat_id): # 判断座位是否存在
        seat = db.session.query(FrontSeat).filter(FrontSeat.is_delete==seat_isdel_no).filter(FrontSeat.id==seat_id).first()
        if seat == None: return False
        else: return True
