from django.urls import path, re_path
from . import views
from pwa.views import service_worker

urlpatterns = [
    path('', views.homepage, name="home"),
    path('v1/', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('sign-up/', views.signUp, name="signup"),
    path('new/post/stp-1/', views.post_1, name="post_1"),
    path('new/post/stp-2/', views.post_2, name="post_2"),
    #path("CVC/user/update/profile/", views.manage_profile, name="create_profile"),

    # Profile View (username may include slashes)
    path('CVC/user/profile/$', views.profile, name='profile'),

    # Create Profile
    path('CVC/user/create/profile/$', views.manage_profile, name='create_profile'),

    # Settings
    path('CVC/user/profile/settings/$', views.settings, name='settings'),
    path('CVC/user/profile/settings/info/$', views.profile_settings, name='profile_settings'),
    path('CVC/user/profile/settings/info/edit/$', views.edit_account, name='edit_account'),

    # Delete Post
    path('<str:post_id>/post/delete/', views.delete, name="delete"),

    # Search Post
    path('search/', views.search, name="search"),

    # Logout
    path('logout/', views.logout, name="logout"),

    # Comments
    path('post/<str:post_id>/comment/', views.comments, name="comment"),

    # Static Pages
    path('about/', views.about, name="about"),
    path('terms/', views.terms, name="terms"),
    path('privacy/', views.privacy, name="privacy"),
    path('feedback-report/', views.feedback, name="feedback"),

    # Service Worker
    path("serviceworker.js", service_worker, name="serviceworker"),
]
