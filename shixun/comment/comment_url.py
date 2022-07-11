from django.urls import path

from . import views

urlpatterns = [
    path('get_comment/', views.GetComment.as_view()),
    path('add_comment/', views.AddComment.as_view()),
]
#