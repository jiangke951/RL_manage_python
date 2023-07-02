from app import db
from config import get_cur_time, Seat, reserve_isdel_no, reserve_isdel_yes, seat_status_free, reserve_status_all, reserve_status_normal, reserve_status_out, is_vaild_timeout, seat_isdel_no

# 后台预约座位表
class BackReserve(db.Model):
    __tablename__ = 'reserve_seat'
    __table_args__ = {
        'autoload': True,
        'autoload_with': db.engine
    }

    @classmethod
    def get_reserve_list(self, page_no, page_size, account, seat_no, reserve_status): # 获取预约信息列表
        query_reserve = None
        reserve_list = []
        r_status = ''
        if reserve_status == reserve_status_all: # 全部
            query_reserve = db.session.query(BackReserve).filter(BackReserve.is_delete==reserve_isdel_no).filter(BackReserve.account.like(f'%{account}%')).filter(BackReserve.seat_no.like(f'%{seat_no}%')).order_by(BackReserve.id.desc()).paginate(page=page_no, per_page=page_size)
            for r in query_reserve:
                if is_vaild_timeout(r.end_time) == False: r_status = reserve_status_normal
                else: r_status = reserve_status_out
                reserve_list.append({'reserve_id': r.id, 'user_id': r.user_id, 'seat_id': r.seat_id, 'account': r.account, 'seat_no': r.seat_no, 'begin_time': r.begin_time, 'end_time': r.end_time, 'reserve_status': r_status})
        elif reserve_status == reserve_status_normal: # 正常
            query_reserve = db.session.query(BackReserve).filter(BackReserve.is_delete==reserve_isdel_no).filter(BackReserve.account.like(f'%{account}%')).filter(BackReserve.seat_no.like(f'%{seat_no}%')).filter(BackReserve.end_time>=get_cur_time()).order_by(BackReserve.id.desc()).paginate(page=page_no, per_page=page_size)
            for r in query_reserve:
                reserve_list.append({'reserve_id': r.id, 'user_id': r.user_id, 'seat_id': r.seat_id, 'account': r.account, 'seat_no': r.seat_no, 'begin_time': r.begin_time, 'end_time': r.end_time, 'reserve_status': reserve_status_normal})
        else:
            query_reserve = db.session.query(BackReserve).filter(BackReserve.is_delete==reserve_isdel_no).filter(BackReserve.account.like(f'%{account}%')).filter(BackReserve.seat_no.like(f'%{seat_no}%')).filter(BackReserve.end_time<get_cur_time()).order_by(BackReserve.id.desc()).paginate(page=page_no, per_page=page_size)
            for r in query_reserve:
                reserve_list.append({'reserve_id': r.id, 'user_id': r.user_id, 'seat_id': r.seat_id, 'account': r.account, 'seat_no': r.seat_no, 'begin_time': r.begin_time, 'end_time': r.end_time, 'reserve_status': reserve_status_out})
        return reserve_list

    @classmethod
    def get_reserve_count(self, account, seat_no, reserve_status): # 获取数量
        query_reserve = None
        reserve_list = []
        if reserve_status == reserve_status_all: # 全部
            query_reserve = db.session.query(BackReserve).filter(BackReserve.is_delete==reserve_isdel_no).filter(BackReserve.account.like(f'%{account}%')).filter(BackReserve.seat_no.like(f'%{seat_no}%'))
            for r in query_reserve:
                reserve_list.append(r.id)
        elif reserve_status == reserve_status_normal: # 正常
            query_reserve = db.session.query(BackReserve).filter(BackReserve.is_delete==reserve_isdel_no).filter(BackReserve.account.like(f'%{account}%')).filter(BackReserve.seat_no.like(f'%{seat_no}%')).filter(BackReserve.end_time>=get_cur_time())
            for r in query_reserve:
                reserve_list.append(r.id)
        else:
            query_reserve = db.session.query(BackReserve).filter(BackReserve.is_delete==reserve_isdel_no).filter(BackReserve.account.like(f'%{account}%')).filter(BackReserve.seat_no.like(f'%{seat_no}%')).filter(BackReserve.end_time<get_cur_time())
            for r in query_reserve:
                reserve_list.append(r.id)
        return len(reserve_list)

    @classmethod
    def exist_reserve(self, reserve_id): # 查询预约信息是否存在且超时
        query_reserve = db.session.query(BackReserve).filter(BackReserve.is_delete==reserve_isdel_no).filter(BackReserve.id==reserve_id).filter(BackReserve.end_time<get_cur_time()).first()
        if query_reserve == None: return False
        else: return True

    @classmethod
    def del_reserve(self, reserve_id, seat_id): # 删除预约信息
        reserve = db.session.query(BackReserve).filter(BackReserve.id == reserve_id).first()
        reserve.is_delete = reserve_isdel_yes
        db.session.commit()
        # 修改座位信息
        query_seat = db.session.query(Seat).filter(Seat.id==seat_id).first()
        query_seat.seat_status = seat_status_free
        db.session.commit()

    @classmethod
    def del_all_reserve(self): # 删除所有超时预约
        reserve = db.session.query(BackReserve).filter(BackReserve.is_delete==reserve_isdel_no).filter(BackReserve.end_time<get_cur_time()).first()
        if reserve == None: return 'ok'
        query_reserve = db.session.query(BackReserve).filter(BackReserve.is_delete==reserve_isdel_no).filter(BackReserve.end_time<get_cur_time()).all()
        seat_ids = []
        for r in query_reserve:
            seat_ids.append(r.seat_id)
            r.is_delete = reserve_isdel_yes
            db.session.commit()
        # 修改座位状态
        for si in seat_ids:
            query_seat = db.session.query(Seat).filter(Seat.is_delete==seat_isdel_no).filter(Seat.id==si).first()
            query_seat.seat_status = seat_status_free
            db.session.commit()

    @classmethod
    def query_all_exist_timeout_reserve(self): # 查询全部， 是否存在超时记录
        reserve = db.session.query(BackReserve).filter(BackReserve.is_delete==reserve_isdel_no).filter(BackReserve.end_time<get_cur_time()).first()
        if reserve == None: return False
        else: return True