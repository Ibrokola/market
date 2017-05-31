from django.contrib import admin

from .models import Profile





class ProfileAdmin(admin.ModelAdmin):
	list_display = ("user", "__str__", "address", "address_2", "member_since")
	search_fields = ["title", "address", "member_since", "user"]
	list_filter = ["title", "address", "user"]
	# list_editable = ["price_2"]

	class Meta:
		model = Profile




admin.site.register(Profile, ProfileAdmin)