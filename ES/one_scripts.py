# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : one_scripts.py
# @Software: PyCharm


"""
将数据库数据导入es
"""
# import pymysql
# import traceback
# from elasticsearch import Elasticsearch
#
#
# def get_db_data():
#     # 打开数据库连接（ip/数据库用户名/登录密码/数据库名）
#     db = pymysql.connect(host="101.42.224.35", user="root", password="123456",
#                          database="cloudnews", charset='utf8')
#     # 使用 cursor() 方法创建一个游标对象 cursor
#     cursor = db.cursor()
#     sql = "SELECT * FROM tb_course"
#     # 使用 execute()  方法执行 SQL 查询
#     cursor.execute(sql)
#     # 获取所有记录列表
#     results = cursor.fetchall()
#     # 关闭数据库连接
#     db.close()
#     return results
#
#
# def insert_data_to_es():
#     es = Elasticsearch("http://101.42.224.35:9200/")
#     # 清空数据
#     # es.indices.delete(index='tb_course')
#     try:
#         i = -1
#         for row in get_db_data():
#             print(row)
#             print(row[1], row[2])
#             i += 1
#             es.index(index='tb_course', body={
#                 'id': i,
#                 'table_name': 'table_name',
#                 'pid': row[0],
#                 'title': row[1],
#                 'desc': str(row[2]),
#             })
#     except:
#         error = traceback.format_exc()
#         print("Error: unable to fecth data", error)
#
#
# if __name__ == "__main__":
#     insert_data_to_es()
#
