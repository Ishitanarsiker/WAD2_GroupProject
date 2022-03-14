from django.urls import path
from django.conf.urls import url
from lectureFinderApp import views

app_name = 'lectureFinderApp'

urlpatterns = [ 
	path('', views.index, name='index'),
	path('members/', views.members, name='members'),
	path('search/', views.search, name='search'),
	#path('about/', views.about, name='about'),
	#path('register/', views.register, name='register'),
	#path('login/', views.user_login, name='login'),
	#path('restricted/', views.restricted, name='restricted'),
	#path('logout/', views.user_logout, name='logout'),
]
