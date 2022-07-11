# Create your views here.


import logging
import traceback

from django.db.models import Q
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.form.integral_shopping_form import FormIntegralShopping
from utils.pinstance import PinstanceList
from .models import PointsMall, Img, Record
from .serializers import PointsMallSer, RecordSer

logger = logging.getLogger('log')


class AddIntegralShopping(APIView):
    """
    管理员  添加商品
    """

    permission_classes = [permissions.IsAuthenticated]

    request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                  required=['name', 'desc', 'image', 'price', 'count'],
                                  properties=
                                  {'name': openapi.Schema(type=openapi.TYPE_STRING, description='昵称'),
                                   'desc': openapi.Schema(type=openapi.TYPE_STRING, description='简介'),
                                   'image': openapi.Schema(type=openapi.TYPE_STRING, description='简介图片'),
                                   'price': openapi.Schema(type=openapi.TYPE_STRING, description='价格'),
                                   'count': openapi.Schema(type=openapi.TYPE_STRING, description='库存')}
                                  )

    @swagger_auto_schema(method='post', request_body=request_body)
    @action(methods=['post'], detail=False)
    def post(self, request):

        # data = request.data
        # test_form = FormIntegralShopping(data)
        # if test_form.is_valid():
        #     # 下面就是验证通过啦
        #     logger.info('AddIntegralShopping——{}'.format(request.POST.get('name'), request.POST.get('desc'),
        #                                                  request.POST.get('price'), request.POST.get('count')))
        #     shopping = PointsMall.objects.create(**data)
        # logger.error('AddIntegralShopping—error:{}'.format(test_form.errors))
        data = request.data
        try:
            info = data['form']
            name = info.get('name')
            desc = info.get('desc')
            image = info.get('image')
            price = info.get('price')
            count = info.get('count')
            points_count = PointsMall.objects.filter(name=name).count()
            if points_count >= 1:
                return Response({'msg': '该商品已存在', 'code': 406})
            shopping = PointsMall.objects.create(name=name, desc=desc, image=image, price=price, count=count)
            shopping.save()
            id = shopping.id
            if data['img_list']:
                for i in data['img_list']:
                    shopping = Img.objects.get_or_create(url=i, pointsmallid_id=id)
            return Response({'code': 200, 'msg': '添加商品成功'})
        except:
            error = traceback.format_exc()
            logger.error('AddIntegralShopping——error:{}'.format(error))
            return Response({'msg': '商品添加失败', 'code': 406})


class GetAllIntegralShopping(APIView):
    """
    展示所有商品
    """
    query_param = []

    @swagger_auto_schema(method='get', manual_parameters=query_param)
    @action(methods=['get'], detail=False)
    def get(self, request):
        data = request.query_params
        page = data.get('page')
        size = data.get('size')
        shopping = PointsMall.objects.filter(status=0).all()
        shopping_count = shopping.count()
        page_cursor = PinstanceList()
        # 分页
        data_list = page_cursor.paginate_queryset(shopping, request, view=self)
        shopping_ser = PointsMallSer(data_list, many=True)
        return Response({'shopping_list': shopping_ser.data, 'shopping_count': shopping_count})


class GetOneIntegralShopping(APIView):
    """
    商品详情信息

    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = request.query_params
        shopping_id = data.get('shopping_id')
        shopping = PointsMall.objects.filter(id=shopping_id).first()
        shopping_list = {
            'id': shopping.id,
            'name': shopping.name,
            'desc': shopping.desc,
            'image': shopping.image,
            'price': shopping.price,
            'count': shopping.count,
            'lock_count': shopping.lock_count,
            'sale_count': shopping.sale_count
        }
        return Response({'code': 200, 'shopping_one': shopping_list})


class UpdateIntegralShopping(APIView):
    """
    修改商品
    """

    permission_classes = [permissions.IsAdminUser]

    request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                  required=['name', 'desc', 'image', 'price', 'count'],
                                  properties=
                                  {'name': openapi.Schema(type=openapi.TYPE_STRING, description='昵称'),
                                   'desc': openapi.Schema(type=openapi.TYPE_STRING, description='简介'),
                                   'image': openapi.Schema(type=openapi.TYPE_STRING, description='简介图片'),
                                   'price': openapi.Schema(type=openapi.TYPE_STRING, description='价格'),
                                   'count': openapi.Schema(type=openapi.TYPE_STRING, description='库存'),
                                   'lock_count': openapi.Schema(type=openapi.TYPE_STRING, description='锁定库存')}
                                  )

    @swagger_auto_schema(method='post', request_body=request_body)
    @action(methods=['post'], detail=False)
    def post(self, request):
        data = request.data
        shopping_id = data.get('shopping_id')
        try:
            test_form = FormIntegralShopping(data)
            if test_form.is_valid():
                # 下面就是验证通过啦
                logger.info('UpdateIntegralShopping——{}'.format(request.POST.get('name'), request.POST.get('desc'),
                                                                request.POST.get('image'), request.POST.get('price'),
                                                                request.POST.get('count'), request.POST.get('lock_count')))
                # shopping = PointsMall.objects.create(**data)
                shopping = PointsMall.objects.get(id=shopping_id).update(**data)
            logger.error('UpdateIntegralShopping—error:{}'.format(test_form.errors))
            return Response({'code': 200, 'msg': '修改成功'})
        except:
            error = traceback.format_exc()
            logger.error('UpdateIntegralShopping—error:{}'.format(error))
            return Response({'code': 406, 'msg': error})


class DelIntegralShopping(APIView):
    """
    删除商品
    """
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        shopping_id = request.query_params.get('shopping_id')
        shopping = PointsMall.objects.get(id=shopping_id)
        if shopping.status == 1:
            return Response({'msg': '该商品已下架', 'code': 406})
        shopping.status = 1
        shopping.save()
        return Response({'code': 200, 'msg': '成功删除'})


class PayShopping(APIView):
    """
    用户购买商品
    """
    permission_classes = [permissions.IsAuthenticated]

    request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                  required=['name', 'desc', 'image', 'price', 'count'],
                                  properties=
                                  {'name': openapi.Schema(type=openapi.TYPE_STRING, description='昵称'),
                                   'desc': openapi.Schema(type=openapi.TYPE_STRING, description='简介'),
                                   'image': openapi.Schema(type=openapi.TYPE_STRING, description='简介图片'),
                                   'price': openapi.Schema(type=openapi.TYPE_STRING, description='价格'),
                                   'count': openapi.Schema(type=openapi.TYPE_STRING, description='库存')}
                                  )

    @swagger_auto_schema(method='post', request_body=request_body)
    @action(methods=['post'], detail=False)
    def post(self, request):
        user = request.user
        user_id = user.id
        data = request.data
        goods_id = data.get('goods_id')
        count = data.get('count', 1)
        # 获取用户的积分
        integral = user.integral
        goods = PointsMall.object.get(id=goods_id)

        # 库存做key
        count_key = "good{}".format(goods_id)
        real_count = int(goods.count) - int(goods.lock_count)
        if real_count < count:
            return Response({'msg': '商品库存量不足', 'code': 400})
        # 获取商品的积分
        price = goods.price
        # 计算商品的积分
        price *= count
        if integral < price:
            return Response({'msg': '用户的积分不足', 'code': 400})
        integral -= price
        user.integral = integral
        logger.info('用户—{}—剩余的积分—{}—'.format(user_id, integral))
        user.save()
        price = int(price)
        Record.objects.create(user_id=user_id, goods_id=goods_id, count=count, price=price)
        return Response({"msg": "兑换成功", 'code': 200})


# 获取用户兑换记录
class UserRrecord(APIView):
    """获取用户兑换记录"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            user_id = request.data.get('user_id')
            user_id = int(user_id)
            record = Record.objects.filter(user_id=user_id)
            if not record:
                return Response({'msg': '没有该用户兑换的记录', 'code': 400})
            record_ = Record.objects.filter(user_id=user_id).all()
            ser = RecordSer(record_, many=True).data
            return Response({'msg': '用户查看记录成功', 'code': '200', 'data': ser})
        except:
            error = traceback.format_exc()
            logger.error(error)
            return Response({'code': 500, 'error': error})


class MaxSaleCount(APIView):
    """
    按照销量排序

    """
    permission_classes = [permissions.IsAuthenticated]
    query_param = [
                   openapi.Parameter(name='size', in_=openapi.IN_QUERY, description="页数大小", type=openapi.TYPE_NUMBER),
                   openapi.Parameter(name='page', in_=openapi.IN_QUERY, description="页码", type=openapi.TYPE_NUMBER),
                   ]

    @swagger_auto_schema(method='get', manual_parameters=query_param)
    @action(methods=['get'], detail=False)
    def get(self, request):
        goods = PointsMall.objects.filter(status=0).order_by('-sale_count')
        total_count = goods.count()
        # 实例化分页对象
        page_cursor = PinstanceList()
        # 分页
        data_list = page_cursor.paginate_queryset(goods, request, view=self)
        data = PointsMallSer(data_list, many=True).data
        return Response({'code': 200, 'data': data, 'count': total_count})


class TypeSorting(APIView):
    """
    # TODO 新建type类型表
    安装类型展示系列
    (相似产品推荐)
    """
    query_param = openapi.Parameter(name='goods_id', in_=openapi.IN_QUERY, description="商品id", type=openapi.TYPE_STRING)

    @swagger_auto_schema(method='get', manual_parameters=query_param)
    @action(methods=['get'], detail=False)
    def get(self, request):
        pass


# class Recommend(APIView):
#     def get(self, request):
#         goods_id = request.query_params.get('goods_id')
#         goods = Goods.objects.filter(id=goods_id)
#         goods_data = GoodsSer(goods, many=True).data
#         for i in goods_data:
#             name = i['name'][:6]
#             desc = i['desc'][:3]
#         goods = Goods.objects.filter(Q(name__contains=name) | Q(desc__contains=desc))
#         return Response({'code': 200, 'data': goods_data})



