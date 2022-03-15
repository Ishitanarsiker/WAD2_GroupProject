from django.shortcuts import render

def index(request):
	return render(request, 'lectureFinderApp/index.html')

def about(request):
	return render(request, 'lectureFinderApp/about.html')

def members(request):
	return render(request, 'lectureFinderApp/members.html')

def search(request):
	return render(request, 'lectureFinderApp/search.html')
