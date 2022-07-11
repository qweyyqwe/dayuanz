from django.urls import path

from . import views

urlpatterns = [
    path('get_dynamic/', views.GetDynamic.as_view()),
    path('get_dy/', views.GetDy.as_view()),
    path('change_status/<int:id>/', views.ChangeStatus.as_view()),
    path('changes_status/<int:id>/', views.ChangesStatus.as_view()),
    path('search_dynamic/', views.ShowSearch.as_view()),
    path('add_dynamic/', views.AddDynamic.as_view()),
    # 获取七牛云token
    path('get_qiniu/', views.QiNiuYun.as_view()),
    path('home/', views.Home.as_view()),
    path('all_people/', views.GetAllPeople.as_view()),
]
