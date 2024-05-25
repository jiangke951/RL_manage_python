# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


import pandas as pd
import pymysql
import csv
from collections import namedtuple
import os


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def get_data(file_name):
    with open(file_name, 'r', encoding='utf-8', errors='ignore') as f:
        f_csv = csv.reader(f)
        headings = next(f_csv)
        Row = namedtuple('Row', headings)
        for r in f_csv:
            yield Row(*r)


def execute_sql(conn, sql):
    with conn.cursor() as cur:
        cur.execute(sql)
        print("执行成功")


def import_csv():
    print("执行开始")
    conn = pymysql.connect(
        host='localhost',
        user='root',
        passwd='12345678',
        db='library',
        port=3306
    )
    print('hahha')
    SQL_FORMAT = """insert into student_info values('{0}','{1}','{2}')"""
    # SQL_FORMAT = """insert into student_info values('{0}','{1}','{2}')"""
    conn.autocommit(1)
    # 获取当前文件的绝对路径

    for t in get_data('../test.csv'):
        print(t.id,t.name,t.gender)
        sql = SQL_FORMAT.format(t.id,t.name,t.gender)
        print(sql)
        execute_sql(conn,sql)
    # sql = SQL_FORMAT.format(1, 'name', 'gender')
    # execute_sql(conn, sql)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    print_hi('PyCharm')
    import_csv()
