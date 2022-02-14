from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


#app_name = 'account'

urlpatterns = [
    #path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),

    # обработчики смены пароля
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # обработчики восстановления пароля
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # ИЛИ
    #path('', include('django.contrib.auth.urls')),

    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('people/', views.people, name='people'),
    path('my_posts/', views.my_posts, name='my_posts'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:author_id>/<int:post_id>/edit_post/', views.edit_post, name='edit_post'),
    path('<slug:author>/<int:author_id>/posts/', views.posts, name='posts'),
    path('add_post/', views.add_post, name='add_post'),

]