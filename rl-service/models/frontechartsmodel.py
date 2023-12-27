from app import db
from config import get_cur_time, get_md5, test_status_true, test_status_false, test_status_all, user_identity_admin, user_identity_user, NoticeRead, NoticeConf, notice_isdel_no

# 后台用户表
class FrontEcharts(db.Model):  # 创建的类对应数据库的表以及对表的相关操作
    __tablename__ = 'datas'
    __table_args__ = {
        # 'autoload': True,
        'autoload_with': db.engine
    }

    @classmethod
    def get_echarts(self,test_detail_id,episode_id): # 查询表格数据
        query_echarts = db.session.query(FrontEcharts).filter(FrontEcharts.test_detail_id==test_detail_id).filter(FrontEcharts.episode_id == episode_id).first()
        if query_echarts == None:
            return []
        return {
            'test_detail_id': query_echarts.test_detail_id,
            'episode_id': query_echarts.episode_id,
            'shap': query_echarts.shap,
            'movement_decision': query_echarts.movement_decision,
            'qvalue': query_echarts.qvalue,
            'value_function': query_echarts.value_function,
            'reward_signal': query_echarts.reward_signal,
            'learning_curve': query_echarts.learning_curve
        }



