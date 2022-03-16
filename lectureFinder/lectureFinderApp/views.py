from django.shortcuts import render
from django.urls import reverse
from lectureFinderApp.models import Lecture


def index(request):
	# Index page will display both the recently uploaded and the most viewed lectures.
	all_lectures = Lecture.objects.all()  # ordered by last record inserted into the table.
	all_lectures_by_views = all_lectures.order_by('-views')

	context_dict = {
		'recently_uploaded': all_lectures,
		'most_viewed': all_lectures_by_views
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


def show_lecture(request, lecture_name_slug):
	return render(request, 'lectureFinderApp/show_lecture.html')
