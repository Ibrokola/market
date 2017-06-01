from django.contrib import admin

from .models import Product, MyProducts, Thumbnail






class ThumbnailInline(admin.TabularInline):
	extra = 1
	model = Thumbnail


class ProductAdmin(admin.ModelAdmin):
	inlines = [ThumbnailInline] 
	list_display = ("user", "__str__", "make", "age", "description", "price_1", "price_2")
	search_fields = ["title", "description", "price", "age"]
	list_filter = ["title", "price_1", "price_2"]
	list_editable = ["price_2"]

	class Meta:
		model = Product



admin.site.register(Product, ProductAdmin)
admin.site.register(MyProducts)