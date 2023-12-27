from app import db
from config import get_cur_time, get_md5, user_status_true, user_status_false, user_status_all, user_identity_admin, user_identity_user, NoticeRead, NoticeConf, notice_isdel_no

# 后台用户表
class BackUser(db.Model):  # 创建的类对应数据库的表以及对表的相关操作
    __tablename__ = 'user'
    __table_args__ = {
        'autoload': True,
        'autoload_with': db.engine
    }

    @classmethod
    def exist_account(self, account):  # 判断是否已经存在当前账号
        query_user = db.session.query(BackUser)
        all_user = query_user.all()
        flag = False
        for user in all_user:
            if user.account == account:
                flag = True
                break
        return flag

    @classmethod
    def add_user(self, account, username, pwd, user_status): # 添加用户
        # 对密码进行加密
        pwd = get_md5(pwd)
        # 获取当前时间为创建时间
        create_time = get_cur_time()
        userinfo = BackUser(account=account, username=username,password=pwd,user_status=user_status,create_time=create_time)
        db.session.add(userinfo)
        db.session.commit()
        # 用户可以显示通知
        user = db.session.query(BackUser).filter(BackUser.identity==user_identity_user).filter(BackUser.account==account).first()
        notice = db.session.query(NoticeConf).filter(NoticeConf.is_delete==notice_isdel_no).all()
        for n in notice:
            nr = NoticeRead(user_id=user.id, notice_id=n.id)
            db.session.add(nr)
            db.session.commit()

    @classmethod
    def get_user_list(self, page_no, page_size, account, username, user_status): # 查询用户列表
        query_user = None
        if user_status == user_status_all:
            query_user = db.session.query(BackUser).filter(BackUser.identity==user_identity_user).filter(BackUser.account.like(f'%{account}%')).filter(BackUser.username.like(f'%{username}%')).order_by(BackUser.id.desc()).paginate(page=page_no, per_page=page_size).items
        else:
            query_user = db.session.query(BackUser).filter(BackUser.identity==user_identity_user).filter(BackUser.user_status == user_status).filter(BackUser.account.like(f'%{account}%')).filter(BackUser.username.like(f'%{username}%')).order_by(BackUser.id.desc()).paginate(page=page_no, per_page=page_size).items
        userlist = []
        login_time = ''
        for user in query_user:
            if user.login_time == None:
                login_time = '无登录记录'
            else: login_time = user.login_time
            userlist.append({'user_id': user.id, 'username': user.username, 'account': user.account, 'identity': user.identity, 'user_status': user.user_status, 'create_time': user.create_time, 'login_time': login_time})
        return userlist

    @classmethod
    def get_user_count(self, account, username, user_status): # 获取用户数量
        if user_status == user_status_all:
            query_user = db.session.query(BackUser).filter(BackUser.identity==user_identity_user).filter(BackUser.account.like(f'%{account}%')).filter(BackUser.username.like(f'%{username}%'))
        else:
            query_user = db.session.query(BackUser).filter(BackUser.identity==user_identity_user).filter(BackUser.account.like(f'%{account}%')).filter(BackUser.username.like(f'%{username}%')).filter(BackUser.user_status==user_status)
        all_user = query_user.all()
        userlist = []
        for user in all_user:
            if user.identity == user_identity_user:
                userlist.append(user.id)
        return len(userlist)

    @classmethod
    def exist_user(self, user_id):  # 判断是否存在用户
        query_user = db.session.query(BackUser)
        all_user = query_user.all()
        flag = False
        for user in all_user:
            if user.id == user_id and user.identity == user_identity_user:
                flag = True
                break
        return flag

    @classmethod
    def back_update_userinfo(self, user_id, pwd, user_status): # 修改用户信息
        user = db.session.query(BackUser).filter(BackUser.id == user_id).first()
        user.password = get_md5(pwd)
        user.user_status = user_status
        db.session.commit()
    
    @classmethod
    def back_update_user_status(self, user_id, user_status): # 修改用户状态
        user = db.session.query(BackUser).filter(BackUser.id == user_id).first()
        user.user_status = user_status
        db.session.commit()

    @classmethod
    def del_user(self, user_id): # 封禁用户
        user = db.session.query(BackUser).filter(BackUser.id == user_id).first()
        user.user_status = user_status_false
        db.session.commit()
    
    


