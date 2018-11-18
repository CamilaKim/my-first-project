from django.urls import path, re_path
from . import views

app_name='areview'
urlpatterns=[
    # path('', views),
    path('scrape/', views.UrlInput, name='urlinput'),
    path('scrape/webcrawling', views.SentimentAnalysisView, name='sentimentanalysis'),
    path('', views.InputKeywordsView, name='index'),
    path('lists/', views.ProductListView, name= 'productlist'),
    path('home',views.home, name='home'),
    path('aid',views.aid, name ='aid'),
    path('study',views.study, name ='study'),
    path('project',views.project, name = 'project'),
    path('comment',views.comment, name='comment'),
    path('contact',views.contact, name='contact'),
    path('base', views.base, name='base'),
    path('base2',views.base2, name='base2'),
    path('delete_post/',views.delete_post),
    path('logout/', views.logout_page),
    path('api/posts/', views.PostCollection.as_view()),
    re_path(r'^api/posts/(?P<pk>[0-9]+)/$', views.PostMember.as_view()),
    path('like/', views.like, name='like'),
    path('create_post/', views.create_post),
    path('join', views.signup, name='join'),
    path('login', views.signin, name='login'),
]
