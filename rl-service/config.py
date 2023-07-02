import json
import time
from app import db
from datetime import datetime
import hashlib # 密码加密
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr



# 用户状态
user_status_true = '1'
user_status_false = '0'
user_status_all = '全部'
# 实验状态
test_status_true = '1'
test_status_false = '0'
test_status_all = '全部'

# 用户身份
user_identity_admin = '管理员'
user_identity_user = '用户'

# 座位状态
seat_status_use = '使用中'
seat_status_free = '空闲中'
seat_status_all = '全部'

# 座位是否被删除
seat_isdel_no = '正常'
seat_isdel_yes = '移除'

# 通知是否被删除
notice_isdel_no = '正常'
notice_isdel_yes = '删除'

# 预约座位状态
reserve_status_normal = '正常'
reserve_status_out = '超时'
reserve_status_all = '全部'

# 预约信息是否被删除
reserve_isdel_no = '正常'
reserve_isdel_yes = '删除'


# 从客户端获取的数据
def get_data(data):
    try:
        return json.loads(list(data)[0])
    except Exception as e:
        return dict(data)

# 传给客户端的数据
def send_data(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False)

# 传提示数据 1为错误, 0为正常, 默认是1, 方便处理错误的消息
def send_cc(msg: str, status: int = 1) -> str:
    return json.dumps({'status': status, 'msg': msg}, ensure_ascii=False)

# 验证日期格式
def isVaildDate(date):
    try:
        if ":" in date:
            time.strptime(date, "%Y-%m-%d %H:%M:%S")
        else:
            time.strptime(date, "%Y-%m-%d")
            return True
    except:
            return False

def is_vaild_date(date):
    try:
        if ":" in date:
            time.strptime(date, "%Y-%m-%d %H:%M:%S")
            return True
    except:
            return False

# 判断给定时间是否大于当前时间15分钟
def is_vaild_big15min(date): # 格式: yyyy-mm-dd hh:mm:ss
    time_arr = None
    try:
        time_arr = time.strptime(date, "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        time_arr = ''
    if time_arr == '' or time_arr == None: return False
    time_stamp = int(round(time.mktime(time_arr) * 1000)) # 转化为时间戳
    # 获取当前时间 加上15分钟 的时间戳
    now = int(round(time.time() * 1000)) + 15 * 60 * 1000
    if time_stamp < now:
        return False
    else: return True

# 判断是否超时
def is_vaild_timeout(date): # 格式: yyyy-mm-dd hh:mm:ss
    time_arr = None
    try:
        time_arr = time.strptime(date, "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        time_arr = ''
    if time_arr == '' or time_arr == None: return True
    time_stamp = int(round(time.mktime(time_arr) * 1000)) # 转化为时间戳
    # 获取当前时间的时间戳
    now = int(round(time.time() * 1000))
    if time_stamp < now:
        return True
    else: return False


# 获取当前日期
def get_cur_time():
    cur_time = str(datetime.now())[0:19]
    return cur_time

# 密码加密
def get_md5(pwd):
    obj = hashlib.md5()
    obj.update(pwd.encode('utf-8'))
    result = obj.hexdigest()
    return result

# 发送邮件
sender = 'test@qq.com'  # 填写发信人的邮箱账号
email_pwd = 'tjazycbkkylqebbj'  # 发件人邮箱授权码
get_user = 'test@qq.com'  # 收件人邮箱账号
def mail(info, title): # 邮件内容和邮件标题
    ret = True
    try:
        msg = MIMEText(info, 'plain', 'utf-8')  # 填写邮件内容
        msg['From'] = formataddr(["昵称", sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["昵称", get_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = title  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器
        server.login(sender, email_pwd)  # 括号中对应的是发件人邮箱账号、邮箱授权码
        server.sendmail(sender, [get_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret

# 通知阅读表
class NoticeRead(db.Model):
    __tablename__ = 'notice_read'
    __table_args__ = {
        # 'autoload': True,
        'autoload_with': db.engine
    }

# 通知表
class NoticeConf(db.Model):
    __tablename__ = 'notice'
    __table_args__ = {
        # 'autoload': True,
        'autoload_with': db.engine
    }

# 用户表
class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {
        # 'autoload': True,
        'autoload_with': db.engine
    }

# 座位表
class Seat(db.Model):
    __tablename__ = 'seat'
    __table_args__ = {
        # 'autoload': True,
        'autoload_with': db.engine
    }

# 预约表
class ReserveConf(db.Model):
    __tablename__ = 'reserve_seat'
    __table_args__ = {
        # 'autoload': True,
        'autoload_with': db.engine
    }

# 图表
class Echarts(db.Model):
    __tablename__ = 'echarts'
    __table_args__ = {
        # 'autoload': True,
        'autoload_with': db.engine
    }

# 实验表
class Test(db.Model):
    __tablename__ = 'test'
    __table_args__ = {
        # 'autoload': True,
        'autoload_with': db.engine
    }