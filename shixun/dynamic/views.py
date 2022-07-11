import redis
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from qiniu import Auth

from dynamic.models import Dynamic
from dynamic.serializers import DynamicSer
from shixun.custom_permission import IsChecker
from shixun.pagenation import MyPagination
from user.models import User, UserGroup


# 初始化审核员
class Home(APIView):
    def post(self, request):
        user = UserGroup.objects.get(id=1)
        house_user = user.user.all()
        a = []
        for i in house_user:
            a.append(i.username)
            print(i.username)
        res = redis.Redis()
        res.ltrim('1', 1, 0)
        for i in house_user:
            # print(i.username)
            res.lpush('1', i.username)
        return Response({'code': 200, 'data': a})


class GetAllPeople(APIView):
    def get(self, request):
        res = redis.Redis()
        peopel = res.lrange('1', 0, -1)
        print(peopel)
        return Response({'code': 200, 'data': peopel})


class AddDynamic(APIView):
    def post(self, request):
        user = request.query_params.get('user_id')
        # user = request.data.get('user_id')
        title = request.data.get('title')
        content = request.data.get('content')
        if not all([title, content]):
            return Response({'code': 401, 'msg': '信息不完善'})
        if len(title) > 50:
            return Response({'code': 402, 'msg': '公告名字过长'})
        users = User.objects.filter(id=user).count()
        print('>>>>>>>>>>>>>.users', users)
        if users == 0:
            return Response({'code': 403, 'msg': '该用户不存在'})
        # 分配修理工
        # res = redis.Redis()
        # data = res.rpop('1')
        # datas = data.decode()
        Dynamic.objects.create(title=title, content=content, user_id=user)
        return Response({'code': 201, 'msg': '添加成功'})


class GetDynamic(APIView):
    """
    展示所有动态
    """

    def get(self, request):
        dynamic_list = Dynamic.objects.filter(status=2)
        page_cursor = MyPagination()
        total_count = dynamic_list.count()
        data_list = page_cursor.paginate_queryset(dynamic_list, request, view=self)
        data_list = DynamicSer(data_list, many=True).data
        return Response({'code': 200, 'data': data_list, 'total_count': total_count})


class ChangeStatus(APIView):
    """点击开始修改公告为status=1"""
    permission_classes = [IsChecker]

    def put(self, request, id):
        notice = Dynamic.objects.filter(id=id)
        print('>>>>>>>>>>>>>>>notice', notice)
        if not notice:
            return Response({'msg': '没有该信息', 'code': 500})
        notice_title = Dynamic.objects.get(id=id, status=0)
        print('>>>>>>>>>notice_title', notice_title)
        notice_title.status = 1
        notice_title.save()
        return Response({'msg': '审核通过，发布成功', 'code': 200})


class ChangesStatus(APIView):
    """点击开始修改动态为status=2"""

    def put(self, request, id):
        notice = Dynamic.objects.filter(id=id)
        print('>>>>>>>>>>>>>>>notice', notice)
        if not notice:
            return Response({'msg': '没有该信息', 'code': 500})
        notice_title = Dynamic.objects.get(id=id, status=0)
        print('>>>>>>>>>notice_title', notice_title)
        notice_title.status = 2
        notice_title.save()
        return Response({'msg': '审核未通过', 'code': 200})


# 通过title查找动态
class ShowSearch(APIView):
    def get(self, request):
        print('>>>', request.query_params)
        name = request.query_params.get('title')
        print('>>name', name)
        order = Dynamic.objects.filter(title__contains=name)
        ser = DynamicSer(order, many=True)
        return Response(ser.data)


AK = 'Vo776PPZQy5f6lgtN0rQy5GQ4VGfrmyJqCT8kK4P'
SK = 'rXAAlcH9HcTFb_jvJUR1V1OFYnvZeUo7F4uGZTc2'
# 要上传的空间
bucket_name = '123admin789'


def get_qiniu_token():
    # 构建鉴权对象
    q = Auth(AK, SK)
    # 生成上传Token，可以指定过期时间等
    token = q.upload_token(bucket_name)
    return token


class QiNiuYun(APIView):
    """
    获取七牛云token
    """

    def get(self, request):
        return Response({'code': 200, 'token': get_qiniu_token()})


class GetDy(ListAPIView):
    """
    获取user表的所有数据
    """
    queryset = Dynamic.objects.all()
    serializer_class = DynamicSer