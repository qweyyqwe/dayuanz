# Create your views here.


import logging
import random
import time
import traceback

from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect
# from django.views.decorators import http
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from utils.alp.alipay import get_ali_object, pay
from utils.custom_permissions import IsCheckUser
from utils.form.bank_form import BankUserForm, RefundMoneyForm
from utils.phone_charm.phone_charm import send_message
from utils.phone_charm.send_code import send_son
from utils.pinstance import PinstanceList
from utils.redis_cache import mredis
from .models import BankUser, LoanRecord, TopUpRecord
from .serializers import BankUserSer, LoanRecordSer
from utils.alp.code import uniqueness_code

logger = logging.getLogger('log')


class AddBankUser(APIView):
    """
    用户———开户
    """
    permission_classes = [permissions.IsAuthenticated]
    request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                  required=['name', 'card_id', 'phone', 'bank_card_id', 'password'], properties=
                                  {'name': openapi.Schema(type=openapi.TYPE_STRING, description='姓名'),
                                   'card_id': openapi.Schema(type=openapi.TYPE_STRING, description='身份证'),
                                   'phone': openapi.Schema(type=openapi.TYPE_STRING, description='手机号'),
                                   'bank_card_id': openapi.Schema(type=openapi.TYPE_STRING, description='银行卡号'),
                                   'password': openapi.Schema(type=openapi.TYPE_STRING, description='银行密码'),
                                   },

                                  )

    @swagger_auto_schema(method='post', request_body=request_body, )
    @action(methods=['post'], detail=False, )
    def post(self, request):
        try:
            data = BankUserForm(request.data)
            user = request.user
            user_id = user.id
            if data.is_valid():
                data = data.cleaned_data
                user = BankUser.objects.filter(user=user_id)
                if not user:
                    data.update({'user_id': request.user.id})
                    obj = BankUser.objects.create(**data)
                    obj.save()
                    return Response({'code': 200, 'msg': '开户成功'})
                else:
                    return Response({'msg': '用户已开户', 'code': 406})
            error = data.errors.as_json()
            return Response({'code': 407, 'msg': error})
        except:
            error = traceback.format_exc()
            logger.error('AddBankUser——— error:{}'.format(error))
            return Response({'code': 500, 'msg': error})


class GetBankUserInfo(APIView):
    """
    获取当前用户的开户信息情况
    """
    permission_classes = [permissions.IsAuthenticated]

    query_param = []

    @swagger_auto_schema(method='get', manual_parameters=query_param)
    @action(methods=['get'], detail=False)
    def get(self, request):
        user = request.user
        user_id = user.id
        try:
            user = BankUser.objects.filter(user_id=user_id)
            if not user:
                return Response({'code': 406, 'msg': '未获取到该用户的开户信息'})
            bankuser = BankUser.objects.get(user_id=user_id)
            bank_ser = BankUserSer(bankuser).data
            return Response({'code': 200, 'data': bank_ser})
        except:
            error = traceback.format_exc()
            logger.error('GetBankUserInfo——error:{}'.format(error))
            return Response({'code': 500, 'msg': error})


class LoanMoney(APIView):
    """
    开户人员借贷
    """

    permission_classes = [permissions.IsAuthenticated]
    request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                  required=['loan_money'], properties=
                                  {
                                      'loan_money': openapi.Schema(type=openapi.TYPE_STRING, description='贷款金额'),
                                      'expect': openapi.Schema(type=openapi.TYPE_STRING, description='分期'),
                                  },
                                  )

    @swagger_auto_schema(method='post', request_body=request_body, )
    @action(methods=['post'], detail=False, )
    def post(self, request):
        user = request.user
        user_id = user.id
        loan_money = request.data.get('loan_money')
        phone = request.data.get('phone')
        code = request.data.get('code')
        bank_password = request.data.get('bank_password')
        bank_user = BankUser.objects.filter(user=user_id)
        if not bank_user:
            return Response({'msg': '该用户未进行开户，请开户后尝试', 'code': 500})
        try:
            get_bank_user = BankUser.objects.get(user=user_id)
            if int(loan_money) > 30000:
                return Response({'msg': '超标了！超标了!!!', 'code': 406})
            if bank_password != get_bank_user.password:
                return Response({'msg': '银行卡的密码不一致，请重试', 'code': 406})
            get_bank_filter = LoanRecord.objects.filter(Q(user_id=get_bank_user.id) & Q(status=0)).count()
            if int(get_bank_filter) > 10:
                return Response({'msg': '已有{}次未还款，请还款后再次借贷'.format(get_bank_user), 'code': 406})
            # 手机验证码
            # redis_cli = redis.Redis(db=2)
            data = mredis.str_get("sms_%s" % phone)
            # 获取的data b字节 转str
            redis_code = str(data, "utf-8")
            print(redis_code, code)
            if redis_code:
                # 取redis中的验证码
                redis_code = data.decode('utf-8')
                logger.info('LoanMoney—输入的code{}取出的redis_code{}'.format(code, redis_code))
                if redis_code == code:
                    loan = LoanRecord.objects.create(loan_money=loan_money, user_id=get_bank_user.id, code=code)
                    loan.save()
                    # 创建成功      数据写入redis进行分配
                    bank_key = 'bank_%s' % user_id
                    code = str(user_id) + str(random.randint(10000, 99999)) + str(int(time.time()))
                    mredis.l_push(bank_key, value=code)
                    return Response({'msg': '提交申请，待处理', 'code': 200})
                else:
                    return Response({'msg': '验证码错误', 'code': '400 '})
            else:
                return Response({"msg": "验证码以过期", "code": "401"})
        except:
            error = traceback.format_exc()
            logger.error('LoanMoney———error:{}'.format(error))
            return Response({'code': 500, 'msg': error})


class ShowBankUser(APIView):
    """
    展示用户自己经审核通过的申请
    """
    permission_classes = [permissions.IsAuthenticated]
    query_param = [openapi.Parameter(name='size', in_=openapi.IN_QUERY, description="页数大小", type=openapi.TYPE_NUMBER),
                   openapi.Parameter(name='page', in_=openapi.IN_QUERY, description="页码", type=openapi.TYPE_NUMBER)]

    @swagger_auto_schema(method='get', manual_parameters=query_param)
    @action(methods=['get'], detail=False)
    def get(self, request):
        user = request.user
        user_id = user.id
        loan_user = BankUser.objects.get(user_id=user_id)
        bank_user = LoanRecord.objects.filter(Q(status=2) & Q(user_id=loan_user.id)).all()
        bank_money_count = bank_user.count()
        bank_money_ser = PinstanceList()
        # 分页
        data_list = bank_money_ser.paginate_queryset(bank_user, request, view=self)
        bank_money_ser = LoanRecordSer(data_list, many=True).data
        return Response({'data': bank_money_ser, 'count': bank_money_count, 'code': '200'})


class GetBankPhone(APIView):
    """
    借贷时手机验证码发送手机验证码
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        mobile = request.data.get('phone')
        # delay 不加这个则会变成同步
        # 调用方法
        result = send_message.delay(mobile)
        if result['statusCode'] == '172001':
            return Response({'msg': '网络错误', 'code': '400'})
        elif result['statusCode'] == '160038':
            return Response({'msg': '验证码过于频繁', 'code': '400'})
        else:
            return Response({'msg': '欧克', 'code': '200'})


class GetAllLoanMoney(APIView):
    """
    审核员 获取自己要处理的数据
    """

    permission_classes = [permissions.IsAuthenticated, IsCheckUser]
    query_param = []

    @swagger_auto_schema(method='get', manual_parameters=query_param)
    @action(methods=['get'], detail=False)
    def get(self, request):
        data = request.query_params
        page = data.get('page')
        size = data.get('size')
        bank_money_list = LoanRecord.objects.filter(Q(status=0) | Q(status=1) & Q(user_id=request.user.id)).all()
        bank_money_count = bank_money_list.count()
        bank_money_ser = PinstanceList()
        # 分页
        data_list = bank_money_ser.paginate_queryset(bank_money_list, request, view=self)
        bank_money_ser = LoanRecordSer(data_list, many=True).data
        return Response({'data': bank_money_ser, 'count': bank_money_count, 'code': '200'})


class CheckSucceed(APIView):
    """
    审核  通过/不通过
    """

    permission_classes = [permissions.IsAuthenticated, IsCheckUser]

    def post(self, request):
        user = request.user
        user_id = user.id
        loan_id = request.data.get('loan_id')
        type = request.data.get('type')

        try:
            if type == 2:
                # 通过
                # loan_record = LoanRecord.objects.get(id=str(loan_id))
                ''' '''
                loan_record = LoanRecord.objects.filter(id=loan_id).update(status=2, late_time=timezone.now(),
                                                                                loan_status=1, check_user_id=user_id)

                # loan_record.status = 2
                # loan_record.late_time = timezone.now
                # loan_record.loan_status = 1
                # loan_record.check_user_id = user_id
                # loan_record.save()
                return Response({'msg': '通过', 'code': 200})
            elif type == 3:
                # TODO 不通过待完善
                return Response({'msg': '不通过', 'code': 200})
            else:
                return Response({'msg': '参数不合法', 'code': 500})
        except:
            error = traceback.format_exc()
            logger.error('CheckSucceed——error:{}'.format(error))
            return Response({'msg': error, 'code': 500})


class GetNotLoanMoney(APIView):
    """
    获取未分配的借贷请求
    """

    permission_classes = [permissions.IsAdminUser, IsCheckUser]
    query_param = [openapi.Parameter(name='size', in_=openapi.IN_QUERY, description="页数大小", type=openapi.TYPE_NUMBER),
                   openapi.Parameter(name='page', in_=openapi.IN_QUERY, description="页码", type=openapi.TYPE_NUMBER)]

    @swagger_auto_schema(method='get', manual_parameters=query_param)
    @action(methods=['get'], detail=False)
    def get(self, request):
        data = request.query_params
        # page = data.get('page')
        # size = data.get('size')
        bank_money_list = LoanRecord.objects.filter(status=0).all()
        bank_money_count = bank_money_list.count()
        bank_money_ser = PinstanceList()
        # 分页
        data_list = bank_money_ser.paginate_queryset(bank_money_list, request, view=self)
        bank_money_ser = LoanRecordSer(data_list, many=True).data
        return Response({'data': bank_money_ser, 'count': bank_money_count, 'code': '200'})


# 进入支付接口
class GetMoney(APIView):
    def post(self, request):
        data = request.data
        user = request.user
        user_id = user.id
        # 显式的开启一个事务
        with transaction.atomic():
            # 创建事务保存点
            save_id = transaction.savepoint()
            try:
                money = data['outer_money']
                code = uniqueness_code(user_id)
                alipay = get_ali_object()
                query_params = alipay.direct_pay(
                    subject="充值",  # 商品简单描述
                    out_trade_no=code,  # 用户购买的商品订单号(每次都不一样)
                    total_amount=int(money)  # 交易金额
                )
                bank_user = BankUser.objects.get(user_id=user_id)
                TopUpRecord.objects.create(user_id=bank_user.id, money=money, code=code)
                bank_user.money += int(money)
                bank_user.save()
                pay_url = "https://openapi.alipaydev.com/gateway.do?{0}".format(query_params)
                logger.info('GetMoney——pay_url:{}'.format(pay_url))
                # 提交订单成功，显式的提交一次事务
                transaction.savepoint_commit(save_id)
                return Response({"code": 200, "message": "ok", "url": pay_url})
            except:
                # 报错回滚
                transaction.savepoint_rollback(save_id)
                error = traceback.format_exc()
                logger.error('GetMoney——error:{}'.format(error))
                return Response({"code": 500, "msg": error})


# 充值回调
class GoMoney(APIView):
    def get(self, request):
        try:
            trade_no = request.query_params.get("trade_no")
            code_key = "code_" + str(request.user.id)
            code = mredis.str_get(code_key)
            money_record = TopUpRecord.objects.filter(code=code).update(serial_number=trade_no)
            return redirect("http://127.0.0.1:8080/user_info")
        except:
            error = traceback.format_exc()
            logger.error('GoMoney——error:{}'.format(error))
            return Response({"code": 500, "msg": False})


class ShowSignAll(APIView):
    """
    展示新标
    """
    permission_classes = [permissions.IsAuthenticated]
    query_param = [openapi.Parameter(name='size', in_=openapi.IN_QUERY, description="页数大小", type=openapi.TYPE_NUMBER),
                   openapi.Parameter(name='page', in_=openapi.IN_QUERY, description="页码", type=openapi.TYPE_NUMBER)]

    @swagger_auto_schema(method='get', manual_parameters=query_param)
    @action(methods=['get'], detail=False)
    def get(self, request):
        try:
            user = request.user
            user_id = user.id
            loan_user = BankUser.objects.get(user_id=user_id)
            # 展示新标  审核通过的 除了自己以外的
            # bank_user = LoanRecord.objects.filter(Q(status=2) & ~Q(user_id=loan_user.id))
            # 展示所有新标
            bank_user = LoanRecord.objects.filter(status=2)
            bank_money_count = bank_user.count()
            bank_money_ser = PinstanceList()
            # 分页
            data_list = bank_money_ser.paginate_queryset(bank_user, request, view=self)
            bank_money_ser = LoanRecordSer(data_list, many=True).data
            return Response({'data': bank_money_ser, 'count': bank_money_count, 'code': '200'})

        except:
            error = traceback.format_exc()
            logger.error('ShowSignAll——error:{}'.format(error))
            return Response({'error': error, 'code': 406})


# class OrderCommitView(APIView):
#     """订单提交"""
#
#     def post(self, request):
#         """保存订单信息和订单商品信息"""
#         # 显式的开启一个事务
#         with transaction.atomic():
#             # 创建事务保存点
#             save_id = transaction.savepoint()
#
#             # 暴力回滚
#             try:
#                 # 保存订单基本信息 OrderInfo（一）
#                 order = OrderInfo.objects.create(
#                     ...
#                 )
#
#                 # 从redis读取购物车中被勾选的商品信息
#                 ...
#                 # 遍历购物车中被勾选的商品信息
#                 for ...
#                     if ...:
#                         # 出错就回滚
#                         transaction.savepoint_rollback(save_id)
#                         return ...
#             except Exception as e:
#                 # 出错后记日志+回滚
#                 logger.error(e)
#                 transaction.savepoint_rollback(save_id)
#                 return ...
#
#             # 提交订单成功，显式的提交一次事务
#             transaction.savepoint_commit(save_id)
#         # 响应提交订单结果
#         return ...


class OrderCommitView(APIView):
    """订单提交"""

    def post(self, request):
        """保存订单信息和订单商品信息"""
        # 获取当前保存订单时需要的信息
        # 显式的开启一个事务
        with transaction.atomic():
            # 创建事务保存点
            save_id = transaction.savepoint()

            # 暴力回滚
            try:
                # 保存订单基本信息 OrderInfo（一）
                order = OrderInfo.objects.create(
                    order_id=order_id,
                    user=user,
                    address=address,
                    total_count=0,
                    total_amount=Decimal('0'),
                    freight=Decimal('10.00'),
                    pay_method=pay_method,
                    status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'] if pay_method == OrderInfo.PAY_METHODS_ENUM[
                        'ALIPAY'] else
                    OrderInfo.ORDER_STATUS_ENUM['UNSEND']
                )

                # 从redis读取购物车中被勾选的商品信息
                redis_conn = get_redis_connection('carts')
                redis_cart = redis_conn.hgetall('carts_%s' % user.id)
                selected = redis_conn.smembers('selected_%s' % user.id)
                carts = {}
                for sku_id in selected:
                    carts[int(sku_id)] = int(redis_cart[sku_id])
                sku_ids = carts.keys()

                # 遍历购物车中被勾选的商品信息
                for sku_id in sku_ids:
                    # 查询SKU信息
                    sku = SKU.objects.get(id=sku_id)
                    # 判断SKU库存
                    sku_count = carts[sku.id]
                    if sku_count > sku.stock:
                        # 出错就回滚
                        transaction.savepoint_rollback(save_id)
                        return JsonResponse({
                            'code': RETCODE.STOCKERR,
                            'errmsg': '库存不足'})

                    # SKU减少库存，增加销量
                    sku.stock -= sku_count
                    sku.sales += sku_count
                    sku.save()

                    # 修改SPU销量
                    sku.goods.sales += sku_count
                    sku.goods.save()

                    # 保存订单商品信息 OrderGoods（多）
                    OrderGoods.objects.create(
                        order=order,
                        sku=sku,
                        count=sku_count,
                        price=sku.price,
                    )

                    # 保存商品订单中总价和总数量
                    order.total_count += sku_count
                    order.total_amount += (sku_count * sku.price)

                # 添加邮费和保存订单信息
                order.total_amount += order.freight
                order.save()
            except Exception as e:
                logger.error(e)
                transaction.savepoint_rollback(save_id)
                return Response({'code': RETCODE.DBERR, 'errmsg': '下单失败'})

            # 提交订单成功，显式的提交一次事务
            transaction.savepoint_commit(save_id)

        # 清除购物车中已结算的商品
        pl = redis_conn.pipeline()
        pl.hdel('carts_%s' % user.id, *selected)
        pl.srem('selected_%s' % user.id, *selected)
        pl.execute()

        # 响应提交订单结果
        return JsonResponse({'code': RETCODE.OK,
                             'errmsg': '下单成功',
                             'order_id': order.order_id})


class InvestMoney(APIView):
    """
    新标  投资
    """
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        user = request.user
        user_id = user.id
        try:
            # 要投的新标
            invest_id = request.data.get('invest_id')
            loan_money = request.data.get('loan_money')
            loan = LoanRecord.objects.get(id=invest_id)
            # 新标投资总额度
            residue_money = loan.loan_money
            if int(loan_money) > int(residue_money):
                return Response({'msg': '当前投资金额大于新标总额', 'code': 406})
            elif int(loan_money) < 0:
                return Response({'msg': '数据不合法', 'code': 406})
            else:
                # 获取当前用户可投金额
                user = BankUser.objects.get(user_id=user_id)
                balance = user.money
                if int(balance) > int(loan_money):
                    # 可投金额
                    # pay_money = pay(loan_money, invest_id)
                    # TODO 对字段进行操作
                    code = uniqueness_code(id)
                    alipay = get_ali_object()
                    query_params = alipay.direct_pay(
                        subject="投资",  # 商品简单描述
                        out_trade_no=code,  # 用户购买的商品订单号(每次都不一样)
                        total_amount=int(loan_money)  # 交易金额
                    )
                    pay_url = "https://openapi.alipaydev.com/gateway.do?{0}".format(query_params)
                    return Response({"code": 200, "message": "ok", "url": pay_url})
                else:
                    return Response({'msg': '余额不足，无法投标', 'code': 500})
        except:
            error = traceback.format_exc()
            logger.error('InvestMoney——error:{}'.format(error))
            return Response({'msg': error, 'code': 406})


class InvestCallBack(APIView):
    """
    投标 回调
    """
    def get(self, request):
        try:
            trade_no = request.query_params.get("trade_no")
            code_key = "invest_code" + str(id)
            mredis.str_get(code_key)
            # money_record = TopUpRecord.objects.filter(code=code_key).update(serial_number=trade_no)
            # 回调成功    登录用户减少  借的金额
            # 对应新标    减少 借的金额   余额到0时新标完成   删除新标    改状态
            return redirect("http://127.0.0.1:8080/user_info")
        except:
            error = traceback.format_exc()
            logger.error('GoMoney——error:{}'.format(error))
            return Response({"code": 500, "msg": False})


class GetUserLoan(APIView):
    """
    获取自己还款清单
    """

    permission_classes = [permissions.IsAuthenticated]
    query_param = [openapi.Parameter(name='size', in_=openapi.IN_QUERY, description="页数大小", type=openapi.TYPE_NUMBER),
                   openapi.Parameter(name='page', in_=openapi.IN_QUERY, description="页码", type=openapi.TYPE_NUMBER)]

    @swagger_auto_schema(method='get', manual_parameters=query_param)
    @action(methods=['get'], detail=False)
    def get(self, request):
        user = request.user
        user_id = user.id
        bank_user = BankUser.objects.get(user_id=user_id)
        bank_user_id = bank_user.id
        loanlist = LoanRecord.objects.filter(Q(user_id=bank_user_id) & Q(status=2))
        loan_money_count = loanlist.count()
        loan_money_ser = PinstanceList()
        # 分页
        data_list = loan_money_ser.paginate_queryset(loanlist, request, view=self)
        loan_money_ser = LoanRecordSer(data_list, many=True).data
        return Response({'data': loan_money_ser, 'count': loan_money_count, 'code': '200'})


class RefundMoney(APIView):
    """
    用户还款
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = RefundMoneyForm(request.data)
        user = request.user
        user_id = user.id
        try:
            bankuser = BankUser.objects.get(user_id=user_id)
            if data.is_valid():
                data = data.cleaned_data
                a = data.get('bank_card_id')
                b = data.get('bank_password')
                print(a, b)
                # bankuser_verify = BankUser.objects.filter(Q(bank_card_id=data.get('bank_card_id') | Q(password=data.get('bank_password')))).first()
                # bankuser_verify = BankUser.objects.filter_by(bank_card_id=data.get('bank_card_id'),password=data.get('bank_password')))).first()
                if bankuser_verify:
                    return Response({'msg': '不匹配', 'code': 500})
                loan_money = LoanRecord.objects.get(user_id=bankuser.user_id)
                money = data.get('refund_money')
                # 余额
                balance = int(loan_money) - int(money)
                bankuser_verify.update(money=balance)

                return Response({'code': 200, 'msg': 'OK'})

            err = data.errors.as_json()
            return Response({'code': 407, 'msg': err})
        except:
            error = traceback.format_exc()
            logger.error('RefundMoney——error:{}'.format(error))
            return Response({'code': 500, 'msg': error})


class SendRefundCode(APIView):
    """
    还款验证手机号
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        phone = request.query_params.get('phone')
        print(phone)
        mobile = send_son(phone)
        return Response({'code': 200, 'msg': '成功'})
