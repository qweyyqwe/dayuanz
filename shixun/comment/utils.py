# 无限级分类重组
def get_comment_list(data):
    if len(data) <= 0:
        return data
    print('++++++++++++++++12346')
    # 对数据解析重组
    tree = {}
    for i in data:
        tree[i['id']] = i
    # 初始化列表
    dlist = []

    for j in data:
        # 查看pid是否为0，为0代表第一级
        print('111',j)
        print('222',j['pid'])
        pid = j['pid']
        if pid == 0:
            dlist.append(j)
        else:
            # 判断此子类的父类下面是否已经有子类，如果没有初始化
            if not tree.get(pid, None):
                continue
            if 'children' not in tree[pid]:
                tree[pid]['children'] = []
            tree[pid]['children'].append(j)

    return dlist