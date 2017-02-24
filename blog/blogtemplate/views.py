from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from mezzanine.blog.models import BlogPost

from future.builtins import str, int

from calendar import month_name

from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _

from mezzanine.blog.models import BlogPost, BlogCategory
from mezzanine.blog.feeds import PostsRSS, PostsAtom
from mezzanine.conf import settings
from mezzanine.generic.models import Keyword
from mezzanine.utils.views import paginate
from blogtemplate.models import AuthorProfile

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



User = get_user_model()


def blog_post_list(request, tag=None, year=None, month=None, username=None,
                   category=None, template="blog/blog_post_list.html",
                   extra_context=None):
    """
    Display a list of blog posts that are filtered by tag, year, month,
    author or category. Custom templates are checked for using the name
    ``blog/blog_post_list_XXX.html`` where ``XXX`` is either the
    category slug or author's username if given.
    """
    templates = []
    profilepics = AuthorProfile.get_pics_as_dict()
    blog_posts = BlogPost.objects.published(for_user=request.user)
    if tag is not None:
        tag = get_object_or_404(Keyword, slug=tag)
        blog_posts = blog_posts.filter(keywords__keyword=tag)
    if year is not None:
        blog_posts = blog_posts.filter(publish_date__year=year)
        if month is not None:
            blog_posts = blog_posts.filter(publish_date__month=month)
            try:
                month = _(month_name[int(month)])
            except IndexError:
                raise Http404()
    if category is not None:
        category = get_object_or_404(BlogCategory, slug=category)
        blog_posts = blog_posts.filter(categories=category)
        templates.append(u"blog/blog_post_list_%s.html" %
                          str(category.slug))
    author = None
    if username is not None:
        author = get_object_or_404(User, username=username)
        blog_posts = blog_posts.filter(user=author)
        templates.append(u"blog/blog_post_list_%s.html" % username)

    prefetch = ("categories", "keywords__keyword")
    blog_posts = blog_posts.select_related("user").prefetch_related(*prefetch)
    blog_posts = paginate(blog_posts, request.GET.get("page", 1),
                          settings.BLOG_POST_PER_PAGE,
                          settings.MAX_PAGING_LINKS)
    context = {"blog_posts": blog_posts, "year": year, "month": month,
               "tag": tag, "category": category, "author": author, 
               "profilepics": profilepics}
    context.update(extra_context or {})
    templates.append(template)
    return TemplateResponse(request, templates, context)


def blog_post_detail(request, slug, year=None, month=None, day=None,
                     template="blog/blog_post_detail.html",
                     extra_context=None):
    """. Custom templates are checked for using the name
    ``blog/blog_post_detail_XXX.html`` where ``XXX`` is the blog
    posts's slug.
    """
    profilepics = AuthorProfile.get_pics_as_dict()
    blog_posts = BlogPost.objects.published(
                                     for_user=request.user).select_related()
    blog_post = get_object_or_404(blog_posts, slug=slug)
    related_posts = blog_post.related_posts.published(for_user=request.user)
    context = {"blog_post": blog_post, "editable_obj": blog_post,
               "related_posts": related_posts, "profilepics": profilepics}
    context.update(extra_context or {})
    templates = [u"blog/blog_post_detail_%s.html" % str(slug), template]
    return TemplateResponse(request, templates, context)
