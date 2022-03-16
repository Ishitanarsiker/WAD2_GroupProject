from django.shortcuts import render
from lectureFinderApp.models import Lecture
from django.urls import reverse


def index(request):
	# Index page will display both the recently uploaded and the most viewed lectures.
	all_lectures = Lecture.objects.all()  # ordered by last record inserted into the table.
	all_lectures_by_likes = all_lectures.order_by('-likes')

	context_dict = {
		'recently_uploaded': all_lectures,
		'most_viewed': all_lectures_by_likes
	}

	return render(request, 'lectureFinderApp/index.html', context=context_dict)


def about(request):
	return render(request, 'lectureFinderApp/about.html')

def members(request):
	return render(request, 'lectureFinderApp/members.html')


def search(request):
	return render(request, 'lectureFinderApp/search.html')


def about(request):
	return render(request, 'lectureFinderApp/about.html')


def show_lecture(request, lecture_id):
	return render(request, 'lectureFinderApp/show_lecture.html')
