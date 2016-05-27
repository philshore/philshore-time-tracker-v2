from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^users/$', views.UsersView.as_view()),

]
