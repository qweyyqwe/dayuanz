from django.urls import path

from . import views

urlpatterns = [
    path('add_pyq/', views.AddPyp.as_view()),
    path('get_self/', views.GetSelf.as_view()),
    path('get_all/', views.GetAll.as_view()),
    path('get_all_pyq/', views.GetAllPyq.as_view()),
    path('add_comment/', views.AddComment.as_view()),
    path('add_floor/', views.AddFloorComment.as_view()),
    path('get_floor/', views.LookFloorComment.as_view()),
]
