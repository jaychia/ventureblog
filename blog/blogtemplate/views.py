from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from mezzanine.blog.models import BlogPost

def scrolling_banner(request):
	posts = BlogPost.objects.all()
	current_site = request.META['HTTP_HOST']
	ctd = {
		"posts": posts,
		"current_site": current_site,
	}
	return render(request, 'generic/includes/banner.html', ctd)