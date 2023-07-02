from app import db
from config import get_cur_time, notice_isdel_no, notice_isdel_yes, NoticeRead

# 前台通知表
class FrontNotice(db.Model):
    __tablename__ = 'notice'
    __table_args__ = {
        'autoload': True,
        'autoload_with': db.engine
    }

    @classmethod
    def get_notice_list(self, user_id): # 查询通知列表
        query_notice = db.session.query(FrontNotice).filter(FrontNotice.is_delete==notice_isdel_no).all()
        query_read = db.session.query(NoticeRead).filter(NoticeRead.user_id==user_id).all()
        noticelist = []
        for notice in query_notice:
            for read in query_read:
                if notice.id == read.notice_id:
                    noticelist.append({'notice_id': notice.id, 'notice_title': notice.notice_title, 'notice_detail': notice.notice_detail, 'create_time': notice.create_time, 'user_id': read.user_id, 'read_notice_id': read.notice_id, 'is_read': read.is_read})
                    break
        noticelist = noticelist[::-1]
        return noticelist

    @classmethod
    def exist_notice(self, notice_id): # 判断通知是否存在
        query_notice = db.session.query(FrontNotice).filter(FrontNotice.is_delete==notice_isdel_no).filter(FrontNotice.id==notice_id).first()
        if query_notice == None: return False
        else: return True
