from django.urls import path
from  . import views

urlpatterns=[
    path('myform/',views.myform_view,name='myform'),
    path('get_Menciones/',views.get_Menciones, name='get_response'),
    path('get_Hashtags/',views.get_Hashtags, name='get_response')
]