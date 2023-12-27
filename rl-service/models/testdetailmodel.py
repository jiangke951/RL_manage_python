from app import db
from config import get_cur_time, get_md5, test_status_true, test_status_false, test_status_all, user_identity_admin, user_identity_user, NoticeRead, NoticeConf, notice_isdel_no
from datetime import datetime
# 后台用户表
class TestDetail(db.Model):  # 创建的类对应数据库的表以及对表的相关操作
    __tablename__ = 'test_detail'
    __table_args__ = {
        # 'autoload': True,
        'autoload_with': db.engine
    }


    def get_test_detail(self, page_no, page_size, test_name, user_name, test_status, parent_id): # 查询实验列表
        query_test = None

        query_test = db.session.query(TestDetail).filter(TestDetail.test_status == test_status).filter(TestDetail.user_name.like(f'%{user_name}%')).filter(TestDetail.test_name.like(f'%{test_name}%')).filter(TestDetail.parent_id == parent_id).order_by(TestDetail.id.asc()).paginate(page=page_no, per_page=page_size).items
        testlist = []
        login_time = ''
        # print(query_test)
        for test in query_test:
            create_time = test.create_time.strftime("%Y-%m-%d %H:%M:%S")
            testlist.append({'test_id': test.id, 'user_name': test.user_name, 'test_name': test.test_name, 'test_status': test.test_status, 'create_time': create_time,'seed': test.seed,'env_id': test.env_id,'learning_rate': test.learning_rate,'input_size': test.input_size,'info': test.info,'episode': test.episode})
        # print(testlist)
        return testlist


