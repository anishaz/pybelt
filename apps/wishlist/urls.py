from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^dashboard$', views.dashboard, name="dashboard"),
    url(r'^wish_items/create$', views.create, name="createproduct"),
    url(r'^wish_items/add_product$', views.add, name="addproduct"),
    url(r'^wish_items/delete/(?P<id>\d+)$', views.delete, name="delete"),
    url(r'^addtomylist/(?P<id>\d+)$', views.mylist, name="addtomylist"),
    url(r'^removefrommylist/(?P<id>\d+)$', views.remove, name="removefrommylist"),
    url(r'^wish_items/(?P<id>\d+)$', views.view, name="viewproduct")
]
