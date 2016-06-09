from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^user/$', views.UsersView.as_view()),
    url(r'^list/$', views.UserListView.as_view()),
    url(r'^auth/$', views.AuthView.as_view(), name='authenticate'),

]
