CREATE DATABASE rl;

USE rl;

#用户表
CREATE TABLE `user`(
`id` INT PRIMARY KEY AUTO_INCREMENT,      #用户的唯一标识
`username` VARCHAR(255) NOT NULL,     #用户名
`account` VARCHAR(255) UNIQUE NOT NULL,       #账号，用于登录
`password` VARCHAR(255) NOT NULL,     #密码
`identity` VARCHAR(255) NOT NULL DEFAULT '用户',#身份: 管理员 | 用户
`user_status` VARCHAR(255) NOT NULL,      #状态: 正常 | 封禁
`create_time` VARCHAR(255) NULL,      #创建时间
`login_time` VARCHAR(255) NULL ,       #登录时间
`email` VARCHAR(255) NULL; #email
);

#通知表
CREATE TABLE `notice`(
`id` INT PRIMARY KEY AUTO_INCREMENT,      #通知的唯一标识
`notice_title` VARCHAR(255) NOT NULL,     #通知的标题
`notice_detail` LONGTEXT NOT NULL,    #通知详情
`create_time` VARCHAR(255) NULL,      #创建时间
`is_delete` VARCHAR(255) NULL DEFAULT '正常' #是否被删除: 正常 | 删除
);
#通知阅读表
CREATE TABLE `notice_read`(
`id` BIGINT PRIMARY KEY AUTO_INCREMENT,#唯一标识
`user_id` INT NOT NULL,#用户id
`notice_id` INT NOT NULL,#通知id
`is_read` VARCHAR(255) NULL DEFAULT '未读'#是否已读: 未读 | 已读
);
#实验表
CREATE TABLE `test`(
`id` INT PRIMARY KEY AUTO_INCREMENT,        #实验的唯一标识
`user_name` VARCHAR(255) NOT NULL,        #用户名
`create_name` VARCHAR(255) NOT NULL,            #创建用户名
`test_name` VARCHAR(255)  NOT NULL,        #实验名
`test_status` VARCHAR(255) NOT NULL,        #状态: 正常 | 封禁
`create_time` VARCHAR(255) NULL,        #创建时间
`update_time` VARCHAR(255) NULL            #更新时间
);
