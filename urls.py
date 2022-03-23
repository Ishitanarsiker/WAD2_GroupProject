from django.urls import path
from lectureFinderApp import views
from django.contrib.auth import views as auth_views

app_name = 'lectureFinderApp'

urlpatterns = [ 
	path('', views.index, name='index'),
	path('members/', views.members, name='members'),
	path('search/', views.search, name='search'),
	path('about/', views.about, name='about'),
	path('terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),
	path('lecture/<slug:lecture_name_slug>', views.show_lecture, name='show_lecture'),
	path('save_lecture/<slug:lecture_name_slug>', views.save_lecture, name='save_lecture'),
	path('delete_saved_lecture/<slug:lecture_name_slug>', views.delete_saved_lecture, name='delete_saved_lecture'),
	path('signup/', views.signup, name='signup'),
	path('login/', views.login_user, name='login'),
	path('logout/', views.logout_user, name='logout'),
	path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

