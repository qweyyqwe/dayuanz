# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : resource.py
# @Software: PyCharm
from child.models import UserGroup
from child.serializers import ResourceSer


def get_resource_list(user):
    group_list = UserGroup.objects.filter(user=user)
    resource_list = []
    for group in group_list:
        resource = ResourceSer(group.resource.all(), many=True).data
        for data in resource:
            resource_list.append(data)
    return resource_list


def menu_left_list(data):
    if len(data) <= 0:
        return data
    tree = {}
    for i in data:
        # 数的第一条数据就 变成data中i循环的第一条数据
        tree[i['id']] = i
    dlist = []
    for j in data:
        # 查看pid 是不是0，0为一级标签
        #  j['pid'] 就是data 数据中  每循环一条的数据中的pid
        pid = j['pid']
        if pid == 0:
            dlist.append(j)
        else:
            # 判断此子类的父类下面是否已经有了子类
            # 如果没有得到这pid 就跳出本次循环进入下一次循环
            if not tree.get(pid, None):
                continue
            # 如果son不在tree[pid]里面
            #    则就添加一个空列表
            # 否则就是在添加son一条数据
            if 'son' not in tree[pid]:
                tree[pid]['son'] = []
            tree[pid]['son'].append(j)
    return dlist
