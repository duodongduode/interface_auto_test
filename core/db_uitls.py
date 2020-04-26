
#coding=utf-8
import  pymysql
import traceback
import random
"""
连接数据库需要知道那几个参数： ip  port  user  password   数据库名字
我们通过pymysql操作数据库， 我们可能只需要增删改查，  增删改（修改数据）    查（只是查看，不修改数据）
1、获取连接
2、从连接里面获取一个cursor
3、执行sql（是增删改  还是查找）
4、获取结果（如果是查找）
5、关闭 cursor  关闭连接
"""
from core import common_data


def  select_data(sql):
    print(sql)
    conn = None
    cur =None
    try:
        #1、获取连接
        conn = pymysql.Connect(host=common_data.global_vars.get("database_ip"), user=common_data.global_vars.get("database_user"), password=common_data.global_vars.get("database_password"), database=common_data.global_vars.get("database_name"), port=int(common_data.global_vars.get("database_port")), charset='UTF8')
        #2、从连接里面获取一个cursor
        cur = conn.cursor()
        #执行sql
        cur.execute(sql)
        #获取结果（如果是查找）
        result = cur.fetchall()
        return result

    except:
        print('错误')
        print(traceback.format_exc())
    #关闭 cursor  关闭连接
    finally:
        try:
            if cur != None:
                cur.close()
        except:
            print(traceback.format_exc())
        finally:
            if conn != None:
                conn.close()


def insert_delete_update(sql):
    """
    执行数据库的增删改查操作
    :param sql:
    :return:
    """
    print(sql)
    conn = None
    cur = None
    try:
        #1、获取连接
        conn = pymysql.Connect(host=common_data.global_vars.get("database_ip"), user=common_data.global_vars.get("database_user"), password=common_data.global_vars.get("database_password"), database=common_data.global_vars.get("database_name"), port=int(common_data.global_vars.get("database_port")), charset='UTF8')
        #2、从连接里面获取一个cursor
        cur = conn.cursor()
        #执行sql
        cur.execute(sql)
        #如果执行增删改操作，需要执行提交操作
        conn.commit()
    except:
        print('错误')
        print(traceback.format_exc())
    #关闭 cursor  关闭连接
    finally:
        try:
            if cur != None:
                cur.close()
        except:
            print(traceback.format_exc())
        finally:
            if conn != None:
                conn.close()


if __name__ == '__main__':

    pass

