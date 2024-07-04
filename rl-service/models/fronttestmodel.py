from app import db
from config import get_cur_time, get_md5, test_status_true, test_status_false, test_status_all, user_identity_admin, user_identity_user, NoticeRead, NoticeConf, notice_isdel_no
from datetime import datetime
# 后台用户表
class FrontTest(db.Model):  # 创建的类对应数据库的表以及对表的相关操作
    __tablename__ = 'test'
    __table_args__ = {
        # 'autoload': True,
        'autoload_with': db.engine
    }


    @classmethod
    def add_test(self, test_name, user_name, test_status, create_name ): # 添加实验
        # 获取当前时间为创建时间
        create_time = get_cur_time()
        update_time = create_time
        testinfo = FrontTest(test_name=test_name, user_name=user_name,test_status=test_status,create_time=create_time,update_time=update_time, create_name = create_name)
        db.session.add(testinfo)
        db.session.commit()


    @classmethod
    def get_test_list(self, page_no, page_size, test_name, user_name, test_status): # 查询实验列表
        query_test = None


        query_test = db.session.query(FrontTest).filter(FrontTest.test_status == test_status).filter(FrontTest.user_name.like(f'%{user_name}%')).filter(FrontTest.test_name.like(f'%{test_name}%')).order_by(FrontTest.id.desc()).paginate(page=page_no, per_page=page_size).items
        testlist = []
        login_time = ''
        # print(query_test)
        for test in query_test:
            create_time = test.create_time.strftime("%Y-%m-%d %H:%M:%S")
            # testlist.append({'test_id': test.id, 'user_name': test.user_name, 'test_name': test.test_name, 'test_status': test.test_status, 'create_time': create_time,'seed': test.seed,'env_id': test.env_id,'learning_rate': test.learning_rate,'input_size': test.input_size,'info': test.info})
            testlist.append({'test_id': test.id, 'user_name': test.user_name, 'test_name': test.test_name, 'test_status': test.test_status, 'create_time': create_time, 'hyperparameters': test.hyperparameters})

        # print(testlist)
        return testlist

    @classmethod
    def get_test_count(self, test_name, user_name, test_status): # 获取实验数量
        query_test = None
        if test_status == test_status_all:
            query_test = db.session.query(FrontTest).filter(FrontTest.test_name.like(f'%{test_name}%')).filter(
                FrontTest.user_name.like(f'%{user_name}%'))
        else:
            query_test = db.session.query(FrontTest).filter(FrontTest.test_status == test_status).filter(
                FrontTest.user_name.like(f'%{user_name}%')).filter(FrontTest.test_name.like(f'%{test_name}%'))
        testlist = []
        login_time = ''
        for test in query_test:
            testlist.append({'test_id': test.id, 'user_name': test.user_name, 'test_name': test.test_name,
                             'test_status': test.test_status, 'create_time': test.create_time})

        return len(testlist)

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
    def updatetestinfo(self, test_id, test_name,user_name,test_status): # 修改实验信息
        test = db.session.query(FrontTest).filter(FrontTest.id == test_id).first()
        test.test_name = test_name
        test.user_name = user_name
        test.test_status = test_status
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



