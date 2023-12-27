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
`create_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,        #创建时间
`update_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP            #更新时间
);
#历史实验表
CREATE TABLE `test_detail` (
  `id` int NOT NULL AUTO_INCREMENT,
  `parent_id` varchar(255) NOT NULL,
  `user_name` varchar(255) NOT NULL,
  `create_name` varchar(255) NOT NULL,
  `test_name` varchar(255) NOT NULL,
  `test_status` varchar(255) NOT NULL,
  `seed` varchar(255) NOT NULL,
  `env_id` varchar(255) NOT NULL,
  `learning_rate` varchar(255) NOT NULL,
  `input_size` varchar(255) NOT NULL,
  `info` varchar(255) NOT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;




#历史实验表
CREATE TABLE `test_detail` (
  `id` int NOT NULL AUTO_INCREMENT,
  `parent_id` varchar(255) NOT NULL,
  `user_name` varchar(255) NOT NULL,
  `create_name` varchar(255) NOT NULL,
  `test_name` varchar(255) NOT NULL,
  `test_status` varchar(255) NOT NULL,
  `seed` varchar(255) NOT NULL,
  `env_id` varchar(255) NOT NULL,
  `learning_rate` varchar(255) NOT NULL,
  `input_size` varchar(255) NOT NULL,
  `info` varchar(255) NOT NULL,
  `episode` int NOT NULL ,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

#实验表数据表（）
CREATE TABLE `datas`(
`id` INT PRIMARY KEY AUTO_INCREMENT,        #datas的唯一标识
`test_detail_id` INT NOT NULL,        #test_detail的唯一标识
`episode_id` INT NOT NULL,
`shap` VARCHAR(255) NOT NULL,        #shap值
`movement_decision` VARCHAR(255) NOT NULL,        #动作选择
`qvalue` text NOT NULL,       #Q值函数
`value_function` VARCHAR(255) NOT NULL,        #价值函数
`reward_signal` VARCHAR(255) NOT NULL,        #奖励信号
`learning_curve` VARCHAR(255) NOT NULL        #学习曲线
);

