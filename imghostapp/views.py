from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import ImageForm
from django.contrib import messages

# Create your views here.
def home_view(request):
	context = {}
	return render(request, "imghostapp/home.html", context)

@login_required
def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Image has been uploaded to the server')
            return redirect('upload-image')
    else:
        form = ImageForm()
    
    return render(request, 'imghostapp/upload.html', {'form': form})