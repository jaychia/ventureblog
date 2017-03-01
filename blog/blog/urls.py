from __future__ import unicode_literals
from future.builtins import str

from django.conf.urls import include, url
from django.contrib.sitemaps.views import sitemap
from django.views.i18n import javascript_catalog
from django.http import HttpResponse
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views.i18n import set_language

from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings
from mezzanine.core.sitemaps import DisplayableSitemap
from mezzanine.blog import views
import blogtemplate.views as blog_views

admin.autodiscover()

# Add the urlpatterns for any custom Django applications here.
# You can also change the ``home`` view to add your own functionality
# to the project's homepage.

urlpatterns = i18n_patterns(
    # Change the admin prefix here to use an alternate URL for the
    # admin interface, which would be marginally more secure.
    url("^admin/", include(admin.site.urls)),
)

if settings.USE_MODELTRANSLATION:
    urlpatterns += [
        url('^i18n/$', set_language, name='set_language'),
    ]

_slash = "/" if settings.APPEND_SLASH else ""

urlpatterns += [
    # We don't want to presume how your homepage works, so here are a
    # few patterns you can use to set it up.

    # HOMEPAGE AS STATIC TEMPLATE
    # ---------------------------
    # This pattern simply loads the index.html template. It isn't
    # commented out like the others, so it's the default. You only need
    # one homepage pattern, so if you use a different one, comment this
    # one out.

    # url("^$", direct_to_template, {"template": "index.html"}, name="home"),

    # HOMEPAGE AS AN EDITABLE PAGE IN THE PAGE TREE
    # ---------------------------------------------
    # This pattern gives us a normal ``Page`` object, so that your
    # homepage can be managed via the page tree in the admin. If you
    # use this pattern, you'll need to create a page in the page tree,
    # and specify its URL (in the Meta Data section) as "/", which
    # is the value used below in the ``{"slug": "/"}`` part.
    # Also note that the normal rule of adding a custom
    # template per page with the template name using the page's slug
    # doesn't apply here, since we can't have a template called
    # "/.html" - so for this case, the template "pages/index.html"
    # should be used if you want to customize the homepage's template.
    # NOTE: Don't forget to import the view function too!

    # url("^$", mezzanine.pages.views.page, {"slug": "/"}, name="home"),

    # HOMEPAGE FOR A BLOG-ONLY SITE
    # -----------------------------
    # This pattern points the homepage to the blog post listing page,
    # and is useful for sites that are primarily blogs. If you use this
    # pattern, you'll also need to set BLOG_SLUG = "" in your
    # ``settings.py`` module, and delete the blog page object from the
    # page tree in the admin if it was installed.
    # NOTE: Don't forget to import the view function too!

    url("^$", blog_views.blog_post_list, name="home"),

    #OWN_URLS
    url("banner", blog_views.scrolling_banner, name="scrolling_banner"),
    url(r"rating/like/(?P<id>.*)", blog_views.like, name="ratinglike"),
    url(r"rating/dislike/(?P<id>.*)", blog_views.dislike, name="ratingdislike"),

    # MEZZANINE'S URLS
    # ----------------
    # ADD YOUR OWN URLPATTERNS *ABOVE* THE LINE BELOW.
    # ``mezzanine.urls`` INCLUDES A *CATCH ALL* PATTERN
    # FOR PAGES, SO URLPATTERNS ADDED BELOW ``mezzanine.urls``
    # WILL NEVER BE MATCHED!

    # If you'd like more granular control over the patterns in
    # ``mezzanine.urls``, go right ahead and take the parts you want
    # from it, and use them directly below instead of using
    # ``mezzanine.urls``.
    # url(r"^", include("mezzanine.urls")),

    # MOUNTING MEZZANINE UNDER A PREFIX
    # ---------------------------------
    # You can also mount all of Mezzanine's urlpatterns under a
    # URL prefix if desired. When doing this, you need to define the
    # ``SITE_PREFIX`` setting, which will contain the prefix. Eg:
    # SITE_PREFIX = "my/site/prefix"
    # For convenience, and to avoid repeating the prefix, use the
    # commented out pattern below (commenting out the one above of course)
    # which will make use of the ``SITE_PREFIX`` setting. Make sure to
    # add the import ``from django.conf import settings`` to the top
    # of this file as well.
    # Note that for any of the various homepage patterns above, you'll
    # need to use the ``SITE_PREFIX`` setting as well.

    # ("^%s/" % settings.SITE_PREFIX, include("mezzanine.urls"))

]

#Pulled from mezzanine urls for granular control:

# JavaScript localization feature
js_info_dict = {'domain': 'django'}
urlpatterns += [
    url(r'^jsi18n/(?P<packages>\S+?)/$', javascript_catalog, js_info_dict),
]

if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:
    try:
        import debug_toolbar
    except ImportError:
        pass
    else:
        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]

# Django's sitemap app.
if "django.contrib.sitemaps" in settings.INSTALLED_APPS:
    sitemaps = {"sitemaps": {"all": DisplayableSitemap}}
    urlpatterns += [
        url("^sitemap\.xml$", sitemap, sitemaps),
    ]

# Return a robots.txt that disallows all spiders when DEBUG is True.
if getattr(settings, "DEBUG", False):
    urlpatterns += [
        url("^robots.txt$",
            lambda r: HttpResponse("User-agent: *\nDisallow: /",
                                   content_type="text/plain")),
    ]

# Miscellanous Mezzanine patterns.
urlpatterns += [
    url("^", include("mezzanine.core.urls")),
    url("^", include("mezzanine.generic.urls")),
]

# Mezzanine's Accounts app
if "mezzanine.accounts" in settings.INSTALLED_APPS:
    # We don't define a URL prefix here such as /account/ since we want
    # to honour the LOGIN_* settings, which Django has prefixed with
    # /account/ by default. So those settings are used in accounts.urls
    urlpatterns += [
        url("^", include("mezzanine.accounts.urls")),
    ]

# Mezzanine's Blog app - edited to redirect to our own view funcs
blog_installed = "mezzanine.blog" in settings.INSTALLED_APPS
if blog_installed:
    BLOG_SLUG = settings.BLOG_SLUG.rstrip("/")
    if BLOG_SLUG:
        BLOG_SLUG += "/"
blog_patterns = [
    url("^feeds/(?P<format>.*)%s$" % _slash,
        views.blog_post_feed, name="blog_post_feed"),
    url("^tag/(?P<tag>.*)/feeds/(?P<format>.*)%s$" % _slash,
        views.blog_post_feed, name="blog_post_feed_tag"),
    url("^tag/(?P<tag>.*)%s$" % _slash,
        blog_views.blog_post_list, name="blog_post_list_tag"),
    url("^category/(?P<category>.*)/feeds/(?P<format>.*)%s$" % _slash,
        views.blog_post_feed, name="blog_post_feed_category"),
    url("^category/(?P<category>.*)%s$" % _slash,
        blog_views.blog_post_list, name="blog_post_list_category"),
    url("^author/(?P<username>.*)/feeds/(?P<format>.*)%s$" % _slash,
        views.blog_post_feed, name="blog_post_feed_author"),
    url("^author/(?P<username>.*)%s$" % _slash,
        blog_views.blog_post_list, name="blog_post_list_author"),
    url("^archive/(?P<year>\d{4})/(?P<month>\d{1,2})%s$" % _slash,
        blog_views.blog_post_list, name="blog_post_list_month"),
    url("^archive/(?P<year>\d{4})%s$" % _slash,
        blog_views.blog_post_list, name="blog_post_list_year"),
    url("^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/"
        "(?P<slug>.*)%s$" % _slash,
        blog_views.blog_post_detail, name="blog_post_detail_day"),
    url("^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>.*)%s$" % _slash,
        blog_views.blog_post_detail, name="blog_post_detail_month"),
    url("^(?P<year>\d{4})/(?P<slug>.*)%s$" % _slash,
        blog_views.blog_post_detail, name="blog_post_detail_year"),
    url("^(?P<slug>.*)%s$" % _slash,
        blog_views.blog_post_detail, name="blog_post_detail"),
    url("^$", blog_views.blog_post_list, name="blog_post_list"),
]
urlpatterns += blog_patterns


# Mezzanine's Pages app.
PAGES_SLUG = ""
if "mezzanine.pages" in settings.INSTALLED_APPS:
    # No BLOG_SLUG means catch-all patterns belong to the blog,
    # so give pages their own prefix and inject them before the
    # blog urlpatterns.
    if blog_installed and not BLOG_SLUG.rstrip("/"):
        PAGES_SLUG = getattr(settings, "PAGES_SLUG", "pages").strip("/") + "/"
        blog_patterns_start = urlpatterns.index(blog_patterns[0])
        urlpatterns[blog_patterns_start:len(blog_patterns)] = [
            url("^%s" % str(PAGES_SLUG), include("mezzanine.pages.urls")),
        ]
        urlpatterns += blog_patterns
    else:
        urlpatterns += [
            url("^", include("mezzanine.pages.urls")),
        ]

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
