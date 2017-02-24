from django.contrib import admin
from models import AuthorProfile

class AuthorProfileAdmin(admin.ModelAdmin):
	pass

# class LikeAdmin(admin.ModelAdmin):
# 	pass

# Register your models here.
admin.site.register(AuthorProfile, AuthorProfileAdmin)
# admin.site.register(Like, LikeAdmin)