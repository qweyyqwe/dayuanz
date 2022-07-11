import logging
import traceback

from django.db.models import Q
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, generics

from goods.models import Goods, Picture, GoodsRecord
from goods.serializers import GoodsSer, GoodsRecordSer
from shixun.custom_permission import IsPointsManagerPermission
from shixun.pagenation import MyPagination
from user.models import User

logger = logging.getLogger('log')


class AddGoods(APIView):
    """
    添加商品
    """
    permission_classes = [permissions.IsAuthenticated, IsPointsManagerPermission]
    request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                  required=['name', 'price', 'count', 'desc', 'sale', 'image', 'picture_list'],
                                  properties=
                                  {'name': openapi.Schema(type=openapi.TYPE_STRING, description='商品名称'),
                                   'price': openapi.Schema(type=openapi.TYPE_STRING, description='商品价格'),
                                   'count': openapi.Schema(type=openapi.TYPE_STRING, description='商品数量'),
                                   'desc': openapi.Schema(type=openapi.TYPE_STRING, description='商品描述'),
                                   'sale_count': openapi.Schema(type=openapi.TYPE_STRING, description='商品售价'),
                                   'image': openapi.Schema(type=openapi.TYPE_STRING, description='商品image'),
                                   'picture_list': openapi.Schema(type=openapi.TYPE_STRING, description='商品图片'), }
                                  )

    @swagger_auto_schema(method='post', request_body=request_body, )
    @action(methods=['post'], detail=False, )
    def post(self, request):
        data = request.data
        name = request.data.get('name')
        logger.info('name:{}'.format(name))
        desc = request.data.get('desc')
        logger.info('desc:{}'.format(desc))
        image = request.data.get('image')
        logger.info('image:{}'.format(image))
        price = request.data.get("price")
        logger.info('price:{}'.format(price))
        count = request.data.get('count')
        logger.info('count:{}'.format(count))
        sale_count = request.data.get('sale_count')
        logger.info('sale_count:{}'.format(sale_count))
        if not all([name, price, price, desc, image, count, sale_count]):
            return Response({'msg': '添加信息不全', 'code': 400})
        if len(name) > 200:
            return Response({"msg": "The product name is too long", 'code': 400})
        if len(desc) > 100:
            return Response({'msg': 'The product desc is too long', 'code': 400})
        goods = Goods.objects.create(name=name, price=price, desc=desc,
                                     image=image, count=count, sale_count=sale_count)
        id = goods.id
        for i in data['picture_list']:
            i = i
            print('>>>>>>>>>i', i)
            pyq_picture = Picture.objects.create(url_path=i, goods_id=id)
            pyq_picture.save()
        return Response({'msg': 'Product added successfully', 'code': 200})


class UpdateGoods(APIView):
    """
    修改商品
    """

    def post(self, request):
        id = request.query_params.get('id')
        name = request.data.get('name')
        price = request.data.get('price')
        count = request.data.get('count')
        desc = request.data.get('desc')
        image = request.data.get('image')
        sale_count = request.data.get('sale_count')
        if not all([name, image, price, count, desc, sale_count]):
            return Response({'msg': '添加信息不全', 'code': 400})
        if len(name) > 20:
            return Response({"msg": "长度过长", 'code': 400})

        goods = Goods.objects.get(id=id)
        if not goods:
            return Response({'msg': '没有该商品', 'code': '400'})
        goods.name = name
        goods.price = price
        goods.desc = desc
        goods.count = count
        goods.sale_count = sale_count
        goods.image = image
        goods.save()
        return Response({'msg': '修改成功', 'code': 200})


class DeleteGoods(APIView):
    """
    删除商品
    """

    def post(self, request):
        id = request.query_params.get('id')
        goods = Goods.objects.get(id=id)
        if not goods:
            return Response({'msg': '没有该商品', 'code': '400'})
        Goods.objects.filter(id=id).update(count=0)
        return Response({'msg': '删除成功', 'code': 200})


class AllGoods(generics.GenericAPIView):
    """
    查看全部
    """
    serializer_class = GoodsSer
    permission_classes = [permissions.IsAuthenticated]
    query_param = [openapi.Parameter(name='size', in_=openapi.IN_QUERY, description="页数大小",
                                     type=openapi.TYPE_NUMBER),
                   openapi.Parameter(name='page', in_=openapi.IN_QUERY, description="页码", type=openapi.TYPE_NUMBER),
                   ]

    @swagger_auto_schema(method='get', manual_parameters=query_param)
    @action(methods=['get'], detail=False)
    def get(self, request):
        goods_list = Goods.objects.filter(count__gte=1)
        # 实例化分页对象
        page_cursor = MyPagination()
        # 分页
        data_list = page_cursor.paginate_queryset(goods_list, request, view=self)
        # total_count = data_list.count()
        data_list = self.get_serializer(data_list, many=True).data
        result = {'code': 200, 'data': data_list}
        return Response(result)


class ListGoods(APIView):
    """查看一条"""

    def get(self, request):
        goods = Goods.objects.filter(id=id).first()
        if not goods:
            return Response({'msg': '没有该商品', 'code': '400'})
        good = GoodsSer(goods).data
        return Response({"msg": '查看成功', 'data': good, 'code': 200})


class GetOneGoods(generics.GenericAPIView):
    """
    获取用户列表  可以按名字查询
    """
    serializer_class = GoodsSer
    permission_classes = [permissions.IsAuthenticated]

    query_param = [openapi.Parameter(name='q', in_=openapi.IN_QUERY, description="查询条件", type=openapi.TYPE_STRING),
                   openapi.Parameter(name='size', in_=openapi.IN_QUERY, description="页数大小",
                                     type=openapi.TYPE_NUMBER),
                   openapi.Parameter(name='page', in_=openapi.IN_QUERY, description="页码", type=openapi.TYPE_NUMBER),
                   ]

    @swagger_auto_schema(method='get', manual_parameters=query_param)
    @action(methods=['get'], detail=False)
    def get(self, request):
        q = request.query_params.get('keyword')
        goods_list = Goods.objects.filter(Q(name__contains=q) | Q(id__contains=q) | Q(desc__contains=q)).order_by('id')
        total_count = goods_list.count()
        # 实例化分页对象
        page_cursor = MyPagination()
        # 分页
        data_list = page_cursor.paginate_queryset(goods_list, request, view=self)

        data_list = self.get_serializer(data_list, many=True).data
        result = {'code': 200, 'data': data_list, 'total_count': total_count}
        return Response(result)


class LookGoods(APIView):
    """
    根据goods_id 查询
    """

    def get(self, request):
        goods_id = request.query_params.get('goods_id')
        goods = Goods.objects.filter(id=goods_id).first()
        goods_data = GoodsSer(goods).data
        info_picture_list = Picture.objects.filter(goods_id=goods_id).values_list('url_path', flat=True)
        info_picture_list = list(info_picture_list)
        goods_data.update({"info_picture_list": info_picture_list})
        return Response({"code": 200, 'data': goods_data})


# 点击购买获取前端商品的id
class PurchaseGoods(APIView):
    """积分购买商品"""

    def post(self, request):
        user = request.user
        user_id = user.id
        lock_count = int(request.data.get('lock_count'))
        goods_id = request.query_params.get('goods_id')
        user = User.objects.get(id=user_id)
        if not user:
            return Response({'msg': '没有该用户', 'code': 400})
        # 获取用户的积分
        integral = user.integral
        print('>>>>>>>>>>>>integral', integral)
        goods = Goods.objects.get(id=goods_id)
        count = goods.count
        if goods.count < lock_count:
            return Response({'msg': '该商品库存不足', 'code': 400})
        if not goods:
            return Response({'msg': '没有该商品', 'code': 400})
        # 获取商品的积分
        price = goods.price * lock_count
        print('>>>>>>>>>>>price', price)
        if integral < price:
            return Response({'msg': '用户的积分不足', 'code': 400})
        integral -= price
        print('积分', integral)
        user.integral = integral
        print("剩余的积分>>>>>>>>>>>", integral)
        count -= lock_count
        goods.count = count
        goods.lock_count += lock_count
        print("剩余的库存>>>>>>>>>>>count", count)
        user.save()
        goods.save()
        GoodsRecord.objects.create(user_id=user_id, goods_id=goods_id, count=lock_count, price=price)
        return Response({"msg": "兑换成功", 'code': 200})


# 获取用户兑换记录
class GoodsRecordView(APIView):
    """获取用户兑换记录"""

    def post(self, request):
        try:
            user = request.user
            user_id = user.id
            goods_record = GoodsRecord.objects.filter(user=user_id)
            print('>>>', goods_record)
            if not goods_record:
                return Response({'msg': '没有该用户兑换的记录', 'code': 400})
            print('>>>>>>>>>>>>>>goods_record', goods_record)
            ser = GoodsRecordSer(goods_record, many=True).data
            return Response({'msg': '用户查看记录成功', 'code': '200', 'data': ser})
        except:
            error = traceback.format_exc()
            logger.error(error)
            return Response({'code': 500, 'error': error})
