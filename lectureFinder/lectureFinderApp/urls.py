from django.urls import path
from lectureFinderApp import views

app_name = 'lectureFinderApp'

urlpatterns = [ 
	path('', views.index, name='index'),
	path('members/', views.members, name='members'),
	path('search/', views.search, name='search'),
	path('about/', views.about, name='about'),
	path('terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),
	path('lecture/<slug:lecture_name_slug>', views.show_lecture, name='show_lecture'),
	path('save_lecture/<slug:lecture_name_slug>', views.save_lecture, name='save_lecture'),
	path('signup/', views.signup, name='signup'),
	path('login/', views.login_user, name='login'),
	path('logout/', views.logout_user, name='logout'),
	#path('register/', views.register, name='register'),
	#path('login/', views.user_login, name='login'),
	#path('restricted/', views.restricted, name='restricted'),
	#path('logout/', views.user_logout, name='logout'),
]

