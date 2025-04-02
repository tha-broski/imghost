from django.shortcuts import render
from django.shortcuts import render
from django.conf import settings


# Create your views here.
def home_view(request):
	context = {}
	return render(request, "imghostapp/home.html", context)