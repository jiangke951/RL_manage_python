from app import db
from config import get_cur_time

# 前台通知表
class FrontRead(db.Model):
    __tablename__ = 'notice_read'
    __table_args__ = {
        'autoload': True,
        'autoload_with': db.engine
    }

    @classmethod
    def set_read(self, user_id, notice_id): # 设置阅读字段为已读
        read = db.session.query(FrontRead).filter(FrontRead.user_id==user_id).filter(FrontRead.notice_id==notice_id).first()
        if read != None:
            read.is_read = '已读'
            db.session.commit()

    @classmethod
    def all_set_read(self, user_id): # 设置该用户全部通知为已读
        query_read = db.session.query(FrontRead).filter(FrontRead.user_id==user_id).all()
        if query_read != None:
            for read in query_read:
                read.is_read = '已读'
                db.session.commit()
