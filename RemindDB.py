#!/usr/bin/python3
# -*- coding:utf-8 -*-
import time
import pymysql
import Config
import json

# 打开数据库连接
db = pymysql.connect(Config.mysql_net_site, Config.mysql_user, Config.mysql_pass, Config.mysql_db)
db.set_charset('utf8')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()


# 打开数据库
def open_db():
    global db, cursor
    # 打开数据库连接
    db = pymysql.connect(Config.mysql_net_site, Config.mysql_user, Config.mysql_pass, Config.mysql_db)
    db.set_charset('utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()


# 查看mysql版本号
def select_mysql_version():
    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("select version()")

    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()

    print("Database version : %s " % data)
    # 关闭数据库连接
    return data


# 创建梦想数据库表
def create_remind_table():
    # 使用 execute() 方法执行 SQL，如果表存在则删除
    cursor.execute("drop table if exists remind")

    # 使用预处理语句创建表
    sql = """create table remind(remind_id BIGINT primary key AUTO_INCREMENT NOT NULL, getup CHAR(150) default '', 
    signin char(150) default '', lunch char(150) default '', signout char(150) default '', offwork CHAR(150) default '',
    overtime char(150) default '',
    sleep char(150) default '',date char(20) ) DEFAULT CHARSET = utf8 """

    try:
        cursor.execute(sql)
        print("创建表成功")
    except:
        db.rollback()
        print("创建表失败")


# 关闭数据库
def close_joke_db():
    cursor.close()
    db.close


# 向数据库中插入数据
def insert_remind_data(sign_in, sign_out, overtime):
    if overtime is None:
        overtime = ''

    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # SQL 插入语句
    sql = """insert into remind(signin, signout, overtime,date ) VALUES ('%s', '%s', '%s', '%s') """
    try:
        # 执行sql语句
        cursor.execute(sql % (sign_in, sign_out, overtime, datetime))
        # 提交到数据库执行
        db.commit()
        print("[笨鸟助手] ", sign_in, " 数据插入成功")
        return '1'
    except Exception:
        # 如果发生错误则回滚
        db.rollback()
        print("[笨鸟助手] 提醒数据插入失败")
        return ''
    return ''


# 向数据库中插入数据
def insert_my_remind_data(my_name):

    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # SQL 插入语句
    sql = """insert into remind(getup,signin,lunch,signout,offwork,overtime,sleep,date) VALUES ("%s",'%s','%s','%s', '%s','%s', '%s', '%s') """
    try:
        # 执行sql语句
        cursor.execute(sql % (my_name, my_name, my_name, my_name,my_name,my_name,my_name, datetime))
        # 提交到数据库执行
        db.commit()
        print("[笨鸟助手] ", my_name, " 数据插入成功")
        return '1'
    except Exception:
        # 如果发生错误则回滚
        db.rollback()
        print("[笨鸟助手] 提醒数据插入失败")
        return ''
    return ''


# 根据 id 删除指定梦想
def delete_remind_by_id(id):
    # 删除记录
    sql = "delete from remind where remind_id = '%d'"

    try:
        # 执行SQL语句
        cursor.execute(sql % id)
        db.commit()
        print("[笨鸟助手]", id, "删除成功")
        return '1'
    except:
        db.rollback()
        print("Error: unable to fetch data")
        return ''


def query_all_remind():
    # SQL 查询语句
    sql = "select * from remind"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
    except:
        print("Error: unable to fetch data")
    return results


# 根据 id 更新指定数据
def update_remind_by_id(remind_id, overtime):
    # SQL 查询语句
    sql = "update remind set overtime = '%s' where remind = '%d'"

    try:
        # 执行SQL语句
        cursor.execute(sql % (overtime, remind_id))
        db.commit()
        print("[笨鸟助手]", overtime, "加班数据成功")
        return '1'
    except:
        db.rollback()
        print("Error: unable to fetch data")
        return ''


# 根据梦想号查询梦想数据，返回json字符串
def query_remind_by_id(remind_id):
    # SQL 查询语句
    sql = "select * from remind where remind_id = '%d'"
    try:
        # 执行SQL语句
        cursor.execute(sql % remind_id)
        # 获取所有记录列表
        results = cursor.fetchall()
    except:
        print("Error: unable to fetch data")
    return results


# 查询梦想数据，返回json字符串
def query_remind_data():
    list = []
    item = {}
    # SQL 查询语句
    sql = "select * from remind"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            data = {}

            id = row[0]
            data['id'] = id

            getup = row[1]
            data['getup'] = getup

            signin = row[2]
            data['signin'] = signin

            lunch = row[3]
            data['lunch'] = lunch

            signout = row[4]
            data['signout'] = signout

            offwork = row[5]
            data['offwork'] = offwork

            overtime = row[6]
            data['overtime'] = overtime

            sleep = row[7]
            data['sleep'] = sleep

            date = row[8]
            data['date'] = date

            list.append(data)

        item['code'] = 1
        item['msg'] = '查询成功'
        item['data'] = list
    except:
        print("Error: unable to fetch data")
    return item


    # 查询梦想数据个数


def query_remind_data_count():
    # SQL 查询语句
    sql = "select count(*) from remind"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        result = cursor.fetchall()
        count = int(result[0][0])
    except:
        print("Error: unable to fetch data")
    return count


# 根据梦想号查询梦想数据，返回json字符串
def query_getup_remind():
    # SQL 查询语句
    sql = "select getup from remind where getup <> '' "
    try:
        # 执行SQL语句
        cursor.execute(sql)
        list = [];
        # 获取所有记录列表
        results = cursor.fetchall()
        if len(results) != 0:
            for item in results:
                list.append(item[0])
        return list
    except:
        print("Error: unable to fetch data")
    return ''


# 根据梦想号查询梦想数据，返回json字符串
def query_signin_remind():
    # SQL 查询语句
    sql = "select signin from remind where signin <> '' "
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        list = [];
        # 获取所有记录列表
        results = cursor.fetchall()
        if len(results) != 0:
            for item in results:
                list.append(item[0])
        return list
    except:
        print("Error: unable to fetch data")
    return ''


def query_lunch_remind():
    # SQL 查询语句
    sql = "select lunch from remind where lunch <> '' "
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        list = [];
        # 获取所有记录列表
        results = cursor.fetchall()
        if len(results) != 0:
            for item in results:
                list.append(item[0])
        return list
    except:
        print("Error: unable to fetch data")
    return ''


def query_signout_remind():
    # SQL 查询语句
    sql = "select signout from remind where signout <> '' "
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        list = [];
        # 获取所有记录列表
        results = cursor.fetchall()
        if len(results) != 0:
            for item in results:
                list.append(item[0])
        return list
    except:
        print("Error: unable to fetch data")
    return ''


def query_offwork_remind():
    # SQL 查询语句
    sql = "select offwork from remind where offwork <> '' "
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        list = [];
        # 获取所有记录列表
        results = cursor.fetchall()
        if len(results) != 0:
            for item in results:
                list.append(item[0])
        return list
    except:
        print("Error: unable to fetch data")
    return ''


def query_overtime_remind():
    # SQL 查询语句
    sql = "select overtime from remind where overtime <> '' "
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        list = [];
        # 获取所有记录列表
        results = cursor.fetchall()
        if len(results) != 0:
            for item in results:
                list.append(item[0])
        return list
    except:
        print("Error: unable to fetch data")
    return ''


def query_sleep_remind():
    # SQL 查询语句
    sql = "select sleep from remind where sleep <> '' "
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        list = [];
        # 获取所有记录列表
        results = cursor.fetchall()
        if len(results) != 0:
            for item in results:
                list.append(item[0])
        return list
    except:
        print("Error: unable to fetch data")
    return ''


# 主方法
if __name__ == '__main__':
    version = select_mysql_version()

    print("Database mysql : %s " % version)

    # create_remind_table()
    #
    # insert_my_remind_data('JerryShen')
    # insert_remind_data('JerryShen','JerryShen',"JerryShen")

    # result = query_all_remind()
    # for data in result:
    #     print(data)

    getup_list = query_getup_remind()
    if len(getup_list) != 0:
        for item in getup_list:
            print(item)


    remind = query_remind_data()
    remind_json = json.dumps(remind, ensure_ascii=False)
    print(remind_json)
