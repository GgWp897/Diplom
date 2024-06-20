from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.news, name='news'),
    path('<int:news_id>/', views.newsPage, name='newsPage'),
    path('auth/', views.auth, name='auth'),
    path('reg/', views.reg, name='reg'),
    path('newpassword/', views.newPassword, name='newPassword'),
    path('contacts/', views.contacts, name='contacts'),
    path('groups/', views.groups, name='groups'),
    path('group/<int:group_id>/', views.group, name='group'),
    path('like_meme/', views.like_meme, name='like_meme'),
    path('group/<int:group_id>/topics/', views.group_topics, name='group_topics'),
    path('discussionTopic/<int:topic_id>/', views.discussionTopic, name='discussionTopic'),
    path('standings/', views.standingsPilots, name='standingsPilots'),
    path('constructors/', views.standingsConstructors, name='standingsConstructors'),
    path('schedule/', views.schedule, name='schedule'),
    path('logout/', views.logOut, name='logout'),
    path('account/', views.account, name='account'),
    path('addPost/', views.addPost, name='addPost'),
    path('deletePost/<int:post_id>/', views.deletePost, name='deletePost'),
    path('posts/', views.posts, name='posts'),
    path('posts/<int:post_id>/', views.postPage, name='postPage'),
    path('post/<int:post_id>/add_comment/', views.postPage, name='add_comment'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
