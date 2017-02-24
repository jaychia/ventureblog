from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from mezzanine.blog.models import BlogPost

# from models import Like

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

def like(request, id):

	likepost = BlogPost.objects.get(pk=id)
	print(request.COOKIES)

	# if request.session.get('likes', False):
	# 	if likepost.id not in request.session['likes']:
	# 		likelist = request.session['likes']
	# 		request.session['likes'] = likelist.append(likepost.id)
	# 		likepost.rating_count = likepost.rating_count + 1
	# 		likepost.save()
	# 		request.session.modified = True

	cookiestring = str(likepost._meta) + "." + str(likepost.pk)
	print(cookiestring)

	if request.COOKIES.get('mezzanine-rating', False):
		if cookiestring not in request.COOKIES.get('mezzanine-rating').split(','):
			cookielist = request.COOKIES['mezzanine-rating']
			cookielist = cookielist + "," + cookiestring
			request.COOKIES['mezzanine-rating'] = cookielist
			likepost.rating_count = likepost.rating_count + 1
			likepost.save()
			resp = JsonResponse({'status': 200})
			resp.set_cookie('mezzanine-rating', cookielist)
			return resp
		else:
			print('already insdie')
			return JsonResponse({'status': 405})
	else:
		print('nolikes')
		# request.session['likes'] = [likepost.id]
		# likepost.rating_count = likepost.rating_count + 1
		# likepost.save()
		# request.session.modified = True
		request.COOKIES['mezzanine-rating'] = cookiestring
		likepost.rating_count = likepost.rating_count + 1
		likepost.save()
		resp = JsonResponse({'status': 200})
		resp.set_cookie('mezzanine-rating', cookiestring)
		return resp


def dislike(request, id):

	likepost = BlogPost.objects.get(pk=id)

	if request.session.get('likes', False):
		pass
	else:
		try:
			newlist = request.session['likes']
			newlist.remove(id)
			request.session['likes'] = newlist
		except:
			pass

	likepost.rating_count = likepost.rating_count - 1
	likepost.save()

	return JsonResponse({'status': 200})