from __future__ import unicode_literals

from django.db import models
from mezzanine.utils.models import get_user_model_name
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import ugettext, ugettext_lazy as _

# Create your models here.
# class Like(models.Model):
#     """
#     A rating that can be given to a piece of content.
#     """

#     rating_date = models.DateTimeField(_("Like Date"), auto_now_add=True, null=True)
#     content_type = models.ForeignKey("contenttypes.ContentType")
#     object_pk = models.IntegerField()
#     content_object = GenericForeignKey("content_type", "object_pk")
#     user = models.ForeignKey(get_user_model_name(), verbose_name=_("Liker"),
#         null=True, related_name="%(class)ss")

#     class Meta:
#         verbose_name = _("Like")
#         verbose_name_plural = _("Likes")

class AuthorProfile(models.Model):
 	"""
 	Profile for an author.
 	"""

 	picture = models.ImageField(upload_to="profile_pictures")
 	tagline = models.TextField(null=True, max_length=250)
 	user = models.OneToOneField('auth.User', blank=False, null=False, related_name="userprofile")

 	@staticmethod
 	def get_pics_as_dict():
 		ret = {}
 		for profile in AuthorProfile.objects.all():
 			ret[profile.user.username] = profile.picture
 		return ret