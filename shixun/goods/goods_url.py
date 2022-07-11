from django.urls import path

from . import views

urlpatterns = [
    path('add_goods/', views.AddGoods.as_view()),
    path('update_goods/', views.UpdateGoods.as_view()),
    path('del_goods/', views.DeleteGoods.as_view()),
    path('all_goods/', views.AllGoods.as_view()),
    path('one_goods/', views.GetOneGoods.as_view()),
    path('one_goods_picture/', views.LookGoods.as_view()),
    path('purchase_goods/', views.PurchaseGoods.as_view()),
    # 查看用户兑换记录
    path('goods_record/', views.GoodsRecordView.as_view()),
]
