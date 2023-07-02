from app import db
from config import get_cur_time, get_md5, seat_status_use, seat_status_free, seat_status_all, seat_isdel_no, seat_isdel_yes, ReserveConf, reserve_isdel_yes, reserve_isdel_no

# 后台座位表
class BackSeat(db.Model):
    __tablename__ = 'seat'
    __table_args__ = {
        'autoload': True,
        'autoload_with': db.engine
    }

    @classmethod
    def exist_seat_no(self, seat_no):  # 判断是否已经存在当前座位编号
        query_seat = db.session.query(BackSeat).filter(BackSeat.is_delete==seat_isdel_no).filter(BackSeat.seat_no==seat_no).first()
        if query_seat == None: return False
        else: return True
    
    @classmethod
    def add_seat(self, seat_no): # 添加座位
        create_time = get_cur_time()
        info = BackSeat(seat_no=seat_no, create_time=create_time)
        db.session.add(info)
        db.session.commit()

    @classmethod
    def get_seat_list(self, page_no, page_size, seat_no, seat_status): # 查询座位列表
        query_seat = None
        if seat_status == seat_status_all:
            query_seat = db.session.query(BackSeat).filter(BackSeat.is_delete==seat_isdel_no).filter(BackSeat.seat_no.like(f'%{seat_no}%')).order_by(BackSeat.id.desc()).paginate(page=page_no, per_page=page_size)
        else:
            query_seat = db.session.query(BackSeat).filter(BackSeat.is_delete==seat_isdel_no).filter(BackSeat.seat_no.like(f'%{seat_no}%')).filter(BackSeat.seat_status == seat_status).order_by(BackSeat.id.desc()).paginate(page=page_no, per_page=page_size)
        seatlist = []
        for seat in query_seat:
            seatlist.append({'seat_id': seat.id, 'seat_no': seat.seat_no, 'seat_status': seat.seat_status, 'use_count': seat.use_count, 'create_time': seat.create_time})
        return seatlist

    @classmethod
    def get_seat_count(self, seat_no, seat_status): # 获取座位数量
        query_seat = None
        if seat_status == seat_status_all:
            query_seat = db.session.query(BackSeat).filter(BackSeat.is_delete==seat_isdel_no).filter(BackSeat.seat_no.like(f'%{seat_no}%'))
        else:
            query_seat = db.session.query(BackSeat).filter(BackSeat.is_delete==seat_isdel_no).filter(BackSeat.seat_no.like(f'%{seat_no}%')).filter(BackSeat.seat_status == seat_status)
        all_seat = query_seat.all()
        seatlist = []
        for seat in all_seat:
            seatlist.append(seat.id)
        return len(seatlist)

    @classmethod
    def exist_seat(self, seat_id): # 判断座位是否存在
        query_seat = db.session.query(BackSeat).filter(BackSeat.is_delete==seat_isdel_no).filter(BackSeat.id==seat_id).first()
        if query_seat == None: return False
        else: return True
    
    @classmethod
    def back_update_seatinfo(self, seat_id, seat_no): # 修改座位信息
        seat = db.session.query(BackSeat).filter(BackSeat.id == seat_id).first()
        seat.seat_no = seat_no
        db.session.commit()
        # 修改对应预约信息
        reserve = db.session.query(ReserveConf).filter(ReserveConf.seat_id==seat_id).filter(ReserveConf.is_delete==reserve_isdel_no).first()
        if reserve == None: return
        reserve.seat_no = seat_no
        db.session.commit()

    @classmethod
    def del_seat(self, seat_id): # 移除座位
        seat = db.session.query(BackSeat).filter(BackSeat.id==seat_id).first()
        seat.is_delete = seat_isdel_yes
        db.session.commit()
        # 删除相关预约信息
        reserve = db.session.query(ReserveConf).filter(ReserveConf.seat_id==seat_id).filter(ReserveConf.is_delete==reserve_isdel_no).first()
        if reserve == None: return
        reserve.is_delete = reserve_isdel_yes
        db.session.commit()

