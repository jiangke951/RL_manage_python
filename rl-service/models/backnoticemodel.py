from app import db
from config import get_cur_time, notice_isdel_no, notice_isdel_yes, NoticeRead, User, user_identity_user

# 后台通知表
class BackNotice(db.Model):
    __tablename__ = 'notice'
    __table_args__ = {
        # 'autoload': True,
        'autoload_with': db.engine
    }

    @classmethod
    def exist_notice_title(self, notice_title): # 是否存在通知标题
        query_notice = db.session.query(BackNotice).filter(BackNotice.is_delete==notice_isdel_no).filter(BackNotice.notice_title==notice_title).first()
        if query_notice == None: return False
        else: return True

    @classmethod
    def add_notice(self, notice_title, notice_detail): # 发布通知
        create_time = get_cur_time()
        notice = BackNotice(notice_title=notice_title,notice_detail=notice_detail,create_time=create_time)
        db.session.add(notice)
        db.session.commit()
        notice_id = db.session.query(BackNotice).order_by(BackNotice.id.desc()).first().id
        query_user = db.session.query(User).filter(User.identity==user_identity_user).all()
        if query_user == None: return
        for user in query_user:
            nr = NoticeRead(user_id=user.id, notice_id=notice_id)
            db.session.add(nr)
            db.session.commit()

    @classmethod
    def get_notice_list(self, page_no, page_size, notice_title): # 查询通知列表
        query_notice = db.session.query(BackNotice).filter(BackNotice.is_delete==notice_isdel_no).filter(BackNotice.notice_title.like(f'%{notice_title}%')).order_by(BackNotice.id.desc()).paginate(page=page_no, per_page=page_size).items
        noticelist = []
        for notice in query_notice:
            noticelist.append({'notice_id': notice.id, 'notice_title': notice.notice_title, 'notice_detail': notice.notice_detail, 'create_time': notice.create_time})
        return noticelist

    @classmethod
    def get_notice_count(self, notice_title): # 获取通知数量
        query_notice = db.session.query(BackNotice).filter(BackNotice.is_delete==notice_isdel_no).filter(BackNotice.notice_title.like(f'%{notice_title}%'))
        all_notice = query_notice.all()
        noticelist = []
        for notice in all_notice:
            noticelist.append(notice.id)
        return len(noticelist)

    @classmethod
    def exist_notice(self, notice_id): # 判断通知是否存在
        query_notice = db.session.query(BackNotice).filter(BackNotice.is_delete==notice_isdel_no).filter(BackNotice.id==notice_id).first()
        if query_notice == None: return False
        else: return True

    @classmethod
    def del_notice(self, notice_id): # 删除通知
        notice = db.session.query(BackNotice).filter(BackNotice.id==notice_id).first()
        notice.is_delete = notice_isdel_yes
        db.session.commit()
        query_user = db.session.query(User).filter(User.identity==user_identity_user).all()
        if query_user == None: return
        for user in query_user:
            nr = db.session.query(NoticeRead).filter(NoticeRead.user_id==user.id).filter(NoticeRead.notice_id==notice_id).first()
            if nr == None: break
            db.session.delete(nr)
            db.session.commit()


