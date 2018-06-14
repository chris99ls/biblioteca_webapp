from django.conf.urls import url,include
from . import views
from django_filters.views import FilterView
from webapp.filters import BookFilter
from django.contrib.auth.views import login,logout
from django.contrib import admin

urlpatterns = [
    url(r'^$', views.home, name='home'),
   
    url(r'^login/$',login, {'template_name': 'accounts/login.html'},name='login'),
    url(r'^logout/$',logout,{'template_name':'accounts/logout.html'},name='logout'),
    url(r'^register/$',views.register,name='register'),

    url(r'^search/$', FilterView.as_view(filterset_class=BookFilter,
        template_name='dashboard/book_searchengine.html'), name='search'),

    url(r'^catalog/$',views.catalog,name='catalogo'),
    url(r'^user/$',views.user_home,name='home_utente'),

    url(r'^book/detail/(?P<xx>[\w\+]+)/(?P<pk>[0-9]+)/$', views.detail , name='book_detail'),
    url(r'^book/reserve/(?P<pk>[0-9]+)/$', views.reserve_book, name='reserve_book'),
    url(r'^book/delete/(?P<pk>[0-9]+)/$', views.delete_book, name='delete_book'),

    url(r'^administrator/search/$', views.search_book_google, name='search_book_google'),
    url(r'^administrator/search/add/(?P<pk>[0-9]+)$', views.add_book, name='add_success'),
     url(r'^administartor/catalog/$',views.admin_catalog,name='admin_catalog'),
    url(r'^administrator/$', views.admin_home, name='admin_home'),
    

]