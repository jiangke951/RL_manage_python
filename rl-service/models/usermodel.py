from app import db
from config import get_cur_time, get_md5,user_status_true,user_status_false, NoticeRead, Echarts

# 用户表
class User(db.Model):  # 创建的类对应数据库的表以及对表的相关操作
    __tablename__ = 'user'
    __table_args__ = {
        'autoload': True,
        'autoload_with': db.engine
    }

    @classmethod
    def user_login(self, account, pwd):  # 用户登录
        query_user = db.session.query(User)
        all_user = query_user.all()

        flag = False
        user_id = 0
        username = ''
        identity = ''
        user_status = ''
        create_time = ''
        # return all_user
        for user in all_user:
            if user.account == account and user.password == get_md5(pwd):
                user_id = user.id
                username = user.username
                identity = user.identity
                user_status = user.user_status
                create_time = user.create_time
                break
        if user_status != user_status_true: return {}
        flag = True
        if flag == True:
            flag = False
            login_time = get_cur_time()
            # 更新用户登录时间
            user = db.session.query(User).filter(User.account == account).first()
            user.login_time = login_time
            db.session.commit()
            return {'user_id': user_id, 'username': username, 'identity': identity, 'user_status': user_status, 'create_time': create_time, 'login_time': login_time}
        else:
            return {}

    @classmethod
    def getuserinfo(self, user_id): # 获取用户信息
        query_user = db.session.query(User)
        all_user = query_user.all()
        flag = False
        username = ''
        account = ''
        identity = ''
        user_status = ''
        create_time = ''
        login_time = ''
        email = ''
        for user in all_user:
            if user.id == user_id and user.user_status == user_status_true:
                flag = True
                username = user.username
                account = user.account
                identity = user.identity
                user_status = user.user_status
                create_time = user.create_time
                login_time = user.login_time
                if user.email == None: email = '未绑定邮箱'
                else: email = user.email
                break
        if flag == True:
            flag = False
            return {'username': username, 'account': account, 'identity': identity, 'user_status': user_status, 'create_time': create_time, 'login_time': login_time, 'email': email}
        else:
            return {}

    @classmethod
    def compare_pwd(self, user_id, oldpwd): # 比较密码
        query_user = db.session.query(User).filter(User.id == user_id).first()
        if query_user.password == get_md5(oldpwd):
            return True
        else:
            return False

    @classmethod
    def exist_user(self, user_id):  # 判断用户是否存在
        query_user = db.session.query(User)
        all_user = query_user.all()
        flag = False
        for user in all_user:
            if user.id == user_id and user.user_status == user_status_true:
                flag = True
                break
        return flag

    @classmethod
    def update_pwd(self, user_id, newpwd): # 修改密码
        user = db.session.query(User).filter(User.id == user_id).first()
        user.password = get_md5(newpwd)
        db.session.commit()

    @classmethod
    def set_email(self, user_id, email): # 设置邮箱
        user = db.session.query(User).filter(User.id == user_id).first()
        user.email = email
        db.session.commit()

    @classmethod
    def get_read(self, user_id): # 获取通知阅读列表
        query_nr = db.session.query(NoticeRead).filter(NoticeRead.user_id==user_id).filter(NoticeRead.is_read=='未读').all()
        if query_nr == None: return []
        readlist = []
        for r in query_nr:
            readlist.append({'read_id': r.id, 'user_id': r.user_id, 'notice_id': r.notice_id})
        return readlist

    @classmethod
    def exist_account_and_name(self, account, username): # 判断账号和用户名是否存在
        query_user = db.session.query(User).filter(User.user_status==user_status_true).filter(User.account==account).filter(User.username==username).first()
        if query_user == None: return False
        else: return True

    @classmethod
    def add_login_count(self): # 访问量加1
        echarts = db.session.query(Echarts).first()
        echarts.login_count = echarts.login_count + 1
        db.session.commit()

    @classmethod
    def get_echarts_info(self): # 获取图表情况
        echarts = db.session.query(Echarts).first()
        return {
                'search_seat_count': echarts.search_seat_count,
                'login_count': echarts.login_count,
                'one_floor_count': echarts.one_floor_count,
                'two_floor_count': echarts.two_floor_count,
                'three_floor_count': echarts.three_floor_count,
                'four_floor_count': echarts.four_floor_count,
                'five_floor_count': echarts.five_floor_count,
                'nine_time_count': echarts.nine_time_count,
                'ten_time_count': echarts.ten_time_count,
                'eleven_time_count': echarts.eleven_time_count,
                'twelve_time_count' :echarts.twelve_time_count,
                'thirteen_time_count' :echarts.thirteen_time_count,
                'fourteen_time_count': echarts.fourteen_time_count,
                'fifteen_time_count' :echarts.fifteen_time_count,
                'sixteen_time_count': echarts.sixteen_time_count,
                'seventeen_time_count': echarts.seventeen_time_count,
                'eighteen_time_count': echarts.eighteen_time_count,
                'nineteen_time_count': echarts.nineteen_time_count,
                'twenty_time_count': echarts.twenty_time_count,
                'twenty_one_time_count': echarts.twenty_one_time_count
            }

    @classmethod
    def get_time_dict(self): # 获取预约时间段次数
        echarts = db.session.query(Echarts).first()
        return {
                '9点': echarts.nine_time_count,
                '10点': echarts.ten_time_count,
                '11点': echarts.eleven_time_count,
                '12点' :echarts.twelve_time_count,
                '13点' :echarts.thirteen_time_count,
                '14点': echarts.fourteen_time_count,
                '15点' :echarts.fifteen_time_count,
                '16点': echarts.sixteen_time_count,
                '17点': echarts.seventeen_time_count,
                '18点': echarts.eighteen_time_count,
                '19点': echarts.nineteen_time_count,
                '20点': echarts.twenty_time_count,
                '21点': echarts.twenty_one_time_count
            }