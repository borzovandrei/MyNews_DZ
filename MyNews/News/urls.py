from django.conf.urls import url, include
from News import views
from .views import  like, add_comment, create_post

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^articles/(?P<article_id>[0-9]+)/$', views.show_article, name='article'),
    url(r'^signup$',  views.signup, name='signup'),
    url(r'^signin$',  views.signin, name='signin'),
    url(r'^logout$',  views.logout, name='logout'),
    url(r'^success$',  views.login_success, name='success'),
    url(r'^tutor/(?P<id>\d+)$',  views.TutorView.as_view(), name='tutor'),
    url(r'^main/$', views.main, name='main'),

    url(r'^post$', create_post, name='create_post'),
    url(r'^like/(?P<post_id>\d+)$', like, name='like'),
    url(r'^comment/(?P<post_id>\d+)$', add_comment, name='add_comment'),
]
