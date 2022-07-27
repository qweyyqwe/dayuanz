# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : excel.py
# @Software: PyCharm
import xlrd
import datetime

from xlrd import xldate_as_tuple

#导入需要读取Excel表格的路径
# data = xlrd.open_workbook(r'test.xlsx')
data = xlrd.open_workbook(r'D:\test\dayuanz\file\xlsx\\test.xls')
table = data.sheets()[0]
# 创建一个空列表，存储Excel的数据
tables = []


# 将excel表格内容导入到tables列表中
def import_excel(excel):
    for rown in range(excel.nrows):
        # array = {'road_name': '', 'bus_plate': '', 'timeline': '', 'road_type': '', 'site': ''}
        # array['road_name'] = table.cell_value(rown, 0)
        # array['bus_plate'] = table.cell_value(rown, 1)
        # # 将Excel表格中的时间格式转化
        # if table.cell(rown, 2).ctype == 3:
        #     date = xldate_as_tuple(table.cell(rown, 2).value, 0)
        #     array['timeline'] = datetime.datetime(*date)
        # array['road_type'] = table.cell_value(rown, 3)
        # array['site'] = table.cell_value(rown, 4)
        # tables.append(array)
        array = {'user': '', 'loab_money': '', 'content': '', 'expect': ''}
        array['user'] = table.cell_value(rown, 0)
        array['loab_money'] = table.cell_value(rown, 2)
        array['content'] = table.cell_value(rown, 4)
        array['expect'] = table.cell_value(rown, 6)
        tables.append(array)



if __name__ == '__main__':
  #将excel表格的内容导入到列表中
  import_excel(table)
  #验证Excel文件存储到列表中的数据
  for i in tables:
    print(i)

