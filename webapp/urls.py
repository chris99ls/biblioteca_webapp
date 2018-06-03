from django.conf.urls import url
from . import views
from django_filters.views import FilterView
from webapp.filters import BookFilter
from django.contrib.auth.views import login,logout

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$', login,{'template_name':'accounts/login.html'}),
    url(r'^logout/$',logout,{'template_name':'accounts/logout.html'}),
    url(r'^register/$',views.register,name='register'),
 
     url(r'^search/$', FilterView.as_view(filterset_class=BookFilter,
        template_name='dashboard/book_searchengine.html'), name='search'),
]