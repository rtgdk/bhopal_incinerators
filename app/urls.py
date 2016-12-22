from django.conf.urls import url
from app import views
urlpatterns = [
url(r'^$', views.index, name='index'),
url(r'^about/$', views.about, name ="about"),
url(r'^services/$', views.services, name='services'),
url(r'^contact/$', views.contact, name ="contact"),
url(r'^our_technology/$', views.our_technology, name ="our_technology"),
url(r'^signup/$', views.signup, name ="signup"),
url(r'^user_login/$', views.user_login, name ="user_login"),
url(r'^admin_login/$', views.admin_login, name ="admin_login"),
url(r'^logout/$', views.logout, name ="logout"),
url(r'^user/(?P<user_id>\w+)/$',views.user_page,name="user page"),
#url(r'^email_validate/$', views.email_validate, name='email_validate'),
url(r'^update/$', views.update , name = 'update'),
url(r'^search/$', views.autocompleteModel , name = 'search'),
#url(r'^search2/$', views.autocompleteModel2 , name = 'search2'),
]

